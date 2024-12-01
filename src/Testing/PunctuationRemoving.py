import re

text = "Hello, world! This is a test."
cleaned_text = re.sub(r'[^\w\s]', '', text)  # Remove all characters except words and spaces
print(cleaned_text)
