from bs4 import BeautifulSoup
from pypdf import PdfReader, PdfWriter
import sys
import os
from webcrawl_functions import open_url, url_screen_for_pdf, write_out_text_file, get_webcrawl_functions_path

ece404_url = 'https://weeklyjoys.wordpress.com/wp-content/uploads/2021/10/ece404_e1_sp2021.pdf'
pdf_name, out_text_file, pdf_hex_content = url_screen_for_pdf(ece404_url)

with open("temp.pdf", "wb") as pdf_file:
    pdf_file.write(pdf_hex_content.content)

pdf_reader = PdfReader("temp.pdf")
write_out_text_file(out_text_file, pdf_reader)

os.remove("temp.pdf")