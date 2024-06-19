from transformers import pipeline

pipe = pipeline("text-generation", model="meta-llama/Meta-Llama-3-8B-Instruct")

def return_output(input):

    input = "Summarize: " + input
    messages = [
    {"role": "user", "content": input},
]

    response = pipe(messages)
    return response[0]["generated_responses"]