import spacy
from transformers import pipeline
from nltk.tokenize import word_tokenize
import nltk
from langchain.chains import SequentialChain
from langchain.steps import Step

nltk.download("punkt")
nltk.download("stopwords")

nlp_model = spacy.load("en_core_web_lg")
qa_pipeline = pipeline(
    "question-answering", model="bert-large-uncased-whole-word-masking-finetuned-squad"
)


def process_text(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = f.read()
    return nlp_model(data)


def extract_sentences(data_processed):
    return [sent.text.strip() for sent in data_processed.sents]


def split_sentences(sentences):
    sentences_processed = []
    for sentence in sentences:
        s = sentence.split("\n")
        for i in s:
            s_ = i.split(".")
            sentences_processed.extend(s_)
    return sentences_processed


def parse_attractions(sentences_processed):
    attractions = {}
    current_index = 0
    for sentence in sentences_processed:
        sentence = sentence.strip()
        if sentence.isdigit():
            val = int(sentence)
            if val == current_index + 1:
                current_index += 1
                attractions[current_index] = ""
        else:
            if current_index != 0:
                attractions[current_index] += sentence + " "
    return attractions


def tokenize_and_clean(attraction_data):
    words = word_tokenize(attraction_data)
    return [w for w in words if w not in [":", "-", "image", "credit", "source"]]


def create_empty_template():
    return {
        "Location": "",
        "Timings": "",
        "Entry Fee": "",
        "Description": "",
        "Built By": "",
        "Built In": "",
        "Price For Two": "",
    }


def fill_template(words):
    val = create_empty_template()
    current = "Description"
    count = 0
    while count < len(words):
        word = words[count].lower()
        if word == "location":
            current = "Location"
        elif word == "timings":
            current = "Timings"
        elif word == "entry" and words[count + 1].lower() == "fee":
            current = "Entry Fee"
            count += 2
            continue
        elif word == "fee":
            current = "Entry Fee"
        elif (
            word == "price"
            and words[count + 1].lower() == "for"
            and words[count + 2].lower() == "two"
        ):
            current = "Price For Two"
            count += 3
            continue
        elif word == "built" and words[count + 1].lower() == "by":
            current = "Built By"
            count += 2
            continue
        elif word == "built-in":
            current = "Built In"
        elif (
            word == "how"
            and words[count + 1].lower() == "to"
            and words[count + 2].lower() == "reach"
        ):
            current = "Location"
            count += 3
            continue
        else:
            val[current] += word + " "
        count += 1
    return val


def ask_questions(val):
    questions = {
        "name": "What is the name of the attraction?",
        "location": "What is the location of the attraction?",
        "timings": "What are the timings of the attraction?",
        "entry_fee": "What is the entry fee of the attraction?",
        "built_in": "When was the attraction built?",
        "built_by": "Who built the attraction?",
        "price_for_two": "What is the price for two at the attraction in inr?",
    }
    answers = {}
    answers["name"] = qa_pipeline(
        question=questions["name"], context=str(val["Description"])
    )
    answers["location"] = (
        qa_pipeline(question=questions["location"], context=val["Location"])
        if val["Location"]
        else {"answer": "Not Found"}
    )
    answers["timings"] = (
        qa_pipeline(question=questions["timings"], context=val["Timings"])
        if val["Timings"]
        else {"answer": "Not Found"}
    )
    answers["entry_fee"] = (
        qa_pipeline(question=questions["entry_fee"], context=val["Entry Fee"])
        if val["Entry Fee"]
        else {"answer": "Not Found"}
    )
    if "no" in answers["entry_fee"]["answer"].lower():
        answers["entry_fee"] = {"answer": "No"}
    answers["built_in"] = (
        qa_pipeline(question=questions["built_in"], context=val["Built In"])
        if val["Built In"]
        else {"answer": "Not Found"}
    )
    answers["built_by"] = (
        qa_pipeline(question=questions["built_by"], context=val["Built By"])
        if val["Built By"]
        else {"answer": "Not Found"}
    )
    answers["price_for_two"] = (
        qa_pipeline(question=questions["price_for_two"], context=val["Price For Two"])
        if val["Price For Two"]
        else {"answer": "Not Found"}
    )
    return answers


def write_results(file_path, attractions, qa_pipeline):
    with open(file_path, "w", encoding="utf-8") as write_file:
        for id, attraction_data in attractions.items():
            words = tokenize_and_clean(attraction_data)
            val = fill_template(words)
            answers = ask_questions(val)
            write_file.write(
                f"""
                Name: {answers['name']['answer']}
                Location: {answers['location']['answer']}
                Timings: {answers['timings']['answer']}
                Entry Fee: {answers['entry_fee']['answer']}
                Built In: {answers['built_in']['answer']}
                Built By: {answers['built_by']['answer']}
                Price For Two: {answers['price_for_two']['answer']}
                Description: {val['Description']}
                """
            )


data_processing_step = Step(
    process_text, inputs=["file_path"], outputs=["data_processed"]
)
sentence_extraction_step = Step(
    extract_sentences, inputs=["data_processed"], outputs=["sentences"]
)
sentence_splitting_step = Step(
    split_sentences, inputs=["sentences"], outputs=["sentences_processed"]
)
attraction_parsing_step = Step(
    parse_attractions, inputs=["sentences_processed"], outputs=["attractions"]
)
result_writing_step = Step(
    write_results, inputs=["file_path", "attractions", "qa_pipeline"]
)

pipeline = SequentialChain(
    steps=[
        data_processing_step,
        sentence_extraction_step,
        sentence_splitting_step,
        attraction_parsing_step,
        result_writing_step,
    ]
)

pipeline(
    {"file_path": "../webscraped data/traveltriangle.txt", "qa_pipeline": qa_pipeline}
)
