import json
import os
import time


def getBarrelForHashed(word_id, metadata_path, num_barrels):
    """
    Retrieve the barrel path and DocumentIDs for a WordID using the hashed barrel method.
    :param word_id: The WordID to retrieve.
    :param metadata_path: Path to the hashed barrel metadata JSON file.
    :param num_barrels: Number of barrels used in the hashing process.
    :return: Barrel path and list of DocumentIDs for the WordID (if found).
    """
    try:
        print("Loading hashed barrel metadata...")
        with open(metadata_path, 'r') as metadata_file:
            barrel_metadata = json.load(metadata_file)

        # Compute the hashed barrel index
        barrel_index = word_id % num_barrels
        print(f"Hashed barrel index: {barrel_index}")
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

# Example Usage
if __name__ == "__main__":
    word_id = 65000

    # Hashed Barrel Example
    hashedMetadataPath = os.path.join('../..', 'data', 'BarrelData', 'Testing', 'PathData', 'barrel_metadata_GlobalEnglish2_Hashed.json')
    numBarrels = 2000
    start = time.time()
    barrel_path, doc_ids = getBarrelForHashed(word_id, hashedMetadataPath, numBarrels)
    end = time.time()
    print(f"Hashed Barrel Path: {barrel_path}, DocumentIDs: {doc_ids}")
    print(f"Time taken: {end - start:.6f} seconds")

    # Ranged Barrel Example
    rangedMetadataPath = os.path.join('../..', 'data', 'BarrelData', 'Testing', 'PathData', 'barrel_metadata_GlobalEnglish2.json')
    start = time.time()
    barrel_path, doc_ids = getBarrelForRanged(word_id, rangedMetadataPath)
    end = time.time()
    print(f"Ranged Barrel Path: {barrel_path}, DocumentIDs: {doc_ids}")
    print(f'Time taken: {end - start:.6f} seconds')