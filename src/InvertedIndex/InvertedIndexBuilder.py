import json
from collections import defaultdict


def buildInvertedIndex(forward_index_path, output_file_path):
    """
    Build an inverted index from a forward index using the standard JSON module.
    :param forward_index_path: Path to the forward index JSON file
    :param output_file_path: Path to save the inverted index JSON file
    """
    inverted_index = defaultdict(set)  # Use set to avoid duplicate DocIDs

    print("Loading forward index...")
    try:
        with open(forward_index_path, 'r') as forward_file:
            forward_index = json.load(forward_file)  # Use json.load instead of orjson.loads

        print("Building inverted index...")
        for doc_id, word_positions in forward_index.items():
            for word_id, _ in word_positions:  # Ignore positions
                inverted_index[word_id].add(doc_id)

        # Convert sets to lists for JSON serialization
        json_ready_index = {str(word_id): list(doc_ids) for word_id, doc_ids in inverted_index.items()}

        print(f"Saving inverted index to {output_file_path}...")
        with open(output_file_path, 'w') as output_file:  # Use 'w' for writing text files
            json.dump(json_ready_index, output_file, indent=2)  # Use json.dump instead of orjson.dumps

        print("Inverted index built and saved successfully.")

    except FileNotFoundError:
        print(f"Error: Forward index file '{forward_index_path}' not found.")
    except Exception as e:
        print(f"Unexpected error while processing: {e}")

