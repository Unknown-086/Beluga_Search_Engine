import boto3

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
source_text = "Σοκάρουν οι μαρτυρίες φοιτητών από το Νεπάλ που βρέθηκαν στη δίνη του πολέμου στη Μέση Ανατολή ανάμεσα στο Ισραήλ και τους τρομοκράτες της Χαμάς. Οι φοιτητές από το Νεπάλ επέστρεψαν πίσω στην πατρίδα τους με την πρώτη ειδική πτήση από το Ισραήλ, έγιναν δεκτοί…"
translated_text = translate_text(source_text, "el", "en")  # Korean to English
print(f"Translated Text: {translated_text}")
