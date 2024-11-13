from PurduePrep.webcrawl.webcrawl_functions import get_content_from_pdf_link, init_gather_websites, crawl_websites
from PurduePrep.webcrawl.page import Page
from PurduePrep.scrape.find_questions import find_questions
import time

CRAWL_DEPTH = 2

# Input from Emma
keywords = ['cryptography', 'key', 'decryption', 'algorithm', 'encryption', 'secret', 'used', 'ciphertext', 'classical', 'plaintext']
#keywords = ['vector', 'row space', 'matrix', 'basis', 'diagonalizable']
#keywords = ['derivative', 'integral', 'integrate', 'chain', 'differentiate']
#keywords = ['binary', 'tree', 'bubble sort', 'sort', 'complexity']

search_query = f"{' '.join(keywords)} past exam midterm final site:.edu"

start_time = time.time()
websites_list, all_page_scores = init_gather_websites(search_query)
sorted_relevant_urls = crawl_websites(search_query, websites_list, CRAWL_DEPTH, all_page_scores)
print('')
print(sorted_relevant_urls)

# Extract page content 
questions = []
for url, score in sorted_relevant_urls:
    pdf_text, _ = get_content_from_pdf_link(url)
    if pdf_text:
        page_content = Page(url, pdf_text, score[1])
        start_nlp_time = time.time()
        questions.extend(find_questions(page_content))

for question in questions:
    print(question)
    print("\n")