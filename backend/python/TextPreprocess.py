import re
import time
from nltk.corpus import stopwords

stop_words = set(stopwords.words("english"))

def preprocessText(text):
    """
        Preprocess text by:
        - Converting to lowercase
        - Removing punctuation
        - Tokenizing into words using regex
        - Removing stopwords
    """

    if not isinstance(text, str):
        return []  # Return empty list for invalid or missing text
    text = text.lower()  # Convert to lowercase
    text = re.sub(r'[^\s\da-zA-Z]', ' ', text) # Remove punctuation
    words = re.findall(r'\b\w+\b', text)  # Tokenize using regex
    words = [word for word in words if word not in stop_words]
    return words