import requests
from io import BytesIO
from pathlib import Path
import PyPDF2
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
from collections import defaultdict
import time
import concurrent.futures

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
    num_links = len(results['items'])

    websites_list = []
    if 'items' in results:
        for link_number in range(num_links):
            websites_list.append(results['items'][link_number]['link'])
    else:
        #print("No results found.")
        websites_list.append("-1")
    
    # return websites_list

    web_pairs_list = []
    for web_pair_idx in range(0, len(websites_list), 2):
        web_pair_instance = []
        web_pair_0 = websites_list[web_pair_idx]
        web_pair_1 = websites_list[web_pair_idx+1] if web_pair_idx + 1 < len(websites_list) else None
        web_pair_instance.append(web_pair_0)
        web_pair_instance.append(web_pair_1)
        web_pairs_list.append(web_pair_instance)

    return web_pairs_list

def open_url(url_to_scrape):
    try:
        url_content = requests.get(url=url_to_scrape, headers={'User-Agent': "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"}, timeout=3)
        if not url_content.ok:
            #print("Could not read content at: " + url_to_scrape)
            url_content = -1
        return url_content
    
    except requests.exceptions.Timeout:
        #print(f"Timeout occurred while trying to retrieve {url_to_scrape}. Skipping.")
        return -1 # Skip this URL if it times out
    
    except requests.RequestException as e:
        #print(f"Failed to retrieve {url_to_scrape}: {e}")
        return  -1 # Handle other request exceptions

def get_content_from_pdf_link(url):
    title_page_multiplier = 1
    pdf_content = open_url(url)
    
    if pdf_content == -1:
        return False, title_page_multiplier
    
    pdf_reader = PyPDF2.PdfReader(BytesIO(pdf_content.content))
    pdf_text = ""

    if len(pdf_reader.pages) > 20:
        return False, title_page_multiplier

    if ("exam" or "Exam" or "midterm" or "Midterm" or "final" or "Final") in pdf_reader.pages[0].extract_text():
        title_page_multiplier = 1.5
    
    for page_num in range(len(pdf_reader.pages)):
        pdf_text += pdf_reader.pages[page_num].extract_text()
    
    return pdf_text, title_page_multiplier

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
    
def check_if_exam(text):
    lines = text.split("\n")
    question_patterns = 0
    pattern_indices = []

    for i, line in enumerate(lines):
        if re.match(r"^\s*(\(?[a-dA-D][\.\)]\)?)", line.strip()):
            question_patterns += 1
            pattern_indices.append(i)  # Store the index where pattern was found
    
    return question_patterns, pattern_indices

def crawl(url, depth, keywords, visited = None, page_scores = None):
    BLACKLIST_PATTERNS = ['lecture', 'Lecture', 'lec' ,'Syllabus', 'syllabus', 'youtube']

    if visited is None:
        visited = set()
    if page_scores is None:
        page_scores = defaultdict(lambda: (0, []))

    if depth == 0 or url in visited:
        return
    #print(f"Crawling: {url}")
    visited.add(url)

    if any(pattern in url.lower() for pattern in BLACKLIST_PATTERNS):
        #print(f"Skipping URL (blacklisted pattern): {url}")
        return
    
    ## Fetch PDF content
    if url.lower().endswith('.pdf'):
        #Open PDF and get its text
        pdf_text, title_page_multiplier = get_content_from_pdf_link(url)
        if pdf_text:
            score, pattern_indices = check_if_exam(pdf_text)
            page_scores[url] = (score *title_page_multiplier, pattern_indices)
            
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
    websites_list = get_websites(f"{keywords_str} past exam midterm final site:.edu")
    all_page_scores = defaultdict(int)
    return websites_list, all_page_scores

def crawl_websites(keywords, websites_list, max_depth, all_page_scores):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_website = {executor.submit(crawl, website, max_depth, keywords): website for website in websites_list}

        for future in concurrent.futures.as_completed(future_to_website):
            website = future_to_website[future]
            try:
                page_scores = future.result()
                if page_scores:
                    all_page_scores.update(page_scores)
            except Exception as e:
                print(f"{website} generated an exception: {e}")

    return sorted(all_page_scores.items(), key=lambda x: x[1], reverse=True)[:10]