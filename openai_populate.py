import json
from openai import OpenAI

client = OpenAI(api_key='')

models = client.models.list()
print(models)
# Set up your OpenAI API key

# Load the input JSON file
with open('after_scraping/Context-Data/fine-tuning-traveltriangle-goa.json', 'r', encoding='utf-8') as infile:
    input_data = json.load(infile)

# Function to generate questions and answers
def generate_qna(context_index, text):
    questions = [
        "What is the name of the attraction?",
        "What is the location of the attraction?",
        "Describe the attraction in detail."
    ]
    answers = []

    for question in questions:
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Context: {text}\n\nQuestion: {question}\nAnswer:"}
        ]

        response = client.chat.completions.create(model="gpt-4",
        messages=messages,
        max_tokens=100)

        answers.append({
            "context_index": context_index,
            "question": question,
            "answer": response.choices[0].message.content.strip()
        })

    return answers

# Create a list to hold the Q&A pairs
qna_pairs = []

# Loop through the input data and generate Q&A pairs
for context_index, text in input_data.items():
    qna_pairs.extend(generate_qna(context_index, text))

# Save the Q&A pairs to an output JSON file
with open('after_scraping/three_qs/fine-tuning-dataset-traveltriangle-goa.json', 'w', encoding='utf-8') as outfile:
    json.dump(qna_pairs, outfile, ensure_ascii=False, indent=4)

print("Q&A pairs generated and saved to output JSON file.")