import requests
from bs4 import BeautifulSoup
import pandas as pd
from pypdf import PdfReader, PdfWriter
import re
import sys

def open_url(url_to_scrape):
    url_content = requests.get(url = url_to_scrape, headers = {'User-Agent': "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"})
    if not url_content.ok:
        sys.exit("Could not read content at: "+url_to_scrape)
    return url_content

def url_screen_for_pdf(url):
    pdf_name = url.split("/")[-1]
    out_text_file = pdf_name.replace('.pdf', '.txt')
    pdf_hex_content = open_url(url)
    return pdf_name, out_text_file, pdf_hex_content

def write_out_text_file(file_to_write, pdf_content):
    with open(file_to_write, "w", encoding="utf-8") as output_file_with_content:
        for page_num in range(len(pdf_content.pages)):
            page = pdf_content.pages[page_num]
            page_text = page.extract_text()
            output_file_with_content.write(page_text)