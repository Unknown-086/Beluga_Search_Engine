import os
import json

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
            barrel_metadata[str(i)] = barrel_path

        # Save the metadata to a JSON file
        print(f"Saving barrel metadata to {metadata_path}...")
        with open(metadata_path, 'w') as metadata_file:
            json.dump(barrel_metadata, metadata_file, indent=2)

        print("Hashed barrels created and metadata saved successfully.")

    except FileNotFoundError:
        print(f"Error: Inverted index file '{inverted_index_path}' not found.")
    except Exception as e:
        print(f"Unexpected error while processing: {e}")

