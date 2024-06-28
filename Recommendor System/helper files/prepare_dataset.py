import pandas as pd
import numpy as np
import csv
import random

users = ['Noel','Harsh', 'Vikranth','Muthuraj','Armaan']

def return_attractions():
    attractions_data = pd.read_csv('../datasets/indian_attractions.csv', usecols=['Name', 'Rating', 'Visits', 'Historical', 'Natural', 'Amusement', 'Beach'])
    attractions = []
    for i in range(len(attractions_data)):
        attributes = [attractions_data['Rating'][i], attractions_data['Visits'][i], attractions_data['Historical'][i], attractions_data['Natural'][i], attractions_data['Amusement'][i], attractions_data['Beach'][i]]
        if attributes:
            attractions.append(attributes)

    attractions = np.array(attractions)
    return attractions

def return_user_attractions_rating():
    users = ['Noel','Harsh', 'Vikranth','Muthuraj','Armaan']
    user_attractions_data = pd.read_csv('../datasets/user_attractions_rating.csv')
    user_attractions = []
    for i in range(len(user_attractions_data)):
        attributes = []
        for j in users:
            attributes.append(user_attractions_data[j][i])
        
        user_attractions.append(attributes)
    user_attractions_data = np.array(user_attractions)

    return user_attractions_data

def make_user_attractions():
    
    write_file = open('../datasets/user_attractions_ratings.csv', 'w',newline='')
    writer = csv.writer(write_file)

    writer.writerow(["Attraction"])

    final_attractions = pd.read_csv('../datasets/final_attractions.csv', usecols=['Name','Rating'])
    for i in range(len(final_attractions)):
        
        writer.writerow([final_attractions['Name'][i]])


    write_file.close()

def make_attractions():
    attractions_indian = pd.read_csv("../datasets/individual_countries/india.csv")
    attractions_oman = pd.read_csv('../datasets/individual_countries/oman.csv')
    attractions_uae = pd.read_csv('../datasets/individual_countries/uae.csv')
    attractions_qatar = pd.read_csv('../datasets/individual_countries/qatar.csv')
    attractions_uk = pd.read_csv('../datasets/individual_countries/uk.csv')
    attractions_us = pd.read_csv('../datasets/individual_countries/us.csv')

    write_file = open("../datasets/final_attractions.csv", 'w',newline='')
    writer = csv.writer(write_file)

    writer.writerow(["Name", "Rating", "Visitors", "Historical", "Natural", "Amusement", "Beach", 'State', 'Country', 'Description','City','Opening Hours'])
    
    for i in range(len(attractions_indian)):
        writer.writerow([attractions_indian['Name'][i], attractions_indian['Rating'][i], attractions_indian['Visitors'][i], attractions_indian['Historical'][i], attractions_indian['Natural'][i], attractions_indian['Amusement'][i], attractions_indian['Beach'][i], attractions_indian['State'][i], 'India', attractions_indian['Description'][i], attractions_indian['City'][i], attractions_indian['Opening Hours'][i]])
    for i in range(len(attractions_oman)):
        writer.writerow([attractions_oman['Name'][i], attractions_oman['Rating'][i], attractions_oman['Visitors'][i], attractions_oman['Historical'][i], attractions_oman['Natural'][i], attractions_oman['Amusement'][i], attractions_oman['Beach'][i], attractions_oman['State'][i], 'Oman', attractions_oman['Description'][i], attractions_oman['City'][i], attractions_oman['Opening Hours'][i]])
    for i in range(len(attractions_uae)):
        writer.writerow([attractions_uae['Name'][i], attractions_uae['Rating'][i], attractions_uae['Visitors'][i], attractions_uae['Historical'][i], attractions_uae['Natural'][i], attractions_uae['Amusement'][i], attractions_uae['Beach'][i], attractions_uae['State'][i], 'UAE', attractions_uae['Description'][i], attractions_uae['City'][i], attractions_uae['Opening Hours'][i]])
    for i in range(len(attractions_qatar)):
        writer.writerow([attractions_qatar['Name'][i], attractions_qatar['Rating'][i], attractions_qatar['Visitors'][i], attractions_qatar['Historical'][i], attractions_qatar['Natural'][i], attractions_qatar['Amusement'][i], attractions_qatar['Beach'][i], attractions_qatar['State'][i], 'Qatar', attractions_qatar['Description'][i], attractions_qatar['City'][i], attractions_qatar['Opening Hours'][i]])

    for i in range(len(attractions_uk)):
        writer.writerow([attractions_uk['Name'][i], attractions_uk['Rating'][i], attractions_uk['Visitors'][i], attractions_uk['Historical'][i], attractions_uk['Natural'][i], attractions_uk['Amusement'][i], attractions_uk['Beach'][i], attractions_uk['State'][i], 'UK', attractions_uk['Description'][i], attractions_uk['City'][i], attractions_uk['Opening Hours'][i]])

    for i in range(len(attractions_us)):
        writer.writerow([attractions_us['Name'][i], attractions_us['Rating'][i], attractions_us['Visitors'][i], attractions_us['Historical'][i], attractions_us['Natural'][i], attractions_us['Amusement'][i], attractions_us['Beach'][i], attractions_us['State'][i], 'US', attractions_us['Description'][i], attractions_us['City'][i], attractions_us['Opening Hours'][i]])

    write_file.close()

def randomize(percent):
    user_ratings = pd.read_csv('../datasets/first-user-study-ratings.csv')

    attractions_ratings = pd.read_csv('../datasets/final_attractions.csv', usecols=['Rating'])


    for i in range(len(attractions_ratings)):
        for j in range(len(user_ratings.columns)):
            if user_ratings.iloc[i,j] == 0:
                n = random.randint(0, int(100/percent))
                if n == 0:
                    user_ratings.iloc[i, j] = attractions_ratings['Rating'][i]

    user_ratings.to_csv(f'../datasets/first-user-study-{percent}.csv', index=False)

randomize(20)