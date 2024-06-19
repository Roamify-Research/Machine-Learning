from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline
import torch


model_name = "deepset/roberta-base-squad2"

model = AutoModelForQuestionAnswering.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

nlp = pipeline('question-answering', model=model_name, tokenizer=model_name)

def return_output(question, context):
    QA_input = {'question': question, 'context': context}
    inputs = tokenizer(QA_input['question'], QA_input['context'], return_tensors='pt')
    outputs = model(**inputs)

    start_scores = outputs.start_logits
    end_scores = outputs.end_logits

    answer_start = torch.argmax(start_scores)
    answer_end = torch.argmax(end_scores) + 1
    answer = tokenizer.decode(inputs['input_ids'][0][answer_start:answer_end])
    return answer

