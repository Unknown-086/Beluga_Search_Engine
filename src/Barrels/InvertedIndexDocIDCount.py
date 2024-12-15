import os
import json

def countDocumentIDs(inverted_index_path):
    """
    Count the total number of unique DocumentIDs in the inverted index.
    :param inverted_index_path: Path to the inverted index JSON file
    :return: Total count of unique DocumentIDs
    """
    count = 0
    try:
        print(f"Loading inverted index from {inverted_index_path}...")
        with open(inverted_index_path, 'r') as file:
            inverted_index = json.load(file)
            # Convert WordIDs to integers and retrieve DocumentIDs
            inverted_index = {int(word_id): doc_ids for word_id, doc_ids in inverted_index.items()}

        print("Counting unique DocumentIDs...")
        all_doc_ids = []  # Use a set to ensure uniqueness
        for doc_ids in inverted_index.values():

            count += len(doc_ids)


        # print(f"Total unique DocumentIDs: {total_count}")
        return count

    except FileNotFoundError:
        print(f"Error: File '{inverted_index_path}' not found.")
    except Exception as e:
        print(f"Unexpected error while processing: {e}")
        return 0

# Example usage
if __name__ == "__main__":
    invertedIndexPath = os.path.join('../..', 'data', 'InvertedIndexData', 'Testing', 'InvertedIndex_GlobalNews_English2.json')
    total_doc_ids = countDocumentIDs(invertedIndexPath)
    print(f"Counted {total_doc_ids} unique DocumentIDs.")
