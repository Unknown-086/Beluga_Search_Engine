import os
import json

import os
import json

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
            inverted_index = {int(word_id): doc_ids for word_id, doc_ids in inverted_index.items()}

        print("Creating barrels...")
        current_barrel = {}
        current_barrel_doc_count = 0
        barrel_id = 1
        barrel_metadata = {}
        first_word_id = None

        def save_barrel(barrel, barrel_id, first_word_id, output_directory, barrel_metadata):
            if barrel:
                barrel_path = os.path.join(output_directory, f"barrel{barrel_id}.json")
                with open(barrel_path, 'w') as barrel_file:
                    json.dump(barrel, barrel_file, indent=2)
                min_word_id = min(barrel.keys())
                max_word_id = max(barrel.keys())
                barrel_metadata[f"{min_word_id}-{max_word_id}"] = barrel_path

        def reset_barrel():
            nonlocal current_barrel, current_barrel_doc_count, first_word_id, barrel_id
            save_barrel(current_barrel, barrel_id, first_word_id, output_directory, barrel_metadata)
            current_barrel = {}
            current_barrel_doc_count = 0
            first_word_id = None
            barrel_id += 1

        for word_id, doc_ids in inverted_index.items():
            doc_count = len(doc_ids)

            if first_word_id is None:
                first_word_id = word_id

            # Handle large single WordID case
            if doc_count > target_barrel_size + tolerance:
                reset_barrel()
                save_barrel({word_id: doc_ids}, barrel_id, word_id, output_directory, barrel_metadata)
                barrel_id += 1
                continue

            # Check if adding the current WordID exceeds the barrel size
            if (current_barrel_doc_count + doc_count > target_barrel_size + tolerance or
                (current_barrel_doc_count > target_barrel_size - tolerance and doc_count > tolerance)):
                reset_barrel()
                first_word_id = word_id  # Start new barrel with current WordID

            current_barrel[word_id] = doc_ids
            current_barrel_doc_count += doc_count

        # Save the final barrel
        reset_barrel()

        print(f"Saving barrel metadata to {metadata_path}...")
        with open(metadata_path, 'w') as metadata_file:
            json.dump(barrel_metadata, metadata_file, indent=2)

        print("Barrels created and metadata saved successfully.")

    except FileNotFoundError:
        print(f"Error: Inverted index file '{inverted_index_path}' not found.")
    except Exception as e:
        print(f"Unexpected error while processing: {e}")

def getBarrelForRanged(word_id, metadata_path):
    """
    Retrieve the barrel path and DocumentIDs for a WordID using the ranged barrel method.
    :param word_id: The WordID to retrieve.
    :param metadata_path: Path to the ranged barrel metadata JSON file.
    :return: Barrel path and list of DocumentIDs for the WordID (if found).
    """
    try:
        print("Loading ranged barrel metadata...")
        with open(metadata_path, 'r') as metadata_file:
            barrel_metadata = json.load(metadata_file)

        # Locate the range containing the WordID
        for range_key, barrel_path in barrel_metadata.items():
            start, end = map(int, range_key.split('-'))
            if start <= word_id <= end:
                print(f"Loading barrel from {barrel_path}...")
                with open(barrel_path, 'r') as barrel_file:
                    barrel_data = json.load(barrel_file)

                doc_ids = barrel_data.get(str(word_id), [])
                return barrel_path, doc_ids

        print(f"WordID {word_id} not found in any range.")
        return None, []

    except FileNotFoundError:
        print(f"Error: File '{metadata_path}' not found.")
        return None, []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None, []
