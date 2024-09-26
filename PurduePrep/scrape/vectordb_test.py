# AI Assisted

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import time

# Load pre-trained sentence transformer model
t1 = time.time()
model = SentenceTransformer('all-MiniLM-L6-v2')
t2 = time.time()
# Define the sentences
sentences = [
    "When in the Course of human events, it becomes necessary for one people to dissolve the political bands which have connected them with another, and to assume among the powers of the earth, the separate and equal station to which the Laws of Nature and of Nature's God entitle them, a decent respect to the opinions of mankind requires that they should declare the causes which impel them to the separation.",
    "The upper downtown area had no power, and it was just warm enough that people had their windows open to get some reprieve from the heat.  That made it easier.  I sent some bugs into every open window, using the roaches and flies that were already present when possible. How many people did I have to reach?  The buildings here were anywhere from six to twelve floors, and there were anywhere from one to six apartments to a floor.  Less than half of the apartments were occupied following the evacuations, but it still made for hundreds of people on each city block. I didn’t slow my pace as I worked.  Bugs swept over the surfaces of rooms for any smooth surfaces that indicated glass or mirrors.  I checked bedside tables for eyeglasses and alarm clocks.  If I found glass, a bed positioned too close to a window or mirror, something potentially dangerous on the bedside table or if there were enough attack bugs around, I attacked the residents.  The bugs bit, stung, or momentarily smothered them, covering their noses and mouths, waking them.",
    "Four score and seven years ago our fathers brought forth, upon this continent, a new nation, conceived in liberty, and dedicated to the proposition that all men are created equal. Now we are engaged in a great civil war, testing whether that nation, or any nation so conceived, and so dedicated, can long endure. We are met on a great battle field of that war. We come to dedicate a portion of it, as a final resting place for those who died here, that the nation might live. This we may, in all propriety do. But, in a larger sense, we can not dedicate we can not consecrate we can not hallow, this ground The brave men, living and dead, who struggled here, have hallowed it, far above our poor power to add or detract. The world will little note, nor long remember what we say here; while it can never forget what they did here. It is rather for us, the living, we here be dedicated to the great task remaining before us that, from these honored dead we take increased devotion to that cause for which they here, gave the last full measure of devotion that we here highly resolve these dead shall not have died in vain; that the nation, shall have a new birth of freedom, and that government of the people, by the people, for the people, shall not perish from the earth.",
]

# Encode the sentences into vectors
t3 = time.time()
sentence_embeddings = model.encode(sentences)
t4 = time.time()
# Check the shape of the embeddings (number of sentences, embedding dimension)
print(f"Embeddings shape: {sentence_embeddings.shape}")

# Initialize FAISS index for L2 (Euclidean) similarity search
t5 = time.time()
d = sentence_embeddings.shape[1]  # Dimension of the embedding vectors
index = faiss.IndexFlatL2(d)      # L2 distance index
t6 = time.time()

# Convert embeddings to numpy array (FAISS works with NumPy)
sentence_embeddings_np = np.array(sentence_embeddings)

# Add vectors to FAISS index
index.add(sentence_embeddings_np)

# Now perform similarity search for the first sentence
query_embedding = sentence_embeddings_np[0].reshape(1, -1)  # Reshape as query for FAISS

# Perform search in FAISS: compare the first sentence against all sentences
D, I = index.search(query_embedding, k=3)  # k is the number of closest sentences to return

# Output the indices of the closest sentences (excluding the first sentence itself)
closest_sentence_index = I[0][1]  # The first result is the query itself, so take the second

# Print which sentence is the most similar
print(f"The most similar sentence to Sentence 1 is Sentence {closest_sentence_index + 1}.") 
# As expected, the Gettysburg address is more similar to the Declaration of Independance than a fantasy novel.

print(f"model load time: {t2 - t1}") # first load takes longer than subsequent with cached model (has to download from HF)
print(f"encode time: {t4 - t3}")
print(f"FAISS load time: {t6 - t5}")