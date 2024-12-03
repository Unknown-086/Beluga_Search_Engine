import re

pattern = r"\d+"  # Match one or more digits
string = "The year is  a 278000 987"

# Search for the pattern
match = re.search(pattern, string)
if match:
    print("Match found:", match.group())
