import pandas as pd
import random
import os

def search_user_ratings(user, attraction):
    user_ratings_data = pd.read_csv('../datasets/user_attractions_ratings.csv')
    
    if user not in user_ratings_data.columns:
        return 0

    user_ratings_data = user_ratings_data[['Attraction', user]]
    if attraction in user_ratings_data['Attraction'].values:
        rating = user_ratings_data.loc[user_ratings_data['Attraction'] == attraction, user].values[0]
        return rating
    else:
        return 0

def load_data():
    attractions_data = pd.read_csv('../datasets/final_attractions.csv', usecols=['Name', 'State', 'City', 'Opening Hours', 'Description', 'Rating'])
    user_ratings_data = pd.read_csv('../datasets/user_attractions_ratings.csv')
    return attractions_data, user_ratings_data

def load_predicted_data():
    attractions_data = pd.read_csv('../datasets/final_attractions.csv', usecols=['Name', 'State', 'City', 'Opening Hours', 'Description', 'Rating'])
    user_ratings_data = pd.read_csv('../datasets/predicted_user_ratings.csv')
    return attractions_data, user_ratings_data

def save_data(user_ratings_data):
    user_ratings_data.to_csv('../datasets/user_attractions_ratings.csv', index=False)

def load_user_data(user):
    attractions_data = pd.read_csv('../datasets/final_attractions.csv', usecols=['Rating', 'Name', 'State', 'City', 'Country', 'Opening Hours', 'Description'])
    if user not in pd.read_csv('../datasets/predicted_user_ratings.csv').columns:
        return None

    user_ratings_data = pd.read_csv('../datasets/predicted_user_ratings.csv', usecols=['Attraction', user])
    attractions_data.rename(columns={'Rating': 'Google_Rating'}, inplace=True)
    attractions_data['User_Rating'] = user_ratings_data[user]

    usecols = ['Name', 'Google_Rating', 'User_Rating', 'State', 'City', 'Country', 'Opening Hours', 'Description']
    return attractions_data[usecols]

def add_user_ratings(new_ratings, user):
    attractions_data, user_ratings_data = load_data()
    new_column_user = []

    if user not in user_ratings_data.columns:
        for i in range(len(attractions_data)):
            attraction = attractions_data['Name'][i]
            attraction_rating = attractions_data['Rating'][i]
            if attraction in new_ratings:
                new_column_user.append(new_ratings[attraction])
            else:
                new_column_user.append(0)
                # n = random.randint(0, 5)
                # if n == 0:
                #     new_column_user.append(attraction_rating)
                # else:
                #     new_column_user.append(0)
    else:
        for i in range(len(attractions_data)):
            attraction = attractions_data['Name'][i]
            attraction_rating = attractions_data['Rating'][i]
            if attraction in new_ratings:
                new_column_user.append(new_ratings[attraction])
            elif user_ratings_data.loc[i, user] != 0:
                new_column_user.append(user_ratings_data[user][i])
            else:
                new_column_user.append(0)
                # n = random.randint(0, 5)
                # if n == 0:
                #     new_column_user.append(attraction_rating)
                # else:
                #     new_column_user.append(0)

    user_ratings_data[user] = new_column_user
    save_data(user_ratings_data)

def get_recommendations(state, number_of_attractions, user):
    attractions_data, user_ratings_data = load_predicted_data()

    if user not in user_ratings_data.columns:
        user_ratings_data[user] = None
        return [], f"User {user} not found in the database. Please add user first."

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