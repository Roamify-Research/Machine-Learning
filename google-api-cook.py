import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pandas as pd
import googlemaps

nltk.download('punkt')
nltk.download('stopwords')

stop_words = set(stopwords.words('english'))
custom_stopwords = {'please', 'specify', 'country', 'state', 'want', 'visit'}
stop_words.update(custom_stopwords)

states = ['Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh', 'Goa', 'Gujarat', 'Haryana',
          'Himachal Pradesh', 'Jharkhand', 'Karnataka', 'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur',
          'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana',
          'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal']

states_lower = [state.lower() for state in states]

df = pd.read_csv('datasets/indian_attractions.csv')

gmaps = googlemaps.Client(key='YOUR_GOOGLE_API_KEY')

def filter_input():
    user_input = input()
    return user_input

def get_place_details(place_name, state):
    place_query = f"{place_name}, {state}, India"
    places_result = gmaps.places(query=place_query)
    if places_result['status'] == 'OK':
        place_details = places_result['results'][0]
        return {
            'name': place_details['name'],
            'address': place_details.get('formatted_address'),
            'rating': place_details.get('rating'),
            'user_ratings_total': place_details.get('user_ratings_total'),
            'types': place_details.get('types'),
            'url': place_details.get('url')
        }
    else:
        return None

def operations(sentence):
    tokenized_words = word_tokenize(sentence)

    filtered_sentence = [w for w in tokenized_words if w.lower() not in stop_words]

    location_found = False
    days_found = False
    state_name = ""

    for word in filtered_sentence:
        if word.lower() in states_lower:
            original_state = states[states_lower.index(word.lower())]
            state_name = original_state
            location_found = True
        elif word.isdigit():
            days_found = True

    if not location_found:
        print("No valid location found in your input.")
    if not days_found:
        print("No valid number of days found in your input.")

    if location_found:
        attractions = df[df['state'].str.lower() == state_name.lower()]
        if not attractions.empty:
            top_visited = attractions.sort_values(by='visits', ascending=False).head(3)
            for idx, row in top_visited.iterrows():
                place_details = get_place_details(row['name'], state_name)
                if place_details:
                    print(f"Name: {place_details['name']}, Address: {place_details['address']}, Visits: {row['visits']}, Rating: {place_details['rating']}")
                else:
                    print(f"Name: {row['name']}, Visits: {row['visits']}, Rating: {row['rating']}")

            top_rated = attractions.sort_values(by='rating', ascending=False).head(3)
            for idx, row in top_rated.iterrows():
                place_details = get_place_details(row['name'], state_name)
                if place_details:
                    print(f"Name: {place_details['name']}, Address: {place_details['address']}, Visits: {row['visits']}, Rating: {place_details['rating']}")
                else:
                    print(f"Name: {row['name']}, Visits: {row['visits']}, Rating: {row['rating']}")
        else:
            print(f"No attractions found for {state_name}.")

print("\nType 'exit' to quit the program.\n")
while True:
    user_input = filter_input()
    if user_input.lower() == 'exit':
        print("Exiting the program.")
        break
    operations(user_input)