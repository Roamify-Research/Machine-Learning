import pandas as pd

def load_data():
    attractions_data = pd.read_csv('../datasets/final_attractions.csv', usecols=['Name', 'State', 'City', 'Opening Hours', 'Description'])
    user_ratings_data = pd.read_csv('../datasets/user_ratings.csv', usecols=['Attraction', 'Noel', 'Harsh', 'Vikranth', 'Muthuraj', 'Armaan'])
    return attractions_data, user_ratings_data


def load_user_data(user):
    attractions_data = pd.read_csv('../datasets/final_attractions.csv', usecols=['Rating', 'Name', 'State', 'City', 'Country', 'Opening Hours', 'Description'])
    user_ratings_data = pd.read_csv('../datasets/user_ratings.csv', usecols=['Attraction', user])
    
    attractions_data.rename(columns={'Rating': 'Google_Rating'}, inplace=True)
    attractions_data['User_Rating'] = user_ratings_data[user]

    usecols=['Name','Google_Rating','User_Rating', 'State', 'City','Country', 'Opening Hours', 'Description']
    return attractions_data[usecols]
def get_recommendations(state, number_of_attractions, user):
    attractions_data, user_ratings_data = load_data()
    
    attraction_names = []
    attractions_description = {}
    for i in range(len(attractions_data)):
        if attractions_data['State'][i] == state:
            attraction_names.append(attractions_data['Name'][i])
            attractions_description[attractions_data['Name'][i]] = [
                attractions_data['City'][i], 
                attractions_data['Opening Hours'][i], 
                attractions_data['Description'][i]
            ]

    attractions = {}
    for i in range(len(user_ratings_data)):
        if user_ratings_data['Attraction'][i] in attraction_names:
            attractions[user_ratings_data['Attraction'][i]] = user_ratings_data[user][i]

    attractions_sorted = dict(sorted(attractions.items(), key=lambda item: item[1], reverse=True))

    if len(attractions_sorted) < number_of_attractions:
        message = f"Only {len(attractions_sorted)} attractions are available in {state} for {user}."
        number_of_attractions = len(attractions_sorted)
    else:
        message = None

    recommendations = []
    count = 0
    for name in attractions_sorted.keys():
        if count == number_of_attractions:
            break
        count += 1
        recommendations.append({
            'Name': name,
            'City': attractions_description[name][0],
            'Opening Hours': attractions_description[name][1],
            'Description': attractions_description[name][2]
        })

    return recommendations, message