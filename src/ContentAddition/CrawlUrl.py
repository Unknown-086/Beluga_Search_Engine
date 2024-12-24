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