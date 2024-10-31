import requests
# from webcrawl.webcrawl_functions import get_content_from_pdf_link
# from welcrawl.webcrawl_functions import get_content_from_pdf_link, get_websites, init_gather_websites, crawl
# from webcrawl.page import Page

from PurduePrep.webcrawl.webcrawl_functions import get_content_from_pdf_link, init_gather_websites, crawl_websites
from PurduePrep.webcrawl.page import Page
import time

# Input from Emma
keywords = ['cryptography', 'key', 'decryption', 'algorithm', 'encryption', 'secret', 'used', 'ciphertext', 'classical', 'plaintext']
search_query = f"{' '.join(keywords)} past exam midterm final site:.edu"

start_time = time.time()
# Gather relevant websites from query
websites_list, max_depth, all_page_scores = init_gather_websites(search_query)

sorted_relevant_urls = crawl_websites(search_query, websites_list, max_depth, all_page_scores)

crawl_time = time.time()
print(f"Total gather_time-start_time: {crawl_time - start_time} seconds")

# Extract page content
for url, score in sorted_relevant_urls:
    pdf_text = get_content_from_pdf_link(url)
    page_content = Page(url, pdf_text)
end_time = time.time()
print(f"Total end_time-craw_time: {end_time - crawl_time} seconds")



