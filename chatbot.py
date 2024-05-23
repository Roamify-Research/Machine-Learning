import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('punkt')
nltk.download('stopwords')

stopwords = set(stopwords.words('english'))

def chatbot():
    print("Hello! I am a chatbot. I can help you with your travel plans.")
    print("Please enter your query: ")
    user_input = input()
    return user_input

def operations(sentence):
    tokenized_words = word_tokenize(sentence)

    filtered_sentence = [w for w in tokenized_words if not w in stopwords]
    places = ['Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jharkhand', 'Karnataka', 'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal']
    places = [i.lower() for i in places]

    for i in filtered_sentence:
        if i.lower() in places:
            print("Location: " + i)
        elif i.isdigit():
            print("Days: " + i)

while (True):
    user_input = chatbot()
    operations(user_input)