import json

def create_barrels(inverted_index, target_barrel_size):
    """
    Create barrels based on the number of DocumentIDs per WordID.
    :param inverted_index: Dictionary with WordID as keys and lists of DocumentIDs as values.
    :param target_barrel_size: Maximum number of DocumentIDs per barrel.
    :return: A dictionary mapping WordID ranges to barrel file paths.
    """
    barrels = {}
    current_barrel = {}
    current_barrel_doc_count = 0
    barrel_id = 1
    barrel_metadata = {}

    for word_id, doc_ids in inverted_index.items():
        doc_count = len(doc_ids)

        # Check if adding this WordID exceeds the target size
        if current_barrel_doc_count + doc_count > target_barrel_size:
            # Save the current barrel
            barrel_path = f"barrels/barrel{barrel_id}.json"
            with open(barrel_path, "w") as barrel_file:
                json.dump(current_barrel, barrel_file)

            # Update metadata
            first_word_id = min(current_barrel.keys())
            last_word_id = max(current_barrel.keys())
            barrel_metadata[f"{first_word_id}-{last_word_id}"] = barrel_path

            # Start a new barrel
            current_barrel = {}
            current_barrel_doc_count = 0
            barrel_id += 1

        # Add WordID and its DocumentIDs to the current barrel
        current_barrel[word_id] = doc_ids
        current_barrel_doc_count += doc_count

    # Save the final barrel
    if current_barrel:
        barrel_path = f"barrels/barrel{barrel_id}.json"
        with open(barrel_path, "w") as barrel_file:
            json.dump(current_barrel, barrel_file)

        first_word_id = min(current_barrel.keys())
        last_word_id = max(current_barrel.keys())
        barrel_metadata[f"{first_word_id}-{last_word_id}"] = barrel_path

    return barrel_metadata
