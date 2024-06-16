import json
import openai

# Set up your OpenAI API key
openai.api_key = 'your-api-key'

# Load the input JSON file
with open('after_scraping/Context-Data/fine-tuning-traveltriangle-goa.json', 'r', encoding='utf-8') as infile:
    input_data = json.load(infile)

# Function to generate questions and answers
def generate_qna(context_index, text):
    questions = [
        "What is the name of the attraction?",
        "What is the location of the attraction?",
        "Describe the attraction in brief"
    ]
    answers = []
    
    # Generating responses using OpenAI API
    for question in questions:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"Context: {text}\n\nQuestion: {question}\nAnswer:",
            max_tokens=150
        )
        answer = response['choices'][0]['text'].strip()
        answers.append({
            "context_index": context_index,
            "question": question,
            "answer": answer
        })
    return answers

# Process the data
output_data = []
for context_index, text in input_data.items():
    qna_pairs = generate_qna(context_index, text)
    output_data.extend(qna_pairs)

# Write the output to a new JSON file
with open('after_scraping/three_qs/fine-tuning-dataset-traveltriangle-goa.json', 'w', encoding='utf-8') as outfile:
    json.dump(output_data, outfile, ensure_ascii=False, indent=4)

print("Processing complete. Output saved to after_scraping/three_qs/fine-tuning-dataset-traveltriangle-goa.json")