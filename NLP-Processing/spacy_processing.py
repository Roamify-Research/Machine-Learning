import spacy
import nltk
import re
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from transformers import pipeline

nltk.download('punkt')
nltk.download('stopwords')

stopwords_set = set(stopwords.words('english'))
nlp_model = spacy.load('en_core_web_sm')

with open("../webscraped data/traveltriangle.txt", "r", encoding="utf-8") as file:
    data = file.read()

sentences = sent_tokenize(data)
attractions = {}
current_index = 0

for sentence in sentences:
    words = word_tokenize(sentence)
    words = [word for word in words if word.isalnum() and word.lower() not in stopwords_set]
    cleaned_sentence = " ".join(words)

    match = re.match(r'^(\d+)\.\s*', sentence)
    if match:
        current_index = int(match.group(1))
        attractions[current_index] = []
    elif current_index:
        attractions[current_index].append(cleaned_sentence)

entities = {}
for idx in attractions:
    combined_text = " ".join(attractions[idx])
    doc = nlp_model(combined_text)
    entities[idx] = [ent.text for ent in doc.ents if ent.label_ in ['GPE', 'LOC', 'ORG', 'PERSON']]

summarizer = pipeline("summarization")

def chunk_text(text, chunk_size=512):
    words = text.split()
    for i in range(0, len(words), chunk_size):
        yield " ".join(words[i:i + chunk_size])

summarized_attractions = {}
for idx, texts in attractions.items():
    full_text = " ".join(texts)
    chunks = list(chunk_text(full_text))
    summary = ""
    for chunk in chunks:
        chunk_summary = summarizer(chunk, max_length=130, min_length=30, do_sample=False)[0]['summary_text']
        summary += chunk_summary + " "
    summarized_attractions[idx] = summary.strip()

with open("../after_scraping/vik_traveltriangle.txt.txt", "w", encoding="utf-8") as write_file:
    for idx in summarized_attractions:
        attraction_name = entities[idx][0] if entities[idx] else 'Unknown Attraction'
        write_file.write(f"{idx}. {attraction_name}\n")
        write_file.write(f"{summarized_attractions[idx]}\n\n")