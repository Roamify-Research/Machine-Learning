import nltk
import spacy
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from transformers import AutoTokenizer, TFAutoModelForQuestionAnswering, Trainer, TrainingArguments, pipeline
from datasets import Dataset, load_metric
import numpy as np
import json
# Download necessary NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

# Load stopwords and spacy model
stopwords = set(stopwords.words('english'))
nlp_model = spacy.load('en_core_web_lg')

# Read the dataset
# data = open("../webscraped data/traveltriangle.txt", "r").read()
# data = open("../webscraped data/traveltriangle.txt", "r", encoding='utf-8').read()


# Preprocess the data using Spacy
# data_processed = nlp_model(data)
# sentences = [sent.text.strip() for sent in data_processed.sents]

# Tokenizer and model initialization
tokenizer = AutoTokenizer.from_pretrained("bert-large-uncased-whole-word-masking-finetuned-squad")
model = TFAutoModelForQuestionAnswering.from_pretrained("bert-large-uncased-whole-word-masking-finetuned-squad")

# Prepare dataset for question answering
qa_dataset = {
    'context': [],
    'question': [],
    'answers': {'text': [], 'answer_start': []}
}
context_data_files = ["../NLP Processing/after_scraping/Context-Data/fine-tuning-traveltriangle-goa.json", "../NLP Processing/after_scraping/Context-Data/fine-tuning-traveltriangle-japan.json", "../NLP Processing/after_scraping/Context-Data/fine-tuning-traveltriangle-vietnam.json"]
dataset_files = ["../NLP Processing/after_scraping/four_qns/fine-tuning-dataset-traveltriangle-goa.json","../NLP Processing/after_scraping/four_qns/fine-tuning-dataset-traveltriangle-japan.json", "../NLP Processing/after_scraping/Previous Datasets/fine-tuning-dataset-traveltriangle-vietnam.json"]

context_data = {}

questions = [
    "What is the name of the attraction?",
    "What is the location of the attraction?",
    "Describe the attraction in detail.",
    "What type of attraction is it? (e.g. historical, natural, amusement, beach)"
]


for i in range(len(context_data_files)):
    context_data[i] = {}
    with open(context_data_files[i], "r") as file:
        context_data[i].update(json.load(file))
    
print(context_data.keys())
print(context_data[0].keys())

for i in range(len(dataset_files)):
    with open(dataset_files[i], "r") as file:
        dataset = json.load(file)
        for entry in dataset:
            id = entry['context_index']
            for question in questions:
                if question == entry['question']:
                    qa_dataset['context'].append(context_data[i][str(id)])
                    qa_dataset['question'].append(question)
                    qa_dataset['answers']['text'].append(entry["answer"])
                    qa_dataset['answers']['answer_start'].append(0)

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

# # Use the fine-tuned model for question answering
# pipeline_model = pipeline("question-answering", model=model, tokenizer=tokenizer)

# # Write the processed data to file
# # write_file = open("../after_scraping/Initial/traveltriangle_after.txt", "w")
# write_file = open("../after_scraping/Initial/traveltriangle_after.txt", "w", encoding='utf-8')
# for id, attraction_data in attractions.items():
#     # Create question-answer pairs
#     questions = {
#         "name": "What is the name of the attraction?",
#         "location": "What is the location of the attraction?",
#         "timings": "What are the timings of the attraction?",
#         "entry_fee": "What is the entry fee of the attraction?",
#         "built_in": "When was the attraction built?",
#         "built_by": "Who built the attraction?",
#         "price_for_two": "What is the price for two at the attraction in INR?",
#         "description": "Describe the attraction in brief?",
#         "type": "What type of attraction is it? (e.g. historical, natural, amusement, beach)"
#     }
#     answers = {}
#     for key, question in questions.items():
#         if val[key.capitalize()]:
#             answer = pipeline_model(question=question, context=val[key.capitalize()])
#             answers[key] = answer['answer']
#         else:
#             answers[key] = "Not Found"
    
#     write_file.write(
#         f"""
#         Name: {answers['name']}
#         Location: {answers['location']}
#         Timings: {answers['timings']}
#         Entry Fee: {answers['entry_fee']}
#         Built In: {answers['built_in']}
#         Built By: {answers['built_by']}
#         Price For Two: {answers['price_for_two']}
#         Description: {val['Description']}
#         """
#     )
# write_file.close()