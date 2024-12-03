import csv
import re
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

def save_forward_index_to_file_with_positions(forward_index, output_file_path):
    """
    Save the forward index with positions to a file for later use.
    :param forward_index: The forward index dictionary with positions
    :param output_file_path: Path to the output file
    """
    try:
        with open(output_file_path, 'w', encoding='utf-8') as file:
            for document_id, words_with_positions in forward_index.items():
                formatted_words = ', '.join([f"({word}, {position})" for word, position in words_with_positions])
                file.write(f"{document_id}: {formatted_words}\n")
    except Exception as e:
        print(f"Error saving forward index to file: {e}")

# Main execution
if __name__ == "__main__":
    # Update the file paths and column name as per your dataset
    csv_file_path = "ModifiedNews-week-17aug5.csv"  # Path to your CSV file
    text_column_name = "headline_text"  # Replace with the actual column name containing text data
    output_file_path = "forward_index_with_positions.txt"  # Path to save the forward index

    # Step 1: Create forward index with positions
    print("Creating forward index with positions...")
    forward_index = create_forward_index_with_positions(csv_file_path, text_column_name)
    
    # Step 2: Save forward index with positions to file
    print(f"Saving forward index with positions to {output_file_path}...")
    save_forward_index_to_file_with_positions(forward_index, output_file_path)
    
    print("Forward indexing with positions completed.")
