import requests
from bs4 import BeautifulSoup

def get_title(soup):
    title = soup.find('title')
    return title.text.strip() if title else 'No title'

def get_description(soup):
    description = soup.find('meta', attrs={'name': 'description'})
    return description['content'].strip() if description else 'No description'

def crawl_url(url, get='all'):
    try:
        # Send an HTTP GET request
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an error for bad HTTP responses

        # Parse the webpage content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the required information based on the 'get' parameter
        if get == 'title':
            return get_title(soup)
        elif get == 'description':
            return get_description(soup)
        else:
            return {
                "url": url,
                "title": get_title(soup),
                "description": get_description(soup)
            }

    except Exception as e:
        # Handle errors such as connection issues or invalid responses
        return {
            "url": url,
            "title": "Error fetching title",
            "description": f"Error: {str(e)}"
        }


import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import time

def scrape_website(url):
    try:
        # Validate URL
        if not url.startswith(('http://', 'https://')):
            return {'error': 'Invalid URL format', 'url': url}

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        response = requests.get(url, headers=headers, timeout=10)
        
        # Check response status
        if response.status_code != 200:
            return {'error': f'HTTPError: {response.status_code}', 'url': url}

        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove unwanted elements
        for element in soup(['script', 'style', 'iframe', 'nav', 'footer']):
            element.decompose()

        title = soup.title.string if soup.title else ""
        
        meta_desc = ""
        meta_tag = soup.find('meta', attrs={'name': 'description'})
        if meta_tag:
            meta_desc = meta_tag.get('content', '')

        # Get main content
        content = ' '.join(soup.stripped_strings)
        
        if not content.strip():
            return {'error': 'No content found', 'url': url}

        return {
            'title': title.strip(),
            'description': meta_desc.strip(),
            'content': content.strip(),
            'url': url
        }

    except requests.exceptions.RequestException as e:
        return {'error': f'Failed to fetch content: {str(e)}', 'url': url}
    except Exception as e:
        return {'error': str(e), 'url': url}