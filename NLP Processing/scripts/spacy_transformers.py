from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
import spacy
import nltk
from transformers import pipeline
import roberta_pipeline
import json

nltk.download("punkt")
nltk.download("stopwords")
import os

stopwords = set(stopwords.words("english"))
nlp_model = spacy.load("en_core_web_lg")
# data = open("../webscraped data/traveltriangle.txt", "r").read()
files = os.listdir("../webscraped data/Muthuraj Dataset")
files = [file.split(".")[0] for file in files]
print(files)
for file_name in files:
    print(f"Executing {file_name}")
    data = open(
        f"../webscraped data/Muthuraj Dataset/{file_name}.txt", "r", encoding="utf-8"
    ).read()
    data_processed = nlp_model(data)

    sentences = [sent.text.strip() for sent in data_processed.sents]

    # summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    # pipeline_model = pipeline("question-answering", model="bert-large-uncased-whole-word-masking-finetuned-squad")
    sentences_processed = []
    current_index = 0
    attractions = {}
    for sentence in sentences:
        s = sentence.split("\n")
        for i in s:
            s_ = i.split(".")
            sentences_processed.extend(s_)

    for index in range(len(sentences_processed)):
        sentence = sentences_processed[index].strip()
        if sentence.isdigit():
            val = int(sentences_processed[index])
            if val == current_index + 1:
                current_index += 1
                attractions[current_index] = ""

        else:
            if current_index != 0:
                attractions[current_index] += sentence + " "

    # result = {}

    # write_file = open("../after_scraping/Initial/traveltriangle_after-vietnam.txt", "w")
    write_file = open(
        f"../after_scraping/Initial/Muthuraj Dataset/{file_name}_after.txt",
        "w",
        encoding="utf-8",
    )
    json_data = {}
    context_id = 0
    for id, attraction_data in attractions.items():
        words = word_tokenize(attraction_data)
        words = [
            w
            for w in words
            if w.isalnum()
            and w != ":"
            and w != "-"
            and w.lower() != "image"
            and w.lower() != "credit"
            and w.lower() != "source"
        ]
        val = {
            "Location": "",
            "Timings": "",
            "Entry Fee": "",
            "Description": "",
            "Built By": "",
            "Built In": "",
            "Price For Two": "",
        }
        current = "Description"
        count = 0
        attraction_data_llama = " ".join(words)
        while count < len(words) - 2:
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

        name = roberta_pipeline.return_output(
            "What is the name of the attraction?", val["Description"]
        )

        if val["Location"]:
            location = roberta_pipeline.return_output(
                "What is the location of the attraction?", val["Location"]
            )
        else:
            location = None

        if val["Timings"]:
            timings = roberta_pipeline.return_output(
                "What are the timings of the attraction?", val["Timings"]
            )
        else:
            timings = None

        if val["Entry Fee"]:
            entry_fee = roberta_pipeline.return_output(
                "What is the entry fee of the attraction?", val["Entry Fee"]
            )
            if "no" in entry_fee.lower():
                entry_fee = "No"
        else:
            entry_fee = None

        if val["Built In"]:
            built_in = roberta_pipeline.return_output(
                "When was the attraction built?", val["Built In"]
            )
        else:
            built_in = None

        if val["Built By"]:
            built_by = roberta_pipeline.return_output(
                "Who built the attraction?", val["Built By"]
            )
        else:
            built_by = None

        if val["Price For Two"]:
            price_for_two = roberta_pipeline.return_output(
                "What is the price for two at the attraction?", val["Price For Two"]
            )
        else:
            price_for_two = None

        result = ""
        result += f"Name: {name}\n"
        if location:
            result += f"Location: {location}.\n"
        if timings:
            result += f"Timings: {timings}.\n"
        if entry_fee:
            result += f"Entry Fee: {entry_fee}.\n"
        if built_in:
            result += f"{name} was built in {built_in}."
        if built_by:
            result += f"{name} was built by {built_by}."
        if price_for_two:
            result += f"The price for two at this attraction is {price_for_two}"
        if val["Description"]:
            result += f"Description: {val['Description']}.\n\n"

        write_file.write(result)

        json_data[str(context_id)] = attraction_data_llama
        context_id += 1

    with open(
        f"../after_scraping/Context-Data/Muthuraj Dataset/fine-tuning-{file_name}.json",
        "w",
    ) as f:
        json.dump(json_data, f, indent=4)

    write_file.close()
