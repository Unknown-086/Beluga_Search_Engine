import os
import json

from sympy import numer


def createHashedBarrels(inverted_index_path, output_directory, metadata_path, num_barrels):
    """
    Create barrels by hashing WordIDs to distribute them across a fixed number of barrels.
    :param inverted_index_path: Path to the inverted index JSON file
    :param output_directory: Directory to save the barrel files
    :param metadata_path: Path to save the barrel metadata JSON file
    :param num_barrels: Number of barrels to create
    """
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    print("Loading inverted index...")
    try:
        with open(inverted_index_path, 'r') as inverted_file:
            inverted_index = json.load(inverted_file)
            # Convert WordIDs to integers for processing
            inverted_index = {int(word_id): doc_ids for word_id, doc_ids in inverted_index.items()}

        print("Creating hashed barrels...")
        barrels = [{} for _ in range(num_barrels)]  # Initialize empty barrels
        barrel_metadata = {}

        # Assign WordIDs to barrels using hashing
        for word_id, doc_ids in inverted_index.items():
            barrel_index = word_id % num_barrels
            barrels[barrel_index][word_id] = doc_ids

        # Save each barrel to a file
        for i, barrel in enumerate(barrels):
            barrel_path = os.path.join(output_directory, f"barrel{i + 1}.json")
            with open(barrel_path, 'w') as barrel_file:
                json.dump(barrel, barrel_file, indent=2)

            # Update metadata with the barrel path
            barrel_metadata[str(i + 1)] = barrel_path

        # Save the metadata to a JSON file
        print(f"Saving barrel metadata to {metadata_path}...")
        with open(metadata_path, 'w') as metadata_file:
            json.dump(barrel_metadata, metadata_file, indent=2)

        print("Hashed barrels created and metadata saved successfully.")

    except FileNotFoundError:
        print(f"Error: Inverted index file '{inverted_index_path}' not found.")
    except Exception as e:
        print(f"Unexpected error while processing: {e}")

def getBarrelForHashed(word_id, metadata_path):
    """
    Retrieve the barrel path and DocumentIDs for a WordID using the hashed barrel method.
    :param word_id: The WordID to retrieve.
    :param metadata_path: Path to the hashed barrel metadata JSON file.
    :return: Barrel path and list of DocumentIDs for the WordID (if found).
    """
    try:
        print("Loading hashed barrel metadata...")
        with open(metadata_path, 'r') as metadata_file:
            barrel_metadata = json.load(metadata_file)

        # Determine the number of barrels from the metadata
        num_barrels = max(int(key) for key in barrel_metadata.keys())

        # Compute the hashed barrel index (starting from 1)
        barrel_index = word_id % num_barrels + 1  # Adjust for 1-based indexing
        barrel_key = str(barrel_index)

        if barrel_key not in barrel_metadata:
            print(f"Barrel index {barrel_key} not found in metadata.")
            return None, []

        barrel_path = barrel_metadata[barrel_key]

        print(f"Loading barrel from {barrel_path}...")
        with open(barrel_path, 'r') as barrel_file:
            barrel_data = json.load(barrel_file)

        doc_ids = barrel_data.get(str(word_id), [])
        return barrel_path, doc_ids

    except FileNotFoundError:
        print(f"Error: File '{metadata_path}' not found.")
        return None, []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None, []
