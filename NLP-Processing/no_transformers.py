from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
import spacy
import nltk

nltk.download('punkt')
nltk.download('stopwords')


stopwords = set(stopwords.words('english'))
nlp_model = spacy.load('en_core_web_lg')
data = open("../webscraped data/goatourismorg.txt", "r").read()
data_processed = nlp_model(data)

sentences = [sent.text.strip() for sent in data_processed.sents]


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


