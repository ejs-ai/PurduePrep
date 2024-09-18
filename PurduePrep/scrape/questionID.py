import os
import json
import nltk

def getquestions():
    # data location
    question_dir = 'STEMquestions/data/'

    # list to store the extracted questions
    questions = []

    # Walk through the base directory and its subfolders
    for root, dirs, files in os.walk(question_dir):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                
                # Open and read the JSON file
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    
                    # Extract the 'Original question' and add to the list
                    if "Original question" in data:
                        questions.append(data["Original question"])

    return questions

def getsentences():
    # Ensure you have the Punkt tokenizer models for sentence splitting (if not done already)
    # nltk.download('punkt_tab')

    from nltk.tokenize import sent_tokenize

    # Define the base directory where your text files are located
    base_dir = 'STEMtext/'

    # Initialize a list to store the sentences
    sentences = []

    # Number of sentences to extract
    num_sentences = 667
    sentences_per_chunk = 3  # Number of sentences per chunk (adjust as needed)

    # Loop through the text files in the directory
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                
                # Open and read the content of the text file
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    # Tokenize the content into sentences
                    sentences = sent_tokenize(content)
                    
                    # Group the sentences into sentences of a few sentences each
                    for i in range(0, len(sentences), sentences_per_chunk):
                        chunk = " ".join(sentences[i:i + sentences_per_chunk])
                        sentences.append(chunk)
                        
                        # Stop if we have collected enough sentences
                        if len(sentences) >= num_sentences:
                            break

                # Stop outer loop if we have enough sentences
                if len(sentences) >= num_sentences:
                    break

    return sentences

def main():
    questions = getquestions()
    sentences = getsentences()
    

if __name__ == "__main__":
    main()