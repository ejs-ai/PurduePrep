# Classes:
# Page {url, body(extracted info from scrape)}
# Question {url from page, question body}

from PurduePrep.webcrawl.webcrawl_functions import get_content_from_pdf_link, init_gather_websites, crawl_websites
from PurduePrep.webcrawl.page import Page
from PurduePrep.webcrawl.query_build import build_query

# Step 0: Initialize the website?
# This is handled in app.py

# Step 1: Retrieve input from the user (text, pdf, or image). App.py handles processing of the input type and calls this function with a string
    

# UI handler ---(input)---> Input handler
# Step 2: Input handler processes input and formats as we need it


# Input handler ---(string)---> Query builder
# Step 3: Query builder processes all user's gibberish, extracts relevant info, forms query string


# Query builder ---(query string)---> Web crawler
# Step 4: Web crawler uses the query string to produce a list of relevant websites

    #from Seth: replace this with actual query builder 
keywords = ['cryptography', 'key', 'decryption', 'algorithm', 'encryption', 'secret', 'used', 'ciphertext', 'classical', 'plaintext']
search_query = f"{' '.join(keywords)} past exam midterm final site:.edu"

# Web crawler ---(relevant sites list)---> Scraper
# Step 6: Web scraper extracts information from websites
websites_list, max_depth, all_page_scores = init_gather_websites(search_query)
sorted_relevant_urls = crawl_websites(search_query, websites_list, max_depth, all_page_scores)

for url, score in sorted_relevant_urls:
    pdf_text = get_content_from_pdf_link(url)
    page_content = Page(url, pdf_text)

# Web scraper ---(extracted text)---> Question ID
# Step 7: Use NLP to identify questions
    # from Seth: use page_content.body and page_content.url


# Question ID ---(question objects)---> Relevance checker
# Step 8: Question objects go to relevance checker to be evaluated for content

# Relevance checker ---(list of question objects)---> Output handler
# Step 9: Output handler loops through list of question objects and packages to the website

# this is hard coded for now but will later be from our processing
# questions needs to be a global variable so app.py can import it
def get_questions():
    questions = [
        ("What is the capital of France?", "https://en.wikipedia.org/wiki/Paris"),
        ("What is 2 + 2?", "https://en.wikipedia.org/wiki/Addition"),
        ("Which planet is known as the Red Planet?", "https://en.wikipedia.org/wiki/Mars"),
    ]
    return questions

# Output handler ---(output)---> Website

def PurduePrepBackend(input_str):
    if input_str:
        print(input_str)
        query_string = build_query(input_str)
    else:
        print("No input text available")
        exit
    questions = get_questions()
    return questions