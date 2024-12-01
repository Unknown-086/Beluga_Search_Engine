import boto3
import time

# Initialize a session using Amazon Translate
translate = boto3.client('translate', region_name='us-east-1')  # Change region as needed

def translate_text(text, source_lang, target_lang):
    # Translate text
    response = translate.translate_text(
        Text=text,
        SourceLanguageCode=source_lang,
        TargetLanguageCode=target_lang
    )
    return response['TranslatedText']

# Example usage
if __name__ == "__main__":
    start = time.time()
    source_text = "Starting today, we're testing a new program (Not A Bot) in New Zealand and the Philippines. New, unverified accounts will be required to sign up for a $1 annual subscription to be able to post &amp; … [+119 chars]"
    translated_text = translate_text(source_text, "ja", "en")  # Korean to English
    end = time.time()
    print(f"Translated Text: {translated_text}")
    print(end - start)

