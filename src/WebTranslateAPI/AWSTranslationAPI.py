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
    source_text = "Located in Skagen, the northernmost point in Denmark, the summer house pays tribute to local architecture and the history of the town. Therefore, the summer house’s materials drew inspiration from houses built during Skagen’s Black Period, when charred wood f…"
    translated_text = translate_text(source_text, "da", "en")  # Korean to English
    end = time.time()
    print(f"Translated Text: {translated_text}")
    print(end - start)

