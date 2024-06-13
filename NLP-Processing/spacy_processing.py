from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
import spacy
import nltk

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



result = {}

write_file = open("../after_scraping/traveltriangle_after.txt", "w")
for i in attractions:
    result[attractions[i][0]] = ""
    for j in range(1, len(attractions[i])):
        result[attractions[i][0]] += attractions[i][j] + ". "
    

    write_file.write(attractions[i][0] + "\n")
    write_file.write(result[attractions[i][0]] + "\n\n")

write_file.close()

