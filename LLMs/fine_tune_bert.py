from transformers import AutoTokenizer, TFDistilBertForQuestionAnswering, TrainingArguments, Trainer
from datasets import Dataset, load_metric
import json
import pandas as pd
import numpy as np
import tensorflow as tf
strategy = tf.distribute.MirroredStrategy()
# Check TensorFlow and Transformers versions
print(f"TensorFlow version: {tf.__version__}")

# Tokenizer and model initialization for DistilBERT
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased-distilled-squad")
with strategy.scope():
    model = TFDistilBertForQuestionAnswering.from_pretrained("distilbert-base-uncased-distilled-squad")

# Read context data and questions
context_data_files = [
    "../NLP Processing/after_scraping/Context-Data/fine-tuning-traveltriangle-goa.json",
    "../NLP Processing/after_scraping/Context-Data/fine-tuning-traveltriangle-japan.json",
    "../NLP Processing/after_scraping/Context-Data/fine-tuning-traveltriangle-vietnam.json"
]
dataset_files = [
    "../NLP Processing/after_scraping/four_qns/fine-tuning-dataset-traveltriangle-goa.json",
    "../NLP Processing/after_scraping/four_qns/fine-tuning-dataset-traveltriangle-japan.json",
    "../NLP Processing/after_scraping/four_qns/fine-tuning-dataset-traveltriangle-vietnam.json"
]

contexts = []
questions_dataset = []
answers_text = []
answers_start = []

# Load context data
context_data = {}
for i, file_path in enumerate(context_data_files):
    with open(file_path, "r") as file:
        context_data[i] = json.load(file)

# Define questions
questions = [
    "What is the name of the attraction?",
    "What is the location of the attraction?",
    "Describe the attraction in detail.",
    "What type of attraction is it? (e.g. historical, natural, amusement, beach)"
]

# Read dataset files
for i, file_path in enumerate(dataset_files):
    with open(file_path, "r") as file:
        dataset = json.load(file)
        for entry in dataset:
            id = entry['context_index']
            for question in questions:
                if question == entry['question'] and str(id) in context_data[i].keys():
                    contexts.append(context_data[i][str(id)])
                    questions_dataset.append(entry["question"])
                    answers_text.append(entry["answer"])
                    answers_start.append(0)

# Create DataFrame
df = pd.DataFrame({
    'context': contexts,
    'question': questions_dataset,
    'answers_text': answers_text,
    'answers_start': answers_start
})

# Tokenize the dataset
def tokenize_function(examples):
    return tokenizer(examples['context'], examples['question'], truncation=True)

# Map tokenization function to dataset
tokenized_datasets = Dataset.from_pandas(df).map(tokenize_function, batched=True)

# Split dataset into training and evaluation
tokenized_datasets = tokenized_datasets.train_test_split(test_size=0.1)

# Training arguments
training_args = TrainingArguments(
    output_dir='./results',
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=3,
    weight_decay=0.01,
)

# Load metric
metric = load_metric("squad")

# Compute metrics function
def compute_metrics(p):
    return metric.compute(predictions=np.argmax(p.predictions, axis=2), references=p.label_ids)


# Scope the Trainer within the strategy
with strategy.scope():
    # Initialize Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_datasets['train'],
        eval_dataset=tokenized_datasets['test'],
        tokenizer=tokenizer,
        compute_metrics=compute_metrics,
    )

    # Train the model
    trainer.train()

# Save the fine-tuned model
trainer.save_model("fine-tuned-distilbert-model")
