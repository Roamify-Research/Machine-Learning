import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('punkt')
nltk.download('stopwords')

stop_words = set(stopwords.words('english'))
custom_stopwords = {'please', 'specify', 'country', 'state', 'want', 'visit'}
stop_words.update(custom_stopwords)

states = ['Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh', 'Goa', 'Gujarat', 'Haryana',
          'Himachal Pradesh', 'Jharkhand', 'Karnataka', 'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur',
          'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana',
          'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal', 'Delhi']

states_lower = [state.lower() for state in states]

def filter_input():
    print("Hello! I am a filter. Please specify the Country and State you want to visit.")
    user_input = input()
    return user_input

def operations(sentence):
    tokenized_words = word_tokenize(sentence)

    filtered_sentence = [w for w in tokenized_words if w.lower() not in stop_words]

    location_found = False
    days_found = False

    for word in filtered_sentence:
        if word.lower() in states_lower:
            original_state = states[states_lower.index(word.lower())]
            print("Location: " + original_state)
            location_found = True
        elif word.isdigit():
            print("Days: " + word)
            days_found = True

    if not location_found:
        print("No valid location found in your input.")
    if not days_found:
        print("No valid number of days found in your input.")

print("\nType 'exit' to quit the program.\n")

while True:
    user_input = filter_input()
    if user_input.lower() == 'exit':
        print("Exiting the program.")
        break
    operations(user_input)