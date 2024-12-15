import os
import json
from collections import defaultdict

def createBarrels(inverted_index_path, output_directory, metadata_path, target_barrel_size, tolerance=1000):
    """
    Create balanced barrels from the inverted index.
    :param inverted_index_path: Path to the inverted index JSON file
    :param output_directory: Directory to save the barrel files
    :param metadata_path: Path to save the barrel metadata JSON file
    :param target_barrel_size: Target number of DocumentIDs per barrel
    :param tolerance: Allowed deviation from the target size (+/- tolerance)
    """
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    print("Loading inverted index...")
    try:
        with open(inverted_index_path, 'r') as inverted_file:
            inverted_index = json.load(inverted_file)
            # Convert WordIDs to integers for processing
            inverted_index = {int(word_id): doc_ids for word_id, doc_ids in inverted_index.items()}

        print("Creating barrels...")
        current_barrel = {}
        current_barrel_doc_count = 0
        barrel_id = 1
        barrel_metadata = {}
        first_word_id = None

        for word_id, doc_ids in inverted_index.items():
            doc_count = len(doc_ids)

            # Start tracking the range of WordIDs in the barrel
            if first_word_id is None:
                first_word_id = word_id

            # Check if adding this WordID exceeds the flexible range
            if (current_barrel_doc_count + doc_count > target_barrel_size + tolerance or
                (current_barrel_doc_count > target_barrel_size - tolerance and doc_count > tolerance)):

                # Save the current barrel
                barrel_path = os.path.join(output_directory, f"barrel{barrel_id}.json")
                with open(barrel_path, 'w') as barrel_file:
                    json.dump(current_barrel, barrel_file, indent=2)

                # Update metadata
                first_word_id = min(current_barrel.keys())
                last_word_id = max(current_barrel.keys())
                barrel_metadata[f"{first_word_id}-{last_word_id}"] = barrel_path

                # Start a new barrel
                current_barrel = {}
                current_barrel_doc_count = 0
                barrel_id += 1
                first_word_id = word_id

            # Add WordID and its DocumentIDs to the current barrel
            current_barrel[word_id] = doc_ids
            current_barrel_doc_count += doc_count

        # Save the final barrel
        if current_barrel:
            barrel_path = os.path.join(output_directory, f"barrel{barrel_id}.json")
            with open(barrel_path, 'w') as barrel_file:
                json.dump(current_barrel, barrel_file, indent=2)

                first_word_id = min(current_barrel.keys())
                last_word_id = max(current_barrel.keys())
            barrel_metadata[f"{first_word_id}-{last_word_id}"] = barrel_path

        # Save the metadata to a JSON file
        print(f"Saving barrel metadata to {metadata_path}...")
        with open(metadata_path, 'w') as metadata_file:
            json.dump(barrel_metadata, metadata_file, indent=2)

        print("Barrels created and metadata saved successfully.")

    except FileNotFoundError:
        print(f"Error: Inverted index file '{inverted_index_path}' not found.")
    except Exception as e:
        print(f"Unexpected error while processing: {e}")
