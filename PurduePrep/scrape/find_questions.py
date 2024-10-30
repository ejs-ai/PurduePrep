import re
from PurduePrep.scrape.split_page import split_page
import pickle
from sentence_transformers import SentenceTransformer
from PurduePrep.webcrawl.page import Page
import os

MAX_TEXT_LENGTH = 1000000

### TEST URL --> WILL BE REPLACED ONCE WE HAVE GATHER_WEBSITES WORKING
ece404_url = 'https://weeklyjoys.wordpress.com/wp-content/uploads/2021/10/ece404_e1_sp2021.pdf'
powerpoint_url = 'https://engineering.purdue.edu/kak/compsec/NewLectures/Lecture13.pdf'

def vector_encode(strings):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    return model.encode(strings)

def predict_sentences(sentences, model):
    sentences = vector_encode(sentences)
    return model.predict(sentences)

def regex_filter(text):
    pattern = r'(^\d+\.|^[a-zA-Z]\.\s*[\s\S]*?(?:\?|\.|\:)|(\b(What|Why|How|Explain|Describe|Define|List|Which|When|Where|Calculate|Compare|Discuss|Name|Identify|Solve|Determine|Recover|Convert|Compute)\b[\s\S]*?[?.:])|(\b(Show|Formulate|Demonstrate|Design|Construct|Prove|Provide|Find|Use)\b[\s\S]*?(work|equation|steps|solution|method|equations|process|procedure)[\s\S]*?[.:])|(\•\s*[\s\S]+))'
    return bool(re.search(pattern, text))



def find_questions(page):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    pkl_path = os.path.join(script_dir, 'questionid.pkl')
    with open(pkl_path, 'rb') as f:
        question_id = pickle.load(f)
 
    questions = []
    
    if((len(page.body) > MAX_TEXT_LENGTH)): # max length
        return None
    
    clusters, lengths = split_page(page.body)
    clusters = list(filter(regex_filter, clusters))
    preds = predict_sentences(clusters, question_id)
    for index, sentence in enumerate(clusters):
        if preds[index] == 1:
            questions.append(sentence)
    return questions