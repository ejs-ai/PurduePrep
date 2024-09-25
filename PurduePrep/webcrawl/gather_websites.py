import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
from collections import defaultdict

# Function to count relevant keywords on a page
def count_relevant_keywords(text, keywords):
    text = text.lower()
    return sum(text.count(keyword.lower()) for keyword in keywords)

# Function to check if a page has any relevant keywords
def is_relevant_page(url, text, keywords):
    return any(keyword.lower() in text.lower() for keyword in keywords)

def crawl(url, depth, keywords, visited=None, page_scores=None):
    if visited is None:
        visited = set()
    if page_scores is None:
        page_scores = defaultdict(int)

    if depth == 0 or url in visited:
        return

    print(f"Crawling: {url}")
    visited.add(url)

    # Fetch the page content
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to retrieve {url}: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Check if the current page has relevant content
    page_text = soup.get_text()
    if is_relevant_page(url, page_text, keywords):
        page_scores[url] = count_relevant_keywords(page_text, keywords)
    
    # Find all the links on the page and crawl them
    links = soup.find_all('a', href=True)
    for link in links:
        next_url = urljoin(url, link['href'])
        if next_url not in visited and re.match(r'^https?://', next_url):
            crawl(next_url, depth - 1, keywords, visited, page_scores)

    return page_scores

# Starting point (seed URL) for crawling
seed_urls = [
    "https://weeklyjoys.wordpress.com/",  # Replace with websites known to host exam problems
]

if __name__ == "__main__":
    # Set maximum depth to control the crawl
    max_depth = 5
    
    # Relevant keywords for identifying useful pages
    keywords = ['ECE', 'ece', '2k1', 'circuit', 'fundamentals', '2k2', 'transistor', 'voltage', 'resistance']
    
    # Dictionary to store the keyword count for each relevant URL
    all_page_scores = defaultdict(int)
    
    # Crawl each seed URL
    for seed_url in seed_urls:
        page_scores = crawl(seed_url, max_depth, keywords)
        if page_scores:
            all_page_scores.update(page_scores)
    
    # Sort URLs by the number of relevant keywords (in descending order) and take the top 10
    sorted_relevant_urls = sorted(all_page_scores.items(), key=lambda x: x[1], reverse=True)[:10]
    
    # Print the top 10 URLs
    print("Top 10 Relevant URLs with practice exam problems:")
    for idx, (site, score) in enumerate(sorted_relevant_urls, start=1):
        print(f"{idx}. {site} (Keyword matches: {score})")