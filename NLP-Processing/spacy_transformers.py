from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
import spacy
import nltk
from transformers import pipeline
import torch

nltk.download('punkt')
nltk.download('stopwords')

stopwords = set(stopwords.words('english'))
nlp_model = spacy.load('en_core_web_sm')
data = open("../webscraped data/traveltriangle.txt", "r").read()
data_processed = nlp_model(data)

sentences = sent_tokenize(data)
attractions = {}
current_index = 0
for index in range(len(sentences)):
    sentence = sentences[index]
    words = word_tokenize(sentence)
    words = [word for word in words if word.isalnum() and word not in stopwords]
    sentences[index] = " ".join(words)

    
    if sentences[index].isdigit():
        current_index = int(sentences[index])
        attractions[current_index] = []
    
    else:
        if current_index:
            attractions[current_index].append(sentences[index])

device = 'metal' if torch.cuda.is_available() else 'cpu'
summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=device)
pipeline_model = pipeline("question-answering", model = "distilbert-base-cased-distilled-squad", device=device)
result = {}

write_file = open("../after_scraping/traveltriangle_after.txt", "w")
for i in attractions:
    print(attractions[i][0])
    result[attractions[i][0]] = ""
    for j in range(1, len(attractions[i])):
        result[attractions[i][0]] += attractions[i][j] + ". "
    
    attraction_details = attractions[i][0]  + "\n" +result[attractions[i][0]]
    summary = summarizer(attraction_details)[0]['summary_text']

    question1 = "What is the attraction about?"
    description = pipeline_model(question=question1, context=summary)['answer']

    question2 = "What are the timings to visit?"
    timings = pipeline_model(question=question2, context=summary)['answer']

    question3 = "Where is the attraction located?"
    location = pipeline_model(question=question3, context=summary)['answer']


    result[attractions[i][0]] = {"Description": description, "Timings": timings, "Location": location}
    write_file.write(attractions[i][0] + "\n")
    write_file.write("Description: " + description + "\n")
    write_file.write("Timings: " + timings + "\n")
    write_file.write("Location: " + location + "\n\n")

write_file.close()

