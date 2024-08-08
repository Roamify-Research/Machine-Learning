# **Roamify: Roaming Redefined**

## _Changing the Way World Travels_

Welcome to the official repository of Roamify Machine Learning research. This repository contains the code and documentation for our innovative approach to providing personalized travel recommendations using advanced machine learning techniques.

## Table of Contents

- [Introduction](#introduction)
- [Directory Structure](#directory-structure)
- [Research Objectives](#research-objectives)
- [Methodology](#methodology)
  - [Data Collection & Preprocessing](#data-collection--preprocessing)
  - [NLP Overview](#nlp-overview)
  - [LLM's Overview](#llms-overview)
- [Evaluation Metrics](#evaluation-metrics)
- [Results](#results)
- [Citing This Work](#citing-this-work)
- [Acknowledgements](#acknowledgements)

## Introduction

Roamify aims to revolutionize the travel experience by leveraging the power of machine learning to provide personalized recommendations. Our research explores various machine learning models and techniques to enhance the accuracy and relevance of travel suggestions, ensuring travelers receive the most tailored and insightful recommendations.

## Directory Structure

```plaintext
Machine Learning/
│
├── LLMs/
│   ├── FlanT5_finetuning_summarization.ipynb
│   ├── llama_3_fine_tuning_summarization.ipynb
│   ├── simple_transformers_tuning_qa_model.ipynb
│   ├── t5_summarization.ipynb
│   └── test.py
│
├── NLP Processing/
│   ├── after_scraping/
│   │   ├── Context-Data/
│   │   │   └── fine-tuning-<city>_traveltriangle.json
│   │   ├── Fine-Tuning-Datasets/
│   │   │   ├── files/
│   │   │   │   └── <city>-out.json
│   │   │   ├── fine-tuning-dataset-qa.json
│   │   │   ├── tuning_summarized_data.json
│   │   │   ├── context_data.json
│   │   │   └── summarized_questions.json
│   │   ├── four_qns/
│   │   │   └── fine-tuning-dataset-traveltriangle-<city>.json
│   │   ├── Initial/
│   │   │   └── <city>_traveltriangle_after.txt
│   │   ├── Manual Summarized/
│   │   │   └── summarized-fine-tuning-<city>_traveltriangle.json
│   │   ├── Previous Questions Datasets/
│   │   │   └── fine-tuning-dataset-traveltriangle-<city>.json
│   │   └── Summarized Llama/
│   │       └── summarized-fine-tuning-<city>_traveltriangle.json
│   ├── helper_files/
│   │   ├── lang_test.py
│   │   ├── make-summarized-dataset.py
│   │   ├── openai_populate.py
│   │   └── process_pipeline.py
│   ├── scripts/
│   │   ├── itinerary_scraping.py
│   │   ├── llama_pipeline.py
│   │   ├── roberta_pipeline.py
│   │   ├── spacy_transformers.py
│   │   └── summarized_file_generator.py
│   └── webscraped_data/
│       └── <city>_traveltriangle.txt
│
├── Recommender System/
│   ├── datasets/
│   │   ├── individual_countries/
│   │   │   └── <country>.csv
│   │   ├── predictions/
│   │   │   └── predicted_user_ratings.csv
│   │   ├── dataset_helper.py
│   │   ├── final_attractions.csv
│   │   ├── first-user-study-ratings.csv
│   │   └── user_features.csv
│   ├── deploy/
│   │   ├── recommendations_streamlit.py
│   │   └── streamlit_app.py
│   ├── google_maps/
│   │   ├── maps_api.py
│   │   └── nlp.py
│   ├── helper_files/
│   │   ├── db_test.py
│   │   ├── filter.py
│   │   └── prepare_dataset.py
│   └── models/
│       ├── Collaborative Filtering/
│       │   ├── collaborative_filtering.ipynb
│       │   └── recommendations.py
│       ├── Kmeans_Clustering.ipynb
│       └── Self_Organizing_Maps.ipynb
│
├── .pre-commit-config.yaml
├── .gitignore
├── dataset.md
├── LICENSE
├── README.md
└── requirements.txt
```

## Research Objectives

1. **Finding the Most Suitable LLM for Summarizing and Cleaning Web Scrapes**: Identify and evaluate various large language models (LLMs) to determine which model performs best in summarizing and cleaning web-scraped data, ensuring the highest accuracy and relevance of travel information.
2. **Determining the Impact of User Preferences on Itinerary Planning**: Investigate how user preferences for different types of attractions (e.g., historical, amusement, natural) influence the planning of itineraries, and develop models that can effectively incorporate these preferences to provide more relevant and personalized travel suggestions.

## Methodology

### Data Collection & Preprocessing

The data used for fine-tuning the models was collected from various online travel platforms, focusing on popular tourist destinations. The datasets included detailed descriptions, locations, types of attractions, and user reviews. The data was pre-processed to remove any noise and irrelevant information, ensuring high-quality input for the models.

For more detailed information about the datasets, please refer to our [Dataset Documentation](dataset.md).

We created two datasets for fine-tuning, each with a different purpose:

1. **Summarization Dataset**: This dataset was utilized to refine the LLaMA-3 and Flan-T5 models. It comprised two components: context and summary. The context pertained to the data obtained by web scraping, while the summary was a concise translation of the text that was both grammatically correct and succinct.

   **Sample data entry:**

   - **Context**:
     ```
     Bangalore Palace Winit Deshpande for Wikimedia Commons Built by Chamaraja Wodeyar in the year 1887, Bangalore Palace is an inspired design by England’s Windsor Castle and is one of the best tourist places in Bangalore. The evocative palace comprises fortified arches, towers, architecture, and green lawns along with sophisticated wood carvings in the interior. It is where the royal family still resides at present. This architectural creation is nothing less than an epitome. The palace has earned foundations that have been attributed to the Wodeyars of Mysore. Location: Vasanth Nagar, Bengaluru. Timings: Sunday to Monday from 10:00 AM to 5:00 PM. Entry Fee: INR 230 for Indians, INR 460 for foreigners. Must Read: New Year Party In Bangalore.
     ```
   - **Summary**:
     ```
     Bangalore Palace, built by Chamaraja Wodeyar in 1887, is inspired by England’s Windsor Castle and features fortified arches, towers, green lawns, and intricate wood carvings. Located in Vasanth Nagar, it remains a residence for the royal family and is a prime tourist attraction in Bangalore, open daily with an entry fee.
     ```

2. **Question-Answering Dataset**: This dataset was utilized to refine question-answering models, specifically BERT, DistilBERT, and RoBERTa. It included six specific questions designed to extract significant insights from the processed scraped data.

**Data Preparation Steps**:

- **Tokenization**: Text data was tokenized using the respective model tokenizers.
- **Cleaning**: Non-ASCII characters, HTML tags, and extra whitespace were removed.
- **Normalization**: Text was converted to lowercase, and punctuation was standardized.
- **Splitting**: The data was split into training and evaluation sets with a typical ratio of 80:20.

These preprocessing steps ensured that the data fed into the models was clean, well-organized, and suitable for training and evaluation, ultimately contributing to the models' performance in generating and fine-tuning travel itineraries.

### NLP Overview

To clear junk from the scraped data, our algorithm involved several stages:

1. **Using spaCy**: We utilized the `en_core_web_lg` model from the spaCy library to preprocess data, incorporating tasks like tokenization, part-of-speech tagging, named entity recognition, and dependency parsing. This phase efficiently cleansed and organized the data.

2. **Extracting Sentences**: The processed text was divided into separate sentences using spaCy, facilitating the identification and analysis of distinct pieces of information.

3. **Recognizing Patterns**: Sentences were segmented into individual words using the `word_tokenize` feature to identify patterns, specifically a consecutive series of integers. This pattern helped in isolating detailed descriptions of attractions.

4. **Data Processing and Structuring**: Text between identified patterns was refined to eliminate interference. The sanitized data was stored in a dictionary format, with keys as attraction names and values as their descriptions, ensuring organized and error-free data ready for analysis and model training.

5. **Handling Large Sections of Text**: Initially, processing large sections of web pages led to fragmented summaries. To improve this, we divided the web page into smaller chunks, each representing an individual attraction. This chunking method allowed models to generate coherent and concise summaries, capturing essential details more effectively, and enhancing the overall summarization process.

By following these procedures, we ensured that the data was thoroughly cleaned, well-organized, and ready for further analysis and model development.

### LLM's overview

#### Question Answering Models

Initially, we utilized various models for the question answering task to address inquiries pertaining to the context presented in the dataset. The main goal was to obtain important insights and precise replies from the processed scraped data. The specific models employed were:

- **BERT**: Known for its bidirectional training approach, which considers context from both directions.
- **RoBERTa**: An optimized version of BERT with improved training methods.
- **DistilBERT**: A distilled version of BERT that retains most of its performance while being smaller and faster.

These models were fine-tuned to handle questions such as identifying the name, location, detailed description, and type of attraction (e.g., historical, natural, amusement, beach).

#### Text-to-Text Generation Models

For the text-to-text generation task, specifically summarization, we optimized the following models to produce precise and succinct summaries of the provided text:

- **T5**: A versatile model that treats all NLP tasks as a text-to-text problem, allowing it to generate coherent and contextually accurate text.
- **Llama-3**: A large language model with sophisticated language understanding and generation capabilities, particularly effective for detailed and personalized text generation.

The approach involved compressing the material while preserving its significance and pertinence, essential for producing succinct descriptions of tourist destinations from the massive web-scraped data. This improved the comprehension and utility of the gathered data, increasing its accessibility and providing users with more interesting insights.

#### Itinerary Generation Model

For generating detailed and personalized travel itineraries, we used the **Ollama** model, employing Llama 3.1. Ollama was leveraged to process the summarized and cleaned data from the initial NLP processing phase. This model provided high accuracy and coherence in the generated itineraries, ensuring users receive well-structured travel plans that cater to their preferences and needs.

By combining these models, we achieved significant improvements in the accuracy and relevance of travel recommendations, showcasing the potential of advanced machine learning techniques in the travel recommendation domain.

## Evaluation Metrics

#### Question Answering Models

We evaluated the performance of our question answering models, BERT, DistilBERT, and RoBERTa, by measuring their training and evaluation loss across three epochs. The results are summarized in the tables below:

**Epoch 1**
| Model | Train Loss | Eval Loss |
|-------------|-------------|-----------|
| DistilBERT | 1.9549 | -2.0043 |
| RoBERTa | 1.6825 | -2.6740 |
| BERT | 6.3657 | 0.2002 |

**Epoch 2**
| Model | Train Loss | Eval Loss |
|-------------|-------------|-----------|
| DistilBERT | 2.6524 | -4.5488 |
| RoBERTa | 0.7623 | -4.2015 |
| BERT | 6.2629 | 0.0262 |

**Epoch 3**
| Model | Train Loss | Eval Loss |
|-------------|-------------|-----------|
| DistilBERT | 1.2276 | -5.2743 |
| RoBERTa | 0.7708 | -4.4541 |
| BERT | 5.6464 | 0.0586 |

These metrics indicate the training and evaluation performance of the models, highlighting areas for further improvement.

#### Text-to-Text Generation Models

For the text-to-text generation task, specifically summarization, we evaluated T5 and Llama-3 models using the following sample context and their respective outputs:

**Context:**
Cubbon Park Sarangib for Pixabay Situated over a sprawling 300 acres of land the park was constructed by Richard Sankey This massive green park along with lawns deserves a special mention Offering statues of famous personalities the park is one among the popular places to visit in Bangalore with friends Location Kas- turba Road Behind High Court of Karnataka Ambed- kar Veedhi Sampangi Rama Nagara BangaloreTimings Open on all daysEntry Fee No entry fee Suggested Read Resorts Near Bangalore

**T5 Output:**
Cubbon Park, a sprawling 300 acres of land, is a popular place to visit in Bangalore with friends. Offering statues of famous personalities, it is a popular place to visit with friends.

**Llama-3 Output:**
The park was constructed by Richard Sankey. This massive green park, along with lawns, deserves a special mention. Offering statues of famous personalities, the park is one among the popular places to visit in Bangalore with friends. Location: Kasturba Road, Behind High Court of Karnataka.

## Results

The objective of this research was to find the most suitable combination of LLMs for generating and fine-tuning itineraries. We prepared two datasets for fine-tuning: a question-answering dataset and a summarization dataset.

Initially, we trained question-answering models to extract relevant details from attraction descriptions, but these models did not perform satisfactorily. Consequently, we shifted our focus to text-to-text generation models, specifically LLaMA-3 and T5, to address the summarization task.

Our experiments revealed that while T5 performs summarization tasks faster than LLaMA-3, it is sometimes less elaborate. Given our use case's priority on speed, we selected T5 for the summarization task. The combination of T5 for initial summarization and LLaMA for elaboration proved to be the most effective. For efficient itinerary generation, we employed Ollama, built on LLaMA 3.1.

Overall, the T5-LLaMA combination ensured both speed and detail in summarization, while Ollama provided accurate and coherent travel itineraries.

## Citing This Work

If you use our code or models in your research, please cite our paper:

<!-- ```
@inproceedings{roamifyredefined2024,
  title={Roamify: Roaming Redefined},
  author={Vikranth Udandarao, Harsh Mistry, Muthuraj Vairamuthu, Noel Tiju and Armaan Singh},
  booktitle={Proceedings of the Top Conference on AI and Travel Technology},
  year={2024},
  organization={IIIT Delhi, Computer Science Engineering Dept}
}
``` -->

```
@inproceedings{roamifyredefined2024,
  title={Roamify: Roaming Redefined},
  author={Vikranth Udandarao, Harsh Mistry, Muthuraj Vairamuthu, Noel Tiju, Armaan Singh, and Dhruv Kumar},
  year={2024},
  organization={IIIT Delhi, Computer Science Engineering Dept}
}
```

## Acknowledgements

We would like to thank our academic institution, [IIIT Delhi](https://iiitd.ac.in/), and our guide, [Dr. Dhruv Kumar](https://kudhru.github.io/) for their support and contributions to this research.
