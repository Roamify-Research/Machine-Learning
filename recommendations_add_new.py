import pandas as pd

def print_recommendations(state, number_of_attractions, user):
    attractions_data = pd.read_csv('datasets/final_attractions.csv', usecols=['Name', 'State', 'City', 'Opening Hours', 'Description'])
    attraction_names = []
    attractions_description = {}
    for i in range(len(attractions_data)):
        if attractions_data['State'][i] == state:
            attraction_names.append(attractions_data['Name'][i])
            attractions_description[attractions_data['Name'][i]] = [attractions_data['City'][i], attractions_data['Opening Hours'][i], attractions_data['Description'][i]]

    attractions = {}
    user_ratings_data = pd.read_csv('datasets/user_ratings.csv', usecols=['Attraction', user])

    for i in range(len(user_ratings_data)):
        if user_ratings_data['Attraction'][i] in attraction_names:
            attractions[user_ratings_data['Attraction'][i]] = user_ratings_data[user][i]

    attractions_sorted = dict(sorted(attractions.items(), key=lambda item: item[1], reverse=True))

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

def add_new_attraction():
    name = input("Enter the attraction name: ")
    state = input("Enter the state: ")
    city = input("Enter the city: ")
    opening_hours = input("Enter the opening hours: ")
    description = input("Enter the description: ")

    new_attraction = pd.DataFrame({
        'Name': [name],
        'State': [state],
        'City': [city],
        'Opening Hours': [opening_hours],
        'Description': [description]
    })

    new_attraction.to_csv('datasets/final_attractions.csv', mode='a', header=False, index=False)
    print("New attraction added successfully!")

while True:
    print("Do you want to get recommendations or add a new attraction? (recommendation/add):")
    action = input().strip().lower()

    if action == 'recommendation':
        print("Enter the state you want to visit:")
        state = input()
        print("Enter the number of attractions you want to visit:")
        number_of_attractions = int(input())
        print("Enter the user for whom you want to get recommendations:")
        user = input()
        if user in ['Noel', 'Harsh', 'Vikranth', 'Muthuraj', 'Armaan']:
            print_recommendations(state, number_of_attractions, user)
        else:
            print("Invalid user. Please enter a valid user.")
    elif action == 'add':
        add_new_attraction()
    else:
        print("Invalid action. Please enter 'recommendation' or 'add'.")

    print("Do you want to continue? (yes/no)")
    cont = input().strip().lower()
    if cont == 'no':
        break