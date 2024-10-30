import spacy
import nltk
import pickle
import os

# Download the spacy model
def download_spacy_model():
    spacy.cli.download("en_core_web_sm")

# # Download nltk model
# def download_nltk_resources():
#     nltk.download('stopwords')  

# Load the pickle file
def load_pickle_model():
    model_path = "questionid.pkl"
    if os.path.exists(model_path):
        with open(model_path, "rb") as file:
            model = pickle.load(file)
        return model
    else:
        raise FileNotFoundError("Pickle model file not found.")

# Run all downloads
if __name__ == "__main__":
    download_spacy_model()
    # download_nltk_resources()
    load_pickle_model()
