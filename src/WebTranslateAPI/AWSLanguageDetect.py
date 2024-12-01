import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
import time

def AWS_detect_language(text):
    # Initialize the boto3 client for AWS Comprehend
    client = boto3.client('comprehend', region_name='us-east-1')  # Specify the region you are working in

    try:
        # Detect the language
        response = client.detect_dominant_language(Text=text)

        # Extract and return the dominant language
        languages = response['Languages']
        if languages:
            dominant_language = languages[0]['LanguageCode']
            return dominant_language
        else:
            return "No dominant language detected"

    except (NoCredentialsError, PartialCredentialsError):
        return "Error: AWS credentials are not set correctly"
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    start = time.time()
    text = "Piwik &amp;#8211; eine Open-Source Webanalyse-Software als Alternative zu Google Analytics"
    language = AWS_detect_language(text)
    end = time.time()
    print(f"The detected language is: {language}")
    print(end - start)