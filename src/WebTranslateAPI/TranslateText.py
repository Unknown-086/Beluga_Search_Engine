import requests

def translate_text_via_api(text, dest_lang='en'):
    """
    Sends a request to the translation API and returns the translated text.

    Args:
        text (str): The text to be translated.
        dest_lang (str): The destination language code (default is 'en' for English).

    Returns:
        str: The translated text.
    """
    url = 'http://127.0.0.1:5000/translate'
    payload = {
        'text': text,
        'dest_lang': dest_lang
    }
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        return response.json().get('translated_text', 'Translation failed')
    else:
        return f"Error: {response.status_code} - {response.text}"




# Example usage
translated_text = translate_text_via_api("지식 구독 서비스 롱블랙, 읽기 습관을 도와주는 ‘알람 앱’ 론칭", "en")
print(translated_text)