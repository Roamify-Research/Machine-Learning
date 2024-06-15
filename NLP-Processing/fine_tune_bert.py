import nltk
import spacy
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from transformers import AutoTokenizer, AutoModelForQuestionAnswering, Trainer, TrainingArguments, pipeline
from datasets import Dataset, load_metric
import torch
import numpy as np

# Download necessary NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

# Load stopwords and spacy model
stopwords = set(stopwords.words('english'))
nlp_model = spacy.load('en_core_web_lg')

# Read the dataset
# data = open("traveltriangle.txt", "r").read()
data = open("../webscraped data/traveltriangle.txt", "r", encoding='utf-8').read()


# Preprocess the data using Spacy
data_processed = nlp_model(data)
sentences = [sent.text.strip() for sent in data_processed.sents]

# Tokenizer and model initialization
tokenizer = AutoTokenizer.from_pretrained("bert-large-uncased-whole-word-masking-finetuned-squad")
model = AutoModelForQuestionAnswering.from_pretrained("bert-large-uncased-whole-word-masking-finetuned-squad")

# Prepare dataset for question answering
qa_dataset = {
    'context': [],
    'question': [],
    'answers': {'text': [], 'answer_start': []}
}

# Extracting relevant parts from the text
def extract_info(sentences):
    current_index = 0
    attractions = {}
    sentences_processed = []

    for sentence in sentences:
        s = sentence.split("\n")
        for i in s:
            s_ = i.split(".")
            sentences_processed.extend(s_)

    for index in range(len(sentences_processed)):
        sentence = sentences_processed[index].strip()
        if sentence.isdigit():
            val = int(sentences_processed[index])
            if val == current_index + 1:
                current_index += 1
                attractions[current_index] = ""
        else:
            if current_index != 0:
                attractions[current_index] += (sentence + " ")

    return attractions

attractions = extract_info(sentences)

# Fill the dataset for question answering
for id, attraction_data in attractions.items():
    words = word_tokenize(attraction_data)
    words = [w for w in words if w.lower() not in ["image", "credit", "source", ":", "-"]]
    val = {"Location": "", "Timings": "", "Entry Fee": "", "Description": "", "Built By": "", "Built In": "", "Price For Two": ""}
    current = "Description"
    count = 0
    while count < len(words):
        word = words[count].lower()
        if word == "location":
            current = "Location"
        elif word == "timings":
            current = "Timings"
        elif word == "entry" and words[count + 1].lower() == "fee":
            current = "Entry Fee"
            count += 2
            continue
        elif word == "fee":
            current = "Entry Fee"
        elif word == "price" and words[count + 1].lower() == "for" and words[count + 2].lower() == "two":
            current = "Price For Two"
            count += 3
            continue
        elif word == "built" and words[count + 1].lower() == "by":
            current = "Built By"
            count += 2
            continue
        elif word == "built-in":
            current = "Built In"
        elif word == "how" and words[count + 1].lower() == "to" and words[count + 2].lower() == "reach":
            current = "Location"
            count += 3
            continue
        else:
            val[current] += (word + " ")
        count += 1

    # Append to the QA dataset
    qa_dataset['context'].append(attraction_data)
    qa_dataset['question'].append("What is the name of the attraction?")
    qa_dataset['answers']['text'].append("")  # Placeholder, should be filled based on manual labeling or another method
    qa_dataset['answers']['answer_start'].append(0)  # Placeholder

# Create a Dataset object
dataset = Dataset.from_dict(qa_dataset)

# Tokenize the dataset
def tokenize_function(examples):
    return tokenizer(examples['context'], examples['question'], truncation=True)

tokenized_datasets = dataset.map(tokenize_function, batched=True)

# Set up training arguments
training_args = TrainingArguments(
    output_dir='./results',
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=3,
    weight_decay=0.01,
)

# Define data collator
from transformers import DefaultDataCollator
data_collator = DefaultDataCollator()

# Define metric
metric = load_metric("squad")

def compute_metrics(p):
    return metric.compute(predictions=np.argmax(p.predictions, axis=2), references=p.label_ids)

# Create Trainer instance
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets,
    tokenizer=tokenizer,
    data_collator=data_collator,
    compute_metrics=compute_metrics,
)

# Train the model
trainer.train()

# Save the model
trainer.save_model("./fine-tuned-bert-model")

# Use the fine-tuned model for question answering
pipeline_model = pipeline("question-answering", model=model, tokenizer=tokenizer)

# Write the processed data to file
# write_file = open("../after_scraping/traveltriangle_after.txt", "w")
write_file = open("../after_scraping/traveltriangle_after.txt", "w", encoding='utf-8')
for id, attraction_data in attractions.items():
    # Create question-answer pairs
    questions = {
        "name": "What is the name of the attraction?",
        "location": "What is the location of the attraction?",
        "timings": "What are the timings of the attraction?",
        "entry_fee": "What is the entry fee of the attraction?",
        "built_in": "When was the attraction built?",
        "built_by": "Who built the attraction?",
        "price_for_two": "What is the price for two at the attraction in INR?"
    }
    answers = {}
    for key, question in questions.items():
        if val[key.capitalize()]:
            answer = pipeline_model(question=question, context=val[key.capitalize()])
            answers[key] = answer['answer']
        else:
            answers[key] = "Not Found"
    
    write_file.write(
        f"""
        Name: {answers['name']}
        Location: {answers['location']}
        Timings: {answers['timings']}
        Entry Fee: {answers['entry_fee']}
        Built In: {answers['built_in']}
        Built By: {answers['built_by']}
        Price For Two: {answers['price_for_two']}
        Description: {val['Description']}
        """
    )
write_file.close()