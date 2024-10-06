import requests
# from webcrawl.webcrawl_functions import get_content_from_pdf_link
# from welcrawl.webcrawl_functions import get_content_from_pdf_link, get_websites, init_gather_websites, crawl
# from webcrawl.page import Page

from webcrawl_functions import get_content_from_pdf_link, init_gather_websites, crawl_websites
from page import Page

#Input from Emma
keywords = ['cryptography', 'key', 'decryption', 'algorithm', 'encryption', 'secret', 'used', 'ciphertext', 'classical', 'plaintext']

# Gather relevant websites from query
keywords_str, websites_list, max_depth, all_page_scores = init_gather_websites(keywords)
sorted_relevant_urls = crawl_websites(keywords_str, websites_list, max_depth, all_page_scores)

# Extract page content
for url, score in sorted_relevant_urls:
    pdf_text = get_content_from_pdf_link(url)
    page_content = Page(url, pdf_text)