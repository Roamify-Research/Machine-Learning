from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
import spacy
import nltk
from transformers import pipeline

nltk.download('punkt')
nltk.download('stopwords')


stopwords = set(stopwords.words('english'))
nlp_model = spacy.load('en_core_web_lg')
data = open("../webscraped data/traveltriangle.txt", "r").read()
data_processed = nlp_model(data)

sentences = [sent.text.strip() for sent in data_processed.sents]


summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
pipeline_model = pipeline("question-answering", model="bert-large-uncased-whole-word-masking-finetuned-squad")
sentences_processed = []
current_index = 0
attractions = {}
for sentence in sentences:
    s = sentence.split("\n")
    for i in s:
        s_ = i.split(".")
        sentences_processed.extend(s_)

for index in range(len(sentences_processed)):
    sentence = sentences_processed[index]
    words = word_tokenize(sentence)
    words = [word for word in words if word.isalnum() and word not in stopwords]
    sentences_processed[index] = " ".join(words).strip()
    if sentences_processed[index].isdigit():
        val = int(sentences_processed[index])
        if val == current_index + 1:
            current_index += 1
            attractions[current_index] = ""
    
    else:
        if current_index!= 0:

            attractions[current_index] += (sentences_processed[index] + " ")


# result = {}

write_file = open("../after_scraping/traveltriangle_after.txt", "w")
for attraction_data in attractions.values():
    
    summary = attraction_data
    # summary = summarizer(attraction_data, max_length=300, min_length=100, length_penalty=2.0, num_beams=4, early_stopping=True)[0]['summary_text']
    question4 = "What is the name of the attraction?"
    name = pipeline_model(question=question4, context=summary)['answer']

    question1 =  "Describe the attraction in brief including its activities, history, and significance?"
    description = pipeline_model(question=question1, context=summary)['answer']

    question2 = "What are the timings to visit?"
    timings = pipeline_model(question=question2, context=summary)['answer']

    question3 = "Where is the attraction located?"
    location = pipeline_model(question=question3, context=summary)['answer']

    question5 = "What is the entry fee for the attraction, if any? If there is no entry fee, return 'No Information'."
    entry_fee = pipeline_model(question=question5, context=summary)['answer']
    print(f"""
Name: {name}
Description: {description}
Timings: {timings}
Location: {location}
Entry Fee: {entry_fee}
          """)


    write_file.write("Name: " + name + "\n")
    write_file.write("Description: " + description + "\n")
    write_file.write("Timings: " + timings + "\n")
    write_file.write("Location: " + location + "\n")
    write_file.write("Entry Fee" + entry_fee + "\n\n")

write_file.close()