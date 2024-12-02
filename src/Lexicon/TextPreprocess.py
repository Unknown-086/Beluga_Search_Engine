import re
from src.WebTranslateAPI.AWSTranslationAPI import translate_text

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



def preprocessLanguageText(text, sourceLanguage):
    """
        Preprocess text by:
        - Converting to lowercase
        - Removing punctuation
        - Tokenizing into words using NLTK
    """

    if not isinstance(text, str):
        return []  # Return empty list for invalid or missing text

    # Translation is not needed if the source language and it will give error
    if text == '':
        return []
    text = translate_text(text, sourceLanguage, "en")

    text = text.lower()  # Convert to lowercase
    text = re.sub(r'[^\s\da-zA-Z]', ' ', text) # Remove punctuation
    return re.findall(r'\b\w+\b', text)  # Tokenize using regex

