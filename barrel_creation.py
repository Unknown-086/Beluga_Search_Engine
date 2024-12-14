import json
import os
import math

# -------------------------
# Step 1: Load Inverted Index
# -------------------------
def load_inverted_index(filepath):
    """
    Load the inverted index from a JSON file.
    :param filepath: Path to the inverted index file.
    :return: Dictionary representation of the inverted index.
    """
    with open(filepath, 'r', encoding='utf-8') as file:
        return json.load(file)

# -------------------------
# Step 2: Calculate Number of Barrels
# -------------------------
def calculate_num_barrels(inverted_index, terms_per_barrel=10000):
    """
    Calculate the number of barrels needed based on the size of the inverted index.
    :param inverted_index: Dictionary representing the inverted index.
    :param terms_per_barrel: Maximum number of terms per barrel.
    :return: Number of barrels.
    """
    total_terms = len(inverted_index)
    num_barrels = math.ceil(total_terms / terms_per_barrel)
    return max(num_barrels, 1)  # Ensure at least one barrel

# -------------------------
# Step 3: Create Barrels Alphabetically
# -------------------------
def create_barrels_alphabetically(inverted_index, output_dir, terms_per_barrel=10000):
    """
    Split the inverted index into smaller chunks (barrels) alphabetically and save them as JSON files.
    :param inverted_index: Dictionary representing the inverted index.
    :param output_dir: Directory to save the barrels.
    :param terms_per_barrel: Maximum number of terms per barrel.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print("Sorting terms alphabetically...")
    sorted_terms = sorted(inverted_index.keys())  # Sort terms alphabetically
    
    # Calculate the number of barrels
    num_barrels = calculate_num_barrels(inverted_index, terms_per_barrel)
    print(f"Creating {num_barrels} barrels alphabetically...")

    # Split terms into barrels
    for i in range(num_barrels):
        start_idx = i * terms_per_barrel
        end_idx = min((i + 1) * terms_per_barrel, len(sorted_terms))
        barrel_terms = sorted_terms[start_idx:end_idx]

        # Create a subset of the inverted index for the current barrel
        barrel_data = {term: inverted_index[term] for term in barrel_terms}

        # Save the barrel to a JSON file
        barrel_filepath = os.path.join(output_dir, f'barrel_{i}.json')
        with open(barrel_filepath, 'w', encoding='utf-8') as barrel_file:
            json.dump(barrel_data, barrel_file, indent=4)
            print(f"Barrel {i} saved to {barrel_filepath}")

# -------------------------
# Step 4: Main Execution
# -------------------------
if __name__ == "__main__":
    # Path to your inverted index file
    inverted_index_filepath = "D:/myPython/InvertedIndex_1000.json"

    # Load the inverted index
    print("Loading inverted index...")
    inverted_index = load_inverted_index(inverted_index_filepath)

    # Output directory for barrels
    barrels_directory = 'barrels'

    # Create barrels alphabetically
    create_barrels_alphabetically(inverted_index, barrels_directory, terms_per_barrel=10000)
    print(f"Barrels created in directory: {barrels_directory}")
