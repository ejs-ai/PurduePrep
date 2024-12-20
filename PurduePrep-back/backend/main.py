# Classes:
# Page {url, body(extracted info from scrape)}
# Question {url from page, question body}
import spacy
from nltk.corpus import stopwords
from transformers import BertTokenizer
from scrape.bert_functions import BERTClassifier, predict_question
from torch import load, device
import time
from pathlib import Path

print('loading spacy model...')
start = time.time()
nlp = spacy.load("en_core_web_md")
end = time.time()
print('loaded spacy model in ' + str(end - start) + ' seconds.')

print('loading stopwords...')
start = time.time()
stop_words = list(stopwords.words('english'))
end = time.time()
print('loaded stopwords in ' + str(end - start) + ' seconds.')


print('loading bert model...')
current_dir = Path(__file__).resolve()
for parent in current_dir.parents:
        if parent.name == 'backend':
            backend_dir = parent
            break
model_path = backend_dir / 'scrape' / 'bert_classifier.pth'
start = time.time()
bert_model_name = 'bert-base-uncased'
num_classes = 2
dev = device("cpu")
tokenizer = BertTokenizer.from_pretrained(bert_model_name)
question_id = BERTClassifier(bert_model_name, num_classes)
question_id.load_state_dict(load(model_path, weights_only=True, map_location=dev))
end = time.time()
print('loaded bert model in ' + str(end - start) + ' seconds.')

from webcrawl.webcrawl_functions import init_gather_websites, crawl_websites, process_url
from webcrawl.query_build import build_query
import concurrent.futures

CRAWL_DEPTH = 4

def main(user_input, num_questions):
    start_time = time.time()
    # Step 0: Initialize the website?
    # This is handled in app.py
    # Step 1: Retrieve input from the user (text, pdf, or image). App.py handles processing of the input type and calls this function with a string

    # UI handler ---(input)---> Input handler
    # Step 2: Input handler processes input and formats as we need it
    if not user_input:
        print("No input text available")
        return 

    # Input handler ---(string)---> Query builder
    # Step 3: Query builder processes all user's gibberish, extracts relevant info, forms query string
    query_string = build_query(user_input)
    print(f'QUERY STRING: {query_string}')
    print('\n')
    # Query builder ---(query string)---> Web crawler
    # Step 4: Web crawler uses the query string to produce a list of relevant websites
    websites_list, all_page_scores = init_gather_websites(query_string)
    sorted_relevant_urls = crawl_websites(query_string, websites_list, CRAWL_DEPTH, all_page_scores)

    # Web crawler ---(relevant sites list)---> Scraper
    # Step 5: Web scraper extracts information from websites
    ### THREAD ###
    questions = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(process_url, url, score): url for url, score in sorted_relevant_urls}
        for future in concurrent.futures.as_completed(futures):
            url = futures[future]
            try:
                questions.extend(future.result())
            except Exception as e:
                print(f"Error processing {url}: {e}")

    # Question ID ---(question objects)---> Relevance checker
    # Step 8: Question objects go to relevance checker to be evaluated for content
    #questions = rank_questions(nlp, user_input, questions)

        # Relevance checker ---(list of question objects)---> Output handler
        # Step 9: Output handler loops through list of question objects and packages to the website
        # Output handler ---(output)---> Website
        # app.py is the output handler, which includes the calling function for main
    end_time = time.time()
    print(f'\n Total runtime: {end_time - start_time} seconds!')
    return questions[:num_questions]