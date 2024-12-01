import nltk
from nltk import sent_tokenize
from nltk.tokenize import word_tokenize

# Download the necessary NLTK data files
# nltk.download('punkt')
# nltk.download('punkt_tab')
# nltk.download('punkt_treebank')

# Sample text
text = ("Natural Language and Toolkit is a powerful library for NLP.\n"
        "I am not what you think")

# Tokenize the text
sentences = sent_tokenize(text)
for word in sentences:
    tokens = word_tokenize(word)
    print(tokens)



# Sample text with paragraphs
text = ("Natural Language Toolkit is a powerful library for NLP.\n\n"
        "It provides easy-to-use interfaces to over 50 corpora and lexical resources.\n\n"
        "NLTK is suitable for linguists, engineers, students, educators, researchers, and industry users.")

# Tokenize the entire text into words
tokens = word_tokenize(text)

print(tokens)