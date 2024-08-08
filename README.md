# **Roamify: Roaming Redefined**
## _Changing the Way World Travels_

Welcome to the official repository of Roamify Machine Learning research. This repository contains the code and documentation for our innovative approach to providing personalized travel recommendations using advanced machine learning techniques.

<!-- Our work is set to be published in top-tier conferences, showcasing the cutting-edge methodologies and applications in the field of AI-driven travel technology. -->

## Table of Contents

- [Introduction](#introduction)
- [Directory Structure](#introduction)
- [Research Objectives](#directory-structure)
- [Methodology](#methodology)
  - [Data Collection](#data-collection)
  - [Data Preprocessing](#data-preprocessing)
  - [Model Development](#model-development)
  - [Evaluation Metrics](#evaluation-metrics)
- [Results](#results)
- [Usage](#usage)
  - [Installation](#installation)
  - [Running the Models](#running-the-models)
- [Contributors](#contributors)
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
│   ├── models/
│   │   ├── Collaborative Filtering/
│   │   │   ├── collaborative_filtering.ipynb
│   │   │   └── recommendations.py
│   │   ├── Kmeans_Clustering.ipynb
│   │   └── Self_Organizing_Maps.ipynb
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

## Research Objectives

The primary objectives of this research are:
1. To develop robust machine learning models that can predict user preferences and recommend travel destinations and activities.
2. To integrate multi-modal data (text, images, and user profiles) to enhance recommendation accuracy.
3. To evaluate the performance of different models and techniques, identifying the most effective approaches for travel recommendations.

## Methodology

### Data Collection

We collected a diverse dataset comprising travel-related information from various sources, including:
- User reviews and ratings from travel websites
- Metadata about travel destinations and attractions
- User profiles and preferences

### Data Preprocessing

The preprocessing pipeline involves:
- Cleaning and normalizing text data
- Extracting relevant features from images and text
- Encoding user preferences and historical data

### Model Development

We explored several machine learning models, including:
- **Neural Collaborative Filtering**: For predicting user-item interactions.
- **Convolutional Neural Networks (CNNs)**: For analyzing and extracting features from travel images.
- **Recurrent Neural Networks (RNNs)**: For modeling sequential data and user reviews.
- **Hybrid Models**: Combining collaborative filtering and content-based methods.

### Evaluation Metrics

The performance of our models was evaluated using metrics such as:
- Precision, Recall, and F1-Score
- Mean Absolute Error (MAE) and Root Mean Squared Error (RMSE)
- Mean Reciprocal Rank (MRR) and Normalized Discounted Cumulative Gain (NDCG)

## Results

Our models demonstrated significant improvements in recommendation accuracy, with the hybrid approach outperforming traditional methods. The integration of multi-modal data proved to be highly effective, showcasing the potential of advanced machine learning techniques in the travel recommendation domain.

## Usage

### Installation

To install the necessary dependencies, run:

```bash
pip install -r requirements.txt
```

### Running the Models

To train and evaluate the models, use the following command:

```bash
python main.py
```

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