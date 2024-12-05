import re
from pathlib import Path
from scrape.split_page import split_page
from webcrawl.page import Page
from transformers import BertTokenizer
from scrape.bert_functions import BERTClassifier, predict_question
from torch import load, device

MAX_TEXT_LENGTH = 1000000

### TEST URLS
# ece404_url = 'https://weeklyjoys.wordpress.com/wp-content/uploads/2021/10/ece404_e1_sp2021.pdf'
# powerpoint_url = 'https://engineering.purdue.edu/kak/compsec/NewLectures/Lecture13.pdf'

def get_scrape_path():
    current_dir = Path(__file__).resolve()
    for parent in current_dir.parents:
        if parent.name == 'backend':
            backend_dir = parent
            break
    else:
        raise FileNotFoundError("Could not locate the 'backend' directory")
    webcrawl_functions_path = backend_dir / 'scrape'
    return str(webcrawl_functions_path)

print("Loading BERT model")
bert_model_name = 'bert-base-uncased'
num_classes = 2
dev = device("cpu")
tokenizer = BertTokenizer.from_pretrained(bert_model_name)
question_id = BERTClassifier(bert_model_name, num_classes)
# path = get_scrape_path() + '/bert_classifier.pth'
# req = requests.get('https://www.dropbox.com/scl/fi/wdf2g7qrtjybqc47j4p9y/bert_classifier.pth?rlkey=y11v2o6wwpsj7rkravtt5gzg2&st=lev4pyed&dl=1')
# with open(path, "wb") as file:
#     file.write(req.content)
question_id.load_state_dict(load(get_scrape_path() + '/bert_classifier.pth', weights_only=True, map_location=dev))

def predict_sentences(sentences, model, tokenizer, dev):
    output = []
    for input in sentences:
        pred = predict_question(input, model, tokenizer, dev)
        output.append(pred)
    return output

def regex_filter(text):
    pattern = r'(^\d+\.|^[a-zA-Z]\.\s*[\s\S]*?(?:\?|\.|\:)|(\b(What|Why|How|Explain|Describe|Define|List|Which|When|Where|Calculate|Compare|Discuss|Name|Identify|Solve|Determine|Recover|Convert|Compute)\b[\s\S]*?[?.:])|(\b(Show|Formulate|Demonstrate|Design|Construct|Prove|Provide|Find|Use)\b[\s\S]*?(work|equation|steps|solution|method|equations|process|procedure)[\s\S]*?[.:])|(\•\s*[\s\S]+))'
    return bool(re.search(pattern, text))

def find_questions(page):
    # question_id, tokenizer, dev = load_model() do on startup instead
    questions = []
    if((len(page.body) > MAX_TEXT_LENGTH)): # max length
        return None
    
    clusters, lengths = split_page(page.body)
    clusters = list(filter(regex_filter, clusters))
    preds = predict_sentences(clusters, question_id, tokenizer, dev)
    for index, sentence in enumerate(clusters):
        if preds[index] == 1:
            questions.append(sentence)
    return questions

# Testing
# if __name__ == '__main__':
#     input_list = Page(ece404_url, get_content_from_pdf_link(powerpoint_url))
#     questions = find_questions(input_list)
    # for i in questions:
    #     print(i + '\n\n')