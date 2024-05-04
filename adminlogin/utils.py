import os
import re
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np 
from sklearn.cluster import DBSCAN


def preproc(txt):

    txt =  re.sub('[^a-zA-Z]', ' ', txt)  
    tokens = word_tokenize(txt.lower())
    # Remove stop words
    words = [token for token in tokens if tokens not in stopwords.words('english')]
    
    return ' '.join(words)

def create_tfidf_vectors(docs):
    
    docs = [preproc(doc) for doc in docs]
    return TfidfVectorizer().fit_transform(docs).toarray()


def find_similarity(doc_filename_pairs):

    plagiarism_results = set() 

    for student_a_file, student_a_vec in doc_filename_pairs:
        remaining_pairs = doc_filename_pairs.copy()
        current_index = remaining_pairs.index((student_a_file, student_a_vec))
        del remaining_pairs[current_index]
        for student_b_file, student_b_vec in remaining_pairs:
            similarity_score = cosine_similarity([student_a_vec, student_b_vec])[0][1]
            sorted_filenames = (student_a_file, student_b_file)
            plagiarism_result = (sorted_filenames[0], sorted_filenames[1], similarity_score)
            plagiarism_results.add(plagiarism_result)
    return plagiarism_results



def create_similarity_matrix(plagiarism_results, files):

    num_files = len(files)
    similarity_matrix = np.zeros((num_files, num_files))
    file_index = {file: index for index, file in enumerate(files)}
    
    for result in plagiarism_results:
        file1, file2, similarity_score = result
        index1 = file_index[file1]
        index2 = file_index[file2]
        similarity_matrix[index1][index2] = similarity_score
        similarity_matrix[index2][index1] = similarity_score 
    return similarity_matrix
