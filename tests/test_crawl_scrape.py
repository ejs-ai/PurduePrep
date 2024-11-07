from PurduePrep.webcrawl.webcrawl_functions import get_content_from_pdf_link, init_gather_websites, crawl_websites
from PurduePrep.webcrawl.page import Page
from PurduePrep.webcrawl.crawler import crawl_websites
from PurduePrep.scrape.find_questions import find_questions

CRAWL_DEPTH = 2

keywords = ['vector', 'row space', 'matrix', 'basis', 'diagonalizable']
search_query = f"{' '.join(keywords)} past exam midterm final site:.edu"

websites_list, all_page_scores = init_gather_websites(search_query)
sorted_relevant_urls = crawl_websites(search_query, websites_list, CRAWL_DEPTH, all_page_scores)

# Extract page content
questions = []
for url, score in sorted_relevant_urls:
    pdf_text, _ = get_content_from_pdf_link(url)
    page_content = Page(url, pdf_text, score[1])
    questions.extend(find_questions(page_content))

print(questions)