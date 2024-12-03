import pandas as pd
import json
from collections import defaultdict
from src.Lexicon.TextPreprocess import preprocessText


def buildForwardIndex(datasetPaths, columnLists, lexicon):
    """
    Build a forward index with Word IDs based on the lexicon.
    :param datasetPaths: List of paths to the datasets
    :param columnLists: List of lists containing column names to process for each dataset
    :param lexicon: Dictionary mapping words to their unique Word IDs
    :return: Forward index dictionary
    """
    forward_index = defaultdict(list)

    for datasetPath, columnList in zip(datasetPaths, columnLists):
        print(f"Processing dataset: {datasetPath}")
        try:
            for chunk in pd.read_csv(datasetPath, chunksize=10_000):
                if 'DocID' not in chunk.columns:
                    print(f"Error: 'DocID' column not found in the dataset '{datasetPath}'.")
                    continue

                for _, row in chunk.iterrows():
                    doc_id = row['DocID']
                    combined_text = []

                    # Combine and preprocess text from all specified columns
                    for column in columnList:
                        if column in row and pd.notna(row[column]):
                            combined_text.extend(preprocessText(row[column]))

                    # Replace words with Word IDs
                    word_ids_with_positions = [
                        (lexicon[word], position) for position, word in enumerate(combined_text) if word in lexicon
                    ]

                    # Add to the forward index
                    forward_index[doc_id].extend(word_ids_with_positions)

        except FileNotFoundError:
            print(f"Error: File '{datasetPath}' not found.")
        except Exception as e:
            print(f"Unexpected error while processing '{datasetPath}': {e}")

    return forward_index


def saveForwardIndexToJSON(forward_index, output_file_path):
    """
    Save the forward index to a JSON file using the standard JSON library.
    :param forward_index: The forward index dictionary
    :param output_file_path: Path to the output JSON file
    """
    try:
        # Prepare forward index for JSON serialization
        json_ready_index = {
            str(doc_id): [[word_id, position] for word_id, position in words_with_positions]
            for doc_id, words_with_positions in forward_index.items()
        }

        # Save to JSON file
        with open(output_file_path, 'w') as json_file:
            json.dump(json_ready_index, json_file, indent=2)

        print(f"Forward index saved successfully to {output_file_path}")
    except Exception as e:
        print(f"Error saving forward index to JSON file: {e}")
