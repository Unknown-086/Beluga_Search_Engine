import re

def preprocess_text(text):
    """
    Preprocess text by lowercasing, removing punctuation, and splitting into words.
    Preserves numbers.
    """
    if not isinstance(text, str):
        return []
    text = text.lower()  # Convert to lowercase
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation, but keep numbers
    return text.split()  # Tokenize into words

# Example usage
sample_text = "The year is 2023, and data science is :/ {} [@#$} growing rapidly."
processed = preprocess_text(sample_text)
print(processed)
