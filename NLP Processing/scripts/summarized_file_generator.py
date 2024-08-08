import os
import json


def return_output():
    files = os.listdir("../after_scraping/Context-Data/Muthuraj Dataset")

    for file in files:
        data = json.load(
            open(f"../after_scraping/Context-Data/Muthuraj Dataset/{file}", "r")
        )
        write_file = open(
            f"../after_scraping/Manual Summarized/Muthuraj Dataset/{file}", "w"
        )

        json_data = {}
        for id, context in data.items():
            d = {"context": context, "summary": ""}
            json_data[id] = d

        json.dump(json_data, write_file, indent=4)


return_output()
