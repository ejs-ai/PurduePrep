from PurduePrep.webcrawl.webcrawl_functions import get_content_from_pdf_link, init_gather_websites, crawl_websites
from PurduePrep.webcrawl.page import Page
import time

CRAWL_DEPTH = 2

#keywords = ['vector', 'row space', 'matrix', 'basis', 'diagonalizable']
#keywords = ['cryptography', 'key', 'decryption', 'algorithm', 'encryption', 'secret', 'used', 'ciphertext', 'classical', 'plaintext']
#keywords = ['derivative', 'integral', 'integrate', 'chain', 'differentiate']
keywords = ['binary', 'tree', 'bubble sort', 'sort', 'complexity']
#keywords = ['discrete', 'math', 'mathematics']

search_query = f"{' '.join(keywords)} past exam midterm final site:.edu"

start_time = time.time()
# Gather relevant websites from query
websites_list, all_page_scores = init_gather_websites(search_query)
sorted_relevant_urls = crawl_websites(search_query, websites_list, CRAWL_DEPTH, all_page_scores)
print(sorted_relevant_urls)

crawl_time = time.time()
print(f"Total time to gather relevant sites: {crawl_time - start_time} seconds")

# Extract page content
for url, score in sorted_relevant_urls:
    relevant_character_indices = score[1]
    pdf_text, _ = get_content_from_pdf_link(url)
    if pdf_text:
        page_content = Page(url, pdf_text, relevant_character_indices)

end_time = time.time()
print(f"Total time to pull web content: {end_time - crawl_time} seconds")