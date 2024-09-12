import requests                 #Will allow us to access websites
from bs4 import BeautifulSoup   #Webcrawling
import pandas as pd             #pandas

# URLs
url_test = 'https://quotes.toscrape.com/'
url_list = [url_test]
pages = []
soup_list = []
not_last_page = True

search_device = {'User-Agent': "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"}
current_page = requests.get(url=url_test, headers=search_device)
current_page_html_content = BeautifulSoup(current_page.content, 'html5lib')

print('soup: ')
print(current_page_html_content)