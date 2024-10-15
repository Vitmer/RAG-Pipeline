import json  # For loading and saving JSON files
import os  # For checking file existence
from sklearn.feature_extraction.text import TfidfVectorizer
import faiss
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Function to vectorize paragraphs using TF-IDF
def vectorize_paragraphs(paragraphs):
    # Initialize TfidfVectorizer with parameters to exclude too frequent or too rare words
    vectorizer = TfidfVectorizer(max_df=0.85, min_df=2)
    # Fit and transform the paragraphs into vectors
    vectors = vectorizer.fit_transform(paragraphs)
    return vectors, vectorizer

# Function to remove similar sentences based on cosine similarity
def remove_similar_sentences(sentences, threshold=0.8, length_diff=0.2):
    unique_sentences = []
    # Vectorize the sentences for similarity comparison
    vectors, _ = vectorize_paragraphs(sentences)
    
    for i, sentence in enumerate(sentences):
        is_unique = True
        for j in range(i):
            # Calculate the cosine similarity between sentences
            sim_score = cosine_similarity(vectors[i], vectors[j])[0][0]
            # Check if similarity exceeds the threshold and if the length difference is small
            if sim_score > threshold and abs(len(sentence) - len(sentences[j])) / len(sentences[j]) < length_diff:
                is_unique = False
                break
        if is_unique:
            unique_sentences.append(sentence)
    
    return unique_sentences

# Function to search for a query in the vectorized data
def search_query(query, vectorizer, index, paragraphs, top_k=3):
    # Transform the query into a vector
    query_vector = vectorizer.transform([query]).toarray()
    # Search for the top-K most similar vectors in the index
    D, I = index.search(query_vector, top_k)
    results = [paragraphs[i] for i in I[0]]
    
    # Remove similar sentences from the results
    filtered_results = remove_similar_sentences(results)
    return filtered_results

# Function to load cleaned data from a JSON file
def load_data_from_json(json_filename):
    if os.path.exists(json_filename):
        with open(json_filename, 'r', encoding='utf-8') as json_file:
            return json.load(json_file)
    else:
        raise FileNotFoundError(f"File {json_filename} not found")

# Main program execution
if __name__ == "__main__":
    # Load cleaned data
    cleaned_json_filename = "cleaned_texts.json"  # Path to the loaded file
    cleaned_texts = load_data_from_json(cleaned_json_filename)

    # Collect all paragraphs for vectorization
    all_paragraphs = []
    for doc in cleaned_texts.values():
        all_paragraphs.extend(doc.values())

    # Vectorize all paragraphs
    vectors, vectorizer = vectorize_paragraphs(all_paragraphs)

    # Create a FAISS index for fast search
    dimension = vectors.shape[1]
    index = faiss.IndexFlatL2(dimension)  # Using L2 metric for indexing
    index.add(vectors.toarray())

    # Optionally, save the index for future use
    faiss.write_index(index, "vector_index.faiss")
    print("Index saved in 'vector_index.faiss'")

    # Questions in German
    questions = [
        "Wie hoch ist die Grundzulage?", 
        "Wie werden Versorgungsleistungen aus einer Direktzusage oder einer Unterstützungskasse steuerlich behandelt?", 
        "Wie werden Leistungen aus einer Direktversicherung, Pensionskasse oder einem Pensionsfonds in der Auszahlungsphase besteuert?"
    ]

    # Retrieve and display relevant sentences for each question
    for question in questions:
        results = search_query(question, vectorizer, index, all_paragraphs, top_k=3)
        print(f"\nQuestion: {question}")
        print("Relevant sentences:")
        for result in results:
            print(result)