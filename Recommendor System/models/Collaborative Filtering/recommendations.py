# Recommendation System Core Logic implemented in models/collaborative_filtering.ipynb

import pandas as pd


def print_recommendations(state, number_of_attractions, user):
    attractions_data = pd.read_csv(
        "../../datasets/final_attractions.csv",
        usecols=["Name", "State", "City", "Opening Hours", "Description"],
    )
    attraction_names = []
    attractions_description = {}
    for i in range(len(attractions_data)):
        if attractions_data["State"][i] == state:
            attraction_names.append(attractions_data["Name"][i])
            attractions_description[attractions_data["Name"][i]] = [
                attractions_data["City"][i],
                attractions_data["Opening Hours"][i],
                attractions_data["Description"][i],
            ]

    attractions = {}
    user_ratings_data = pd.read_csv(
        "../../datasets/predictions/predicted_user_ratings.csv", usecols=["Name", user]
    )

    for i in range(len(user_ratings_data)):
        if user_ratings_data["Name"][i] in attraction_names:
            attractions[user_ratings_data["Name"][i]] = user_ratings_data[user][i]

    attractions_sorted = dict(
        sorted(attractions.items(), key=lambda item: item[1], reverse=True)
    )

    count = 0
    for name in attractions_sorted.keys():
        if count == number_of_attractions:
            break
        count += 1
        print(f"Attraction name: {name}")
        print(f"City: {attractions_description[name][0]}")
        print(f"Opening Hours: {attractions_description[name][1]}")
        print(f"Description: {attractions_description[name][2]}")
        print("***************************************************")


while True:
    print("Enter the state you want to visit:")
    state = input()
    print("Enter the number of attractions you want to visit:")
    number_of_attractions = int(input())
    print("Enter the user for whom you want to get recommendations:")
    user = input()
    users = [
        i
        for i in pd.read_csv("../../datasets/first-user-study-20.csv").columns
        if i != "Name" and i != "State" and i != "Country"
    ]
    if user in users:
        print_recommendations(state, number_of_attractions, user)
    else:
        print("Invalid user. Please enter a valid user.")

    print("Do you want to continue? (yes/no)")
    cont = input()
    if cont == "no":
        break
