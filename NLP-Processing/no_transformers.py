import spacy
import nltk
import re
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from collections import defaultdict

nltk.download('punkt')
nltk.download('stopwords')

stopwords_set = set(stopwords.words('english'))
nlp = spacy.load('en_core_web_sm')

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
summaries = defaultdict(list)

for idx in attractions:
    combined_text = " ".join(attractions[idx])
    doc = nlp(combined_text)
    entities[idx] = [ent.text for ent in doc.ents if ent.label_ in ['GPE', 'LOC', 'ORG', 'PERSON']]
    
    # Extract and rank sentences
    sentence_ranking = []
    for sent in doc.sents:
        score = 0
        for token in sent:
            if token.ent_type_ in ['GPE', 'LOC', 'ORG', 'PERSON']:
                score += 2
            elif token.pos_ in ['PROPN', 'VERB']:
                score += 1
        sentence_ranking.append((score, sent.text))
    
    # Sort sentences by score
    top_sentences = sorted(sentence_ranking, key=lambda x: x[0], reverse=True)[:3]
    summary = " ".join([sent[1] for sent in top_sentences])
    summaries[idx] = summary

with open("../after_scraping/vik_2_traveltriangle.txt", "w", encoding="utf-8") as write_file:
    for idx in summaries:
        attraction_name = entities[idx][0] if entities[idx] else 'Unknown Attraction'
        write_file.write(f"{idx}. {attraction_name}\n")
        write_file.write(f"{summaries[idx]}\n\n")