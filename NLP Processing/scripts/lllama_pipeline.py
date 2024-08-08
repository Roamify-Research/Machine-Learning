import transformers
import torch
import json

model_id = "meta-llama/Meta-Llama-3-8B-Instruct"
hf_token = "your_huggingface_token"  # Your Hugging Face token

# Load the text generation pipeline with specified settings
pipe = transformers.pipeline(
    "text-generation",
    model=model_id,
    tokenizer=model_id,
    model_kwargs={"torch_dtype": torch.bfloat16},
    device_map="cuda:0",  # Let the library handle device mapping automatically
    token=hf_token,  # Ensure authentication for loading the model
)


def return_output(input):
    input = "Summarize: " + input
    messages = [
        {"role": "user", "content": input},
    ]

    response = pipe(messages)
    return response


files = [
    "fine-tuning-bangalore_traveltriangle.json",
    "fine-tuning-chennai_traveltriangle.json",
    "fine-tuning-dehradun_traveltriangle.json",
    "fine-tuning-goa_traveltriangle.json",
    "fine-tuning-hyderabad_traveltriangle.json",
    "fine-tuning-italy_traveltriangle.json",
    "fine-tuning-japan_traveltriangle.json",
    "fine-tuning-kerala_traveltriangle.json",
    "fine-tuning-lakshwadeep_traveltriangle.json",
    "fine-tuning-mysore_traveltriangle.json",
    "fine-tuning-pune_traveltriangle.json",
    "fine-tuning-tn_traveltriangle.json",
    "fine-tuning-vietnam_traveltriangle.json",
]


for i in files:
    data = json.load(open(f"../after_scraping/Context-Data/{i}", "r"))
    write_file = open(f"../after_scraping/Summarized-LLAMA/summarized-{i}", "w")
    json_data = {}
    for id, context in data.items():
        output = return_output(context)
        print(output)
        d = {"context": context, "summary": output}
        json_data[id] = d

    json.dump(json_data, write_file, indent=4)
