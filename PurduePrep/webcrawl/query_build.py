# "text" argument is a string
# Use TFIDF to find the frequent keywords from input text
# Append google search commands to filter content
import urllib.parse
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.corpus import stopwords

# Function to extract keywords using TF-IDF
def extract_keywords(text, top_n=10):
    # Define stopwords
    nltk.download('stopwords')
    stop_words = list(stopwords.words('english'))
    
    # Use TF-IDF to extract keywords (no stopwords)
    vectorizer = TfidfVectorizer(stop_words=stop_words)
    tfidf_matrix = vectorizer.fit_transform([text])
    feature_names = vectorizer.get_feature_names_out()
    tfidf_scores = tfidf_matrix.toarray()[0]
    word_scores = dict(zip(feature_names, tfidf_scores))
    
    # Sort words by their TF-IDF score and select the top N keywords
    sorted_keywords = sorted(word_scores.items(), key=lambda x: x[1], reverse=True)
    top_keywords = [word for word, score in sorted_keywords[:top_n]]
    
    return top_keywords

def build_query(text):
    # Extract the list of keywords and append relevant exam related keywords
    keywords = extract_keywords(text)
    keywords.append('past')
    keywords.append('exam')
    keywords.append('midterm')
    keywords.append('final')
    
    # Construct the search query string with Google search operator to limit results to .edu domains
    query = ' '.join(keywords) + ' site:.edu'
    
    # Encode query to be URL-safe, build google search url
    # encoded_query = urllib.parse.quote(query)
    #search_url = f"https://www.google.com/search?q={encoded_query}"
    
    return query