from PurduePrep.webcrawl.webcrawl_functions import get_content_from_pdf_link, init_gather_websites, crawl_websites
from PurduePrep.webcrawl.page import Page
import time

CRAWL_DEPTH = 2

# Input from Emma
#keywords = ['cryptography', 'key', 'decryption', 'algorithm', 'encryption', 'secret', 'used', 'ciphertext', 'classical', 'plaintext']
#keywords = ['derivative', 'integral', 'integrate', 'chain', 'differentiate']
keywords = ['vector', 'row space', 'matrix', 'basis', 'diagonalizable']
search_query = f"{' '.join(keywords)} past exam midterm final site:.edu"

start_time = time.time()
# Gather relevant websites from query
websites_list, all_page_scores = init_gather_websites(search_query)

for web_pairs in websites_list:
    crawl_time = time.time()

    sorted_relevant_urls = crawl_websites(search_query, web_pairs, CRAWL_DEPTH, all_page_scores)

    end_time = time.time()
    print(f"Total time to crawl pair: {end_time - crawl_time} seconds")
    print('')
    
    print(sorted_relevant_urls)

    # Extract page content
    for url, score in sorted_relevant_urls:
        relevant_character_indices = score[1]
        pdf_text, _ = get_content_from_pdf_link(url)
        page_content = Page(url, pdf_text, relevant_character_indices)

