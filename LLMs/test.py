# Use a pipeline as a high-level helper
from transformers import pipeline

pipe = pipeline("text2text-generation", model="NoelTiju/t5-small-finetuned-attraction")

input_texts = [
    "summarize: Chapora Fort: For Selfie Lovers. Popular for its history, the Chapora Fort is one of the prime tourist attractions of Goa. It gained prominence after the Bollywood movie *Dil Chahta Hai* was shot here. Perched on a prominent position, one can get sweeping views of all directions from here. This is one of the prime sightseeing places in Goa where you can enjoy a wonderful sight of the sea from up above. Location: Chapora Fort Rd, Chapora, Goa. What’s Special? *Dil Chahta Hai* was shot here! The fort offers picturesque views of the Chapora River uniting with the waters of the Arabian Sea. Built By: Adil Shah of Bijapur. Nearby Attractions: Vagator Beach and Anjuna Beach. How To Reach: The fort is well-connected and can be easily reached by road. Entry Fee: No entry fee"
]

# Generate text for each input
for text in input_texts:
    output = pipe(text)
    print(f"Input: {text}")
    print(f"Output: {output[0]['generated_text']}\n")
