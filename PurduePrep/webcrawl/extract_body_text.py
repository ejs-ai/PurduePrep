import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader, PdfWriter
import re
import sys
import os
from webcrawl_functions import open_url, url_screen_for_pdf

ece404_url = 'https://weeklyjoys.wordpress.com/wp-content/uploads/2021/10/ece404_e1_sp2021.pdf'
pdf_name, out_text_file, pdf_hex_content = url_screen_for_pdf(ece404_url)

#TEMPORARILY DOWNLOAD THE PDF SO THAT WE CAN READ IT
with open("temp.pdf", "wb") as pdf_file:
    pdf_file.write(pdf_hex_content.content)

pdf_reader = PdfReader("temp.pdf")

# WRITE TO TEXT FILE
with open(out_text_file, "w", encoding="utf-8") as output_file_with_content:
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        page_text = page.extract_text()
        output_file_with_content.write(page_text)

os.remove("temp.pdf")