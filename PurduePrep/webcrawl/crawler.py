from pypdf import PdfReader
import os
from webcrawl.webcrawl_functions import get_content_from_pdf_link
from webcrawl.page import Page

### TEST URL --> WILL BE REPLACED ONCE WE HAVE GATHER_WEBSITES WORKING
ece404_url = 'https://weeklyjoys.wordpress.com/wp-content/uploads/2021/10/ece404_e1_sp2021.pdf'

### Extract text from URL
pdf_text = get_content_from_pdf_link(ece404_url)
page_content = Page(ece404_url, pdf_text)
