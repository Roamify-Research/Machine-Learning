import json

context_data_files = [
    "../NLP Processing/after_scraping/Context-Data/fine-tuning-goa_traveltriangle.json",
    "../NLP Processing/after_scraping/Context-Data/fine-tuning-japan_traveltriangle.json",
    "../NLP Processing/after_scraping/Context-Data/fine-tuning-vietnam_traveltriangle.json",
]
dataset_files = [
    "../NLP Processing/after_scraping/four_qns/fine-tuning-dataset-traveltriangle-goa.json",
    "../NLP Processing/after_scraping/four_qns/fine-tuning-dataset-traveltriangle-japan.json",
    "../NLP Processing/after_scraping/four_qns/fine-tuning-dataset-traveltriangle-vietnam.json",
]

context_data = {}
for i, file_path in enumerate(context_data_files):
    with open(file_path, "r") as file:
        context_data[i] = json.load(file)
questions = [
    "What is the name of the attraction?",
    "What is the location of the attraction?",
    "Describe the attraction in detail.",
    "What type of attraction is it? (e.g. historical, natural, amusement, beach)",
]

training_data = []
for i, file_path in enumerate(dataset_files):
    with open(file_path, "r") as file:
        dataset = json.load(file)
        for entry in dataset:
            if (
                entry["question"]
                != "What type of attraction is it? (e.g. historical, natural, amusement, beach)"
            ):
                unique_id = str(i) + str(entry["context_index"])
                ans = {
                    "context": context_data[i][str(entry["context_index"])],
                    "qas": [
                        {
                            "id": unique_id,
                            "is_impossible": False,
                            "question": entry["question"],
                            "answers": [{"text": entry["answer"], "answer_start": 0}],
                        }
                    ],
                }
                training_data.append(ans)
                print(ans)


with open("fine-tuning-dataset-qa.json", "w") as file:
    json.dump(training_data, file, indent=4)
