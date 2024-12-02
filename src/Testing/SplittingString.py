import re

text = "apple;banana|cherry,:grape"
fruits = re.split(r'[:;|,]', text)  # Split by semicolon, pipe, or comma
print(fruits)
