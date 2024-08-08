from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline


model_name = "deepset/roberta-base-squad2"

model = AutoModelForQuestionAnswering.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

nlp = pipeline("question-answering", model=model_name)


def return_output(question, context):
    answer = nlp(question=question, context=context)
    return answer["answer"]
