import os
import json
directory_path = '../after_scraping/Manual Summarized'
items = os.listdir(directory_path)

count = 0
# Create a new file to store the summarized data
with open('../after_scraping/Fine-Tuning-Datasets/tuning_summarized_data.json', 'w') as file:
    l = []
    for item in items:
        
        with open(f'{directory_path}/{item}', 'r') as f:
            dataset = json.load(f)
            for id in dataset:
                l.append(dataset[id])
        
    json.dump(l, file, indent=4)