import csv
import pandas as pd
import numpy as np
users = ['Noel','Harsh', 'Vikranth','Muthuraj','Armaan']
import random
def return_attractions():
    attractions_data = pd.read_csv('datasets/indian_attractions.csv', usecols=['Name', 'Rating', 'Visits'])
    attractions = []
    for i in range(len(attractions_data)):
        attributes = [attractions_data['Rating'][i], attractions_data['Visits'][i]]
        if attributes:
            attractions.append(attributes)

    attractions = np.array(attractions)
    return attractions

def return_user_attractions_rating():
    users = ['Noel','Harsh', 'Vikranth','Muthuraj','Armaan']
    user_attractions_data = pd.read_csv('datasets/user_attractions_rating.csv')
    user_attractions = []
    for i in range(len(user_attractions_data)):
        attributes = []
        for j in users:
            attributes.append(user_attractions_data[j][i])
        
        user_attractions.append(attributes)
    user_attractions_data = np.array(user_attractions)

    return user_attractions_data

def initial():
    
    write_file = open('datasets/user_attractions_rating.csv', 'w',newline='')
    writer = csv.writer(write_file)

    writer.writerow(["Name"] + users)

    attractions_data = pd.read_csv('datasets/indian_attractions.csv', usecols=['Name','Rating'])

    for i in range(len(attractions_data)):
        values = []
        for _ in users:
            n = random.randint(0,3)
            if n == 0:
                values.append(attractions_data['Rating'][i])
            else:
                values.append(0)
        writer.writerow([attractions_data['Name'][i]] + values)

    write_file.close()

initial()