import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
import nltk

# Ensure NLTK data is downloaded
nltk.download('punkt')
nltk.download('stopwords')

def preprocess_text(text):
    """
    Preprocesses text by tokenizing, converting to lowercase, removing punctuation and stopwords.

    Parameters:
        text (str): The input text to preprocess.

    Returns:
        str: The preprocessed text.
    """
    # Tokenize and convert to lowercase
    tokens = word_tokenize(text.lower())

    # Remove punctuation
    table = str.maketrans('', '', string.punctuation)
    tokens = [word.translate(table) for word in tokens]

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]

    return " ".join(tokens)


def load_data_from_json(json_file):
    """
    Loads captions from a JSON file.

    Parameters:
        json_file (str): Path to the JSON file containing captions.

    Returns:
        list: List of dictionaries containing video IDs and captions.
    """
    with open(json_file, 'r') as f:
        data = json.load(f)
    return data


def search_videos(json_file, search_query, threshold=0.1):
    """
    Searches for videos based on a query using TF-IDF and cosine similarity.

    Parameters:
        json_file (str): Path to the JSON file containing captions.
        search_query (str): The search query string.
        threshold (float): Minimum similarity score to consider a result (default is 0.1).

    Returns:
        list: List of video IDs that match the query.
    """
    # Load captions from JSON file
    data = load_data_from_json(json_file)

    # Preprocess captions
    preprocessed_captions = []
    for item in data:
        concatenated_captions = " ".join(item["captions"])
        preprocessed_captions.append(preprocess_text(concatenated_captions))

    # Initialize TF-IDF vectorizer
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(preprocessed_captions)

    # Preprocess the search query
    preprocessed_query = preprocess_text(search_query)
    query_vector = vectorizer.transform([preprocessed_query])

    # Compute cosine similarity
    similarities = cosine_similarity(query_vector, tfidf_matrix)

    # Retrieve video IDs with similarity above the threshold
    relevant_videos = []
    for idx, similarity_score in enumerate(similarities[0]):
        if similarity_score >= threshold:
            relevant_videos.append(data[idx]["video_id"])

    return relevant_videos


if __name__ == "__main__":
    # Example usage
    captions_file = "output.json"
    query = "cat playing in the park"

    try:
        results = search_videos(captions_file, query)
        print("Videos matching the query:")
        for video_id in results:
            print(video_id)
    except FileNotFoundError:
        print(f"Error: {captions_file} not found. Ensure the JSON file exists.")
    except Exception as e:
        print(f"An error occurred: {e}")
