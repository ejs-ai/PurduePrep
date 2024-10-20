# Classes:
# Page {url, body(extracted info from scrape)}
# Question {url from page, question body}

from PurduePrep.webcrawl.webcrawl_functions import get_content_from_pdf_link, init_gather_websites, crawl_websites
from PurduePrep.webcrawl.page import Page
from PurduePrep.webcrawl.query_build import build_query
from PurduePrep.scrape.find_questions import find_questions

def main(user_input):
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

    # Query builder ---(query string)---> Web crawler
    # Step 4: Web crawler uses the query string to produce a list of relevant websites
    websites_list, max_depth, all_page_scores = init_gather_websites(query_string)
    sorted_relevant_urls = crawl_websites(query_string, websites_list, max_depth, all_page_scores)

    # Web crawler ---(relevant sites list)---> Scraper
    # Step 5: Web scraper extracts information from websites
    questions = []
    for url, score in sorted_relevant_urls:
        pdf_text = get_content_from_pdf_link(url)
        page_content = Page(url, pdf_text)

        # Web scraper ---(extracted text)---> Question ID
        # Step 7: Use NLP to identify questions
        page_questions = find_questions(page_content)
        for question in page_questions:
            questions.append((question, url))

        # Question ID ---(question objects)---> Relevance checker
        # Step 8: Question objects go to relevance checker to be evaluated for content

        # Question ID ---(question objects)---> Relevance checker
        # Step 8: Question objects go to relevance checker to be evaluated for content

        # Relevance checker ---(list of question objects)---> Output handler
        # Step 9: Output handler loops through list of question objects and packages to the website

        # Output handler ---(output)---> Website

    return questions