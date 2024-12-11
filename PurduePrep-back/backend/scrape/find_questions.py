import re
from scrape.split_page import split_page
from main import dev, tokenizer, question_id
from scrape.bert_functions import predict_question

MAX_TEXT_LENGTH = 1000000

### TEST URLS
# ece404_url = 'https://weeklyjoys.wordpress.com/wp-content/uploads/2021/10/ece404_e1_sp2021.pdf'
# powerpoint_url = 'https://engineering.purdue.edu/kak/compsec/NewLectures/Lecture13.pdf'

def predict_sentences(sentences):
    output = []
    for input in sentences:
        pred = predict_question(input, question_id, tokenizer, dev)
        output.append(pred)
    return output

def regex_filter(text):
    pattern = r'(^\d+\.|^[a-zA-Z]\.\s*[\s\S]*?(?:\?|\.|\:)|(\b(What|Why|How|Explain|Describe|Define|List|Which|When|Where|Calculate|Compare|Discuss|Name|Identify|Solve|Determine|Recover|Convert|Compute)\b[\s\S]*?[?.:])|(\b(Show|Formulate|Demonstrate|Design|Construct|Prove|Provide|Find|Use)\b[\s\S]*?(work|equation|steps|solution|method|equations|process|procedure)[\s\S]*?[.:])|(\•\s*[\s\S]+))'
    return bool(re.search(pattern, text))

def find_questions(page):
    questions = []
    if((len(page.body) > MAX_TEXT_LENGTH)): # max length
        return None
    
    clusters, lengths = split_page(page.body)
    clusters = list(filter(regex_filter, clusters))
    preds = predict_sentences(clusters)
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