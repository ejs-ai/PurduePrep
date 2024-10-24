import requests
from io import BytesIO
from pathlib import Path
import PyPDF2
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
from collections import defaultdict

def get_websites(search_query):
    with open(get_webcrawl_functions_path() + '\\google_search_api.txt', 'r') as file:
        API_KEY = file.read().strip()
    SEARCH_ENGINE_ID = "7153013e76dda42f8"

    url = 'https://www.googleapis.com/customsearch/v1'
    params = {
        'q': search_query,
        'key': API_KEY,
        'cx': SEARCH_ENGINE_ID
    }

    response = requests.get(url, params = params )
    results = response.json()

    websites_list = []
    if 'items' in results:
        for link_number in range(10):
            websites_list.append(results['items'][link_number]['link'])
    else:
        print("No results found.")
        websites_list.append("-1")

    return websites_list

def open_url(url_to_scrape):
    try:
        url_content = requests.get(url=url_to_scrape, headers={'User-Agent': "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"}, timeout=10)
        if not url_content.ok:
            print("Could not read content at: " + url_to_scrape)
            url_content = -1
        return url_content
    
    except requests.exceptions.Timeout:
        print(f"Timeout occurred while trying to retrieve {url_to_scrape}. Skipping.")
        return -1 # Skip this URL if it times out
    
    except requests.RequestException as e:
        print(f"Failed to retrieve {url_to_scrape}: {e}")
        return  -1 # Handle other request exceptions

def get_content_from_pdf_link(url):
    pdf_content = open_url(url)
    
    if pdf_content == -1:
        return False
    
    pdf_reader = PyPDF2.PdfReader(BytesIO(pdf_content.content))
    pdf_text = ""
    
    for page_num in range(len(pdf_reader.pages)):
        pdf_text += pdf_reader.pages[page_num].extract_text()
    
    return pdf_text

def get_webcrawl_functions_path():
    current_dir = Path(__file__).resolve()
    for parent in current_dir.parents:
        if parent.name == 'PurduePrep':
            purdue_prep_dir = parent
            break
    else:
        raise FileNotFoundError("Could not locate the 'PurduePrep' directory")
    webcrawl_functions_path = purdue_prep_dir / 'webcrawl'
    return str(webcrawl_functions_path)

def contains_question_patterns(text):
    if type(text) is str:
        lines = text.split("\n")
        question_patterns = sum(1 for line in lines if re.match(r"^\s*(\(?[a-dA-D][\.\)]\)?)", line.strip()))
        return question_patterns

def crawl(url, depth, keywords, visited = None, page_scores = None):
    if visited is None:
        visited = set()
    if page_scores is None:
        page_scores = defaultdict(int)

    if depth == 0 or url in visited:
        return
    print(f"Crawling: {url}")
    visited.add(url)

    ## Fetch PDF content
    if url.lower().endswith('.pdf'):
        pdf_text = get_content_from_pdf_link(url)
        if pdf_text:
            page_scores[url] = contains_question_patterns(pdf_text)

    ## If not PDF, keep looking for a DARN PDF
    else:
        http_request_response = open_url(url)
        if http_request_response == -1:
            return
        
        # Parse html
        soup = BeautifulSoup(http_request_response.text, 'html.parser')
        page_text = soup.get_text()
        
        # Find all the links on the page and crawl them
        links = soup.find_all('a', href=True)
        for link in links:
            next_url = urljoin(url, link['href'])
            if next_url not in visited and re.match(r'^https?://', next_url):
                crawl(next_url, depth - 1, keywords, visited, page_scores)

    return page_scores

def init_gather_websites(keywords_str):
    max_depth = 1
    websites_list = get_websites(f"{keywords_str} past exam midterm final site:.edu")
    all_page_scores = defaultdict(int)
    return websites_list, max_depth, all_page_scores

def crawl_websites(keywords, websites_list, max_depth, all_page_scores):
    for website in websites_list:
        page_scores = crawl(website, max_depth, keywords)
        if page_scores:
            all_page_scores.update(page_scores)

    return sorted(all_page_scores.items(), key=lambda x: x[1], reverse=True)[:10]