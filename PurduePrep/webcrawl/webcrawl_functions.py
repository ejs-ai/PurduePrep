import requests
from io import BytesIO
from pathlib import Path
import PyPDF2

def open_url(url_to_scrape):
    #Case 1: Links to PDFs
    url_content = requests.get(url=url_to_scrape, headers={'User-Agent': "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"})
    if not url_content.ok:
        print("Could not read content at: " + url_to_scrape)
        url_content = -1
    return url_content

def get_content_from_pdf_link(url):
    pdf_content = open_url(url)
    
    if pdf_content == -1:
        return None, None
    
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