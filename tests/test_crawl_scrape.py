from PurduePrep.webcrawl.webcrawl_functions import get_content_from_pdf_link, init_gather_websites, crawl_websites
from PurduePrep.webcrawl.page import Page
from PurduePrep.scrape.find_questions import find_questions
import time

CRAWL_DEPTH = 2

# Input from Emma
#keywords = ['cryptography', 'key', 'decryption', 'algorithm', 'encryption', 'secret', 'used', 'ciphertext', 'classical', 'plaintext']
#keywords = ['vector', 'row space', 'matrix', 'basis', 'diagonalizable']
keywords = ['derivative', 'integral', 'integrate', 'chain', 'differentiate']

search_query = f"{' '.join(keywords)} past exam midterm final site:.edu"

start_time = time.time()
websites_list, all_page_scores = init_gather_websites(search_query)

for web_pairs in websites_list:
    print(f'crawling from roots {web_pairs}')
    sorted_relevant_urls = crawl_websites(search_query, web_pairs, CRAWL_DEPTH, all_page_scores)
    print('finished crawl')
    crawl_time = time.time()
    
    # Extract page content 
    questions = []
    for url, score in sorted_relevant_urls:
        pdf_text, _ = get_content_from_pdf_link(url)
        page_content = Page(url, pdf_text, score[1])
        questions.extend(find_questions(page_content))

    print(questions)