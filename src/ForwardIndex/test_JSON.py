import csv
import re
import json
import time
from collections import defaultdict


def preprocess_text_with_positions(text):
    """
    Preprocess the text and return a list of tuples with each word and its position.
    """
    text = text.lower()  # Convert to lowercase
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    words = text.split()  # Split into words
    return [(word, position) for position, word in enumerate(words)]  # Pair word with position


def create_forward_index_with_positions(csv_file_path, text_column_name):
    """
    Create a forward index with word positions from the dataset.
    :param csv_file_path: Path to the CSV file
    :param text_column_name: Column name containing text data
    :return: A dictionary representing the forward index with positions
    """
    
    forward_index = defaultdict(list)  # Using a defaultdict to store lists of (word, position) tuples
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)  # Read the CSV as a dictionary
            for row_number, row in enumerate(reader):
                document_id = row_number + 1  # Use row number as document ID (1-based index)
                text = row[text_column_name]  # Get text data from the specified column
                words_with_positions = preprocess_text_with_positions(text)  # Get words with positions
                forward_index[document_id] = words_with_positions  # Map document ID to words with positions
    except KeyError:
        print(f"Error: Column '{text_column_name}' not found in CSV file.")
    except FileNotFoundError:
        print(f"Error: File '{csv_file_path}' not found.")
    except Exception as e:
        print(f"Unexpected error: {e}")

    return forward_index


def save_forward_index_to_json(forward_index, output_file_path):
    """
    Save the forward index with positions to a JSON file for later use.
    :param forward_index: The forward index dictionary with positions
    :param output_file_path: Path to the output JSON file
    """
    try:
        # Convert the forward index to a format that can be serialized to JSON
        json_ready_index = {doc_id: [{"word": word, "position": position} for word, position in words_with_positions]
                            for doc_id, words_with_positions in forward_index.items()}

        with open(output_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(json_ready_index, json_file, indent=4, ensure_ascii=False)  # Write JSON with indentation
    except Exception as e:
        print(f"Error saving forward index to JSON file: {e}")


# Main execution
if __name__ == "__main__":
    start = time.time()

    # Update the file paths and column name as per your dataset
    csv_file_path = "myDataset.csv"  # Path to your CSV file
    text_column_name = "headline_text"  # Replace with the actual column name containing text data
    output_file_path = "forward_index_MyDataset_JSON.json"  # Path to save the forward index in JSON format

    # Step 1: Create forward index with positions
    print("Creating forward index with positions...")
    forward_index = create_forward_index_with_positions(csv_file_path, text_column_name)

    # Step 2: Save forward index with positions to JSON file
    print(f"Saving forward index with positions to {output_file_path}...")
    save_forward_index_to_json(forward_index, output_file_path)

    print("Forward indexing with positions completed.")

    end = time.time()
    print(f"Time taken: {end - start:.2f} seconds")

