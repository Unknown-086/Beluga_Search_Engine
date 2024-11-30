from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

app = Flask(__name__)

def translate_using_google_translate(text, dest_lang='en'):
    # Set up the Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        # Open Google Translate
        driver.get('https://translate.google.com')

        # Find the input text area and enter the text
        input_area = driver.find_element(By.XPATH, '//*[@aria-label="Source text"]')
        input_area.send_keys(text)

        # Select the target language
        target_lang_button = driver.find_element(By.XPATH, '//*[@aria-label="More target languages"]')
        target_lang_button.click()
        target_lang_input = driver.find_element(By.XPATH, '//*[@aria-label="Search languages"]')
        target_lang_input.send_keys(dest_lang)
        target_lang_input.send_keys(Keys.ENTER)

        # Wait for the translation to appear
        time.sleep(2)  # Adjust the sleep time if necessary

        # Get the translated text
        translated_text = driver.find_element(By.XPATH, '//*[@class="J0lOec"]').text

        return translated_text
    except Exception as e:
        return str(e)
    finally:
        driver.quit()

@app.route('/translate', methods=['POST'])
def translate_text():
    data = request.get_json()
    text = data.get('text')
    dest_lang = data.get('dest_lang', 'en')  # Default to English if not specified

    if not text:
        return jsonify({'error': 'No text provided'}), 400

    try:
        translated_text = translate_using_google_translate(text, dest_lang)
        return jsonify({'translated_text': translated_text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)