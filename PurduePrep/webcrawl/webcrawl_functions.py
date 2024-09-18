import requests
from pathlib import Path


def open_url(url_to_scrape):
    url_content = requests.get(url=url_to_scrape, headers={'User-Agent': "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"})
    if not url_content.ok:
        print("Could not read content at: "+url_to_scrape)
        url_content = -1
    return url_content


def url_screen_for_pdf(url):
    pdf_name = url.split("/")[-1]
    out_text_file = pdf_name.replace('.pdf', '.txt')
    pdf_hex_content = open_url(url)
    return pdf_name, out_text_file, pdf_hex_content


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


def write_out_text_file(file_to_write, pdf_content):
    path_to_file = get_webcrawl_functions_path()
    with open(path_to_file + "\\" + file_to_write, "w", encoding="utf-8") as output_file_with_content:
        for page_num in range(len(pdf_content.pages)):
            page = pdf_content.pages[page_num]
            page_text = page.extract_text()
            output_file_with_content.write(page_text)
