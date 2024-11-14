import numpy as np
import spacy

# load spacy model
try:
    nlp = spacy.load("en_core_web_md")
except OSError:
    print("Model 'en_core_web_md' not found. Downloading it now...")
    spacy.cli.download("en_core_web_md")
    nlp = spacy.load("en_core_web_md")

def rank_questions(user_input, questions):
    user_input_vec = nlp(user_input)
    scores = []
    for question, url in questions:
        question_vec = nlp(question)
        scores.append(user_input_vec.similarity(question_vec))
    questions_sorted = [q for _, q in sorted(zip(scores, questions), reverse=True)]
    return questions_sorted

def filter_questions(user_input, questions, threshold=0.9):
    # Remove questions with a cosine similarity less than threshold (tweakable param)
    user_input_vec = nlp(user_input)
    questions_filtered = []
    for question, url in questions:
        question_vec = nlp(question)
        if (user_input_vec.similarity(question_vec) > threshold):
            questions_filtered.append((question, url))
    return questions_filtered

# def filter_faiss(user_input, questions, k=3):
#     question_vectors = [nlp(question).vector for question in questions]
#     question_matrix = np.array(question_vectors).astype('float32')

#     # Build a FAISS index
#     dimension = question_matrix.shape[1]  # Dimensionality of vectors
#     index = faiss.IndexFlatL2(dimension)  # Use L2 distance (Euclidean)
#     index.add(question_matrix)            # Add vectors to the index

#     user_input_vec = nlp(user_input).vector.reshape(1, -1).astype('float32')

#     _, indices = index.search(user_input_vec, k)
#     return [questions[i] for i in indices[0]]