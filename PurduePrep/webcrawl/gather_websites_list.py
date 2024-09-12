import requests                 #Will allow us to access websites
from bs4 import BeautifulSoup   #Webcrawling
import pandas as pd             #pandas

# URLs
url_test = 'http://quotes.toscrape.com'
url_list = [url_test]
pages = []
soup_list = []
not_last_page = True

#1: Pull the requests

# We want the headers to determine the User Agent
# The user agent will identify the search devices which will better the search. We should webscrape for this too
# headers_MS = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
headers_crawler = {'User-Agent': "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"}

current_page = requests.get(url=URL, headers=headers_crawler)
print('current_page:')

soup = BeautifulSoup(r.content, 'html5lib')