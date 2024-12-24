import json
import os
from CrawlingWebLinks.CrawlUrl import crawl_url
from Barrels.HashBarrelMaker import createHashedBarrels

# File paths
NEW_CONTENT_FILE = 'new_dataset.json'
LEXICON_FILE = 'D:\\myPython\\Lexicons\\SampleTesting\\Lexicon_1000.json'
FORWARD_INDEX_FILE = 'D:\\myPython\\ForwardIndexData\\SampleTesting\\ForwardIndex_1000.json'
INVERTED_INDEX_FILE = 'D:\\myPython\\InvertedIndexData\\SampleTesting\\InvertedIndex_1000.json'
BARRELS_DIR = 'D:\\myPython\\BarrelsData\\SampleTesting\\barrels'
HASH_BARRELS_DIR = os.path.join(BARRELS_DIR, 'hash')
METADATA_PATH = 'D:\\myPython\\Metadata.json'
NUM_BARRELS = 10

# Utility functions for loading and saving JSON files
def load_json(filepath, default_data=None):
    """Load JSON data from a file, returning default_data if the file doesn't exist or is empty."""
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
                if content.strip():
                    return json.loads(content)  
                else:
                    print(f"Warning: {filepath} is empty. Using default data.")
                    return default_data
        except json.JSONDecodeError:
            print(f"Warning: {filepath} contains invalid data. Skipping reset and using default data.")
            return default_data
    else:
        print(f"Warning: {filepath} does not exist. Creating new file.")
        return default_data if default_data else {}

def save_json(filepath, data):
    """Save data to a JSON file."""
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

# Add new content
def add_new_content(url):
    """Add new content to the search engine dataset."""
    # Load existing datasets
    lexicon = load_json(LEXICON_FILE, {})
    forward_index = load_json(FORWARD_INDEX_FILE, {})
    inverted_index = load_json(INVERTED_INDEX_FILE, {})
    new_content = load_json(NEW_CONTENT_FILE, [])  # Load existing content or initialize as an empty list

    # Check if the URL is already in the dataset
    if any(entry.get('url') == url for entry in new_content):
        print(f"The URL '{url}' has already been added. Skipping.")
        return

    # Retrieve metadata for the URL
    metadata = crawl_url(url)
    if metadata.get('title', '') == "Error fetching title":
        print(f"Failed to retrieve metadata for {url}")
        return

    # Assign a new document ID
    new_doc_id = str(len(forward_index) + 1)

    # Add new metadata to the list
    metadata['url'] = url  # Ensure the URL is stored for duplicate checking
    new_content.append(metadata)

    # Tokenize title and description
    terms = (metadata['title'] + ' ' + metadata['description']).split()
    terms = [term.lower() for term in terms]  # Normalize terms

    # Update lexicon and forward index
    forward_index[new_doc_id] = []
    for term in terms:
        if term not in lexicon:
            term_id = str(len(lexicon) + 1)  
            lexicon[term] = term_id
        else:
            term_id = lexicon[term]
        forward_index[new_doc_id].append(term_id)

        # Update inverted index (word ID -> doc IDs)
        if term_id not in inverted_index:
            inverted_index[term_id] = []
        if new_doc_id not in inverted_index[term_id]:
            inverted_index[term_id].append(new_doc_id)

    # Save updated datasets
    save_json(LEXICON_FILE, lexicon)
    save_json(FORWARD_INDEX_FILE, forward_index)
    save_json(INVERTED_INDEX_FILE, inverted_index)
    save_json(NEW_CONTENT_FILE, new_content)

    print(f"Content from {url} added successfully with document ID {new_doc_id}.")

    # Now we will make hash barrels
    createHashedBarrels(INVERTED_INDEX_FILE, HASH_BARRELS_DIR, METADATA_PATH, NUM_BARRELS)

# Main script
if __name__ == "__main__":
    while True:
        url = input("Enter the URL to add (or 'exit' to quit): ")
        if url.lower() == 'exit':
            break
        add_new_content(url)
    print("Content addition process completed.")
