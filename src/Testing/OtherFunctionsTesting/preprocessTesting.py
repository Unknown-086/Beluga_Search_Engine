import re
import time
from collections import defaultdict
from nltk import sent_tokenize
from nltk.tokenize import word_tokenize
from sympy import timed


def preprocessText(text):
    """
        Preprocess text by:
        - Converting to lowercase
        - Removing punctuation
        - Tokenizing into words using NLTK
    """

    if not isinstance(text, str):
        return []  # Return empty list for invalid or missing text
    text = text.lower()  # Convert to lowercase
    text = re.sub(r'[^\s\da-zA-Z]', ' ', text) # Remove punctuation
    return re.findall(r'\b\w+\b', text)  # Tokenize using regex


if __name__ == '__main__':
    text = ("https://appleinsider.com/articles/23/10/01/national-emergency-alert-test-will-affect-all-us-iphones-on-wednesday")
    # text = preprocessText(text)

    print(text)
    start = time.time()
    text = preprocessText(text)
    end = time.time()
    print(text)
    print(f"Time taken: {end - start} seconds")


    # # Tokenize the text
    # sentences = sent_tokenize(text)
    # for word in sentences:
    #     tokens = word_tokenize(word)
    #     print(tokens)


    # text = ("I am not don't and she's")
    # text = preprocessText(text)
    #
    # print(text)
    # # Tokenize the text
    # sentences = sent_tokenize(text)
    # for word in sentences:
    #     tokens = word_tokenize(word)
    #     print(tokens)
