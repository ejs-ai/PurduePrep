import time
t1 = time.time()
import re
from purdueprep.scrape.split_page import split_page
import xgboost as xgb
import pickle
from sentence_transformers import SentenceTransformer

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

with open('questionid.pkl', 'rb') as f:
    question_id = pickle.load(f)

num_qs = 0
num_pt = 0

clusters, lengths = split_page(ece404_url)
unfiltered = len(clusters)
clusters = list(filter(regex_filter, clusters))
filtered = len(clusters)
num_pt += unfiltered - filtered

preds = predict_sentences(clusters, question_id)

for index, sentence in enumerate(clusters):
    if preds[index] == 1:
        num_qs += 1
        #print("Question " + str(num_qs) + ":\n" + sentence + '\n\n')
    else:
        num_pt += 1
        #print("Plaintext " + str(num_pt) + ":\n" + sentence + '\n\n')

print(str(num_pt) + " blocks of plaintext and " + str(num_qs) + " questions found.")

t2 = time.time()
print("took " + str(t2 - t1) + " seconds.")