from nltk.tokenize import sent_tokenize
import requests
from io import BytesIO
from pathlib import Path
import PyPDF2
import xgboost as xgb
import pickle
from sentence_transformers import SentenceTransformer


class Page:
    def __init__(self, url, body):
        self.url = url
        self.body = body

    def info(self):
        print("URL: " + self.url)
        print("\n")
        print("BODY: " + self.body)

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

def vector_encode(strings):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    return model.encode(strings)

def predict_sentences(sentences, model):
    sentences = vector_encode(sentences)
    return model.predict(sentences)

### TEST URL --> WILL BE REPLACED ONCE WE HAVE GATHER_WEBSITES WORKING
ece404_url = 'https://weeklyjoys.wordpress.com/wp-content/uploads/2021/10/ece404_e1_sp2021.pdf'

### Extract text from URL
pdf_text = get_content_from_pdf_link(ece404_url)
page_content = Page(ece404_url, pdf_text)

with open('questionid.pkl', 'rb') as f:
    question_id = pickle.load(f)

sentences = sent_tokenize(page_content.body)
preds = predict_sentences(sentences, question_id)
print(preds)
for index, sentence in enumerate(sentences):
    if preds[index] == 0:
        print("Found " + str(index) + ":\n" + sentence + '\n\n')