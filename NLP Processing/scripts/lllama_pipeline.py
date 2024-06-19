from transformers import pipeline
import torch
import json

pipe = pipeline("text-generation", model="meta-llama/Meta-Llama-3-8B-Instruct")

def return_output(input):

    input = "Summarize: " + input
    messages = [
    {"role": "user", "content": input},
]

    response = pipe(messages)
    return response[0]["generated_responses"]


files = [
    'fine-tuning-goa_traveltriangle.json',
    'fine-tuning-italy_traveltriangle.json',
    'fine-tuning-japan_traveltriangle.json',
    'fine-tuning-kerala_traveltriangle.json',
    'fine-tuning-lakshwadeep_traveltriangle.json',
    'fine-tuning-makemytrip.json',
    'fine-tuning-tn_traveltriangle.json',
    'fine-tuning-vietnam_traveltriangle.json'
]

for i in files:
    data = json.load(open(f"../after_scraping/Context-Data/{i}", "r"))
    write_file =  open(f"../after_scraping/Summarized-LLAMA/summarized-{i}", "w")
    json_data = {}
    for id, context in data.items():
        d = {"context": context, "summary": return_output(context)}
        json_data[id] = d

    json.dump(json_data, write_file, indent=4)
    