import os
import time
import pandas as pd
import orjson
import json
from collections import defaultdict
from src.Lexicon.TextPreprocess import preprocessText


def preprocessTextWithPositions(text):
    """
    Preprocess text and return a list of tuples with each word and its position.
    """
    if pd.isnull(text) or not isinstance(text, str):
        return []  # Return empty list for invalid or missing text

    words = preprocessText(text)  # Preprocess text
    return [(word, position) for position, word in enumerate(words)]  # Pair word with position


def createForwardIndexWithLexicon(datasetPaths, columnLists, lexicon):
    """
    Create a forward index with word positions using Word IDs from a lexicon.
    :param datasetPaths: List of dataset file paths
    :param columnLists: List of column names to process for each dataset
    :param lexicon: Dictionary mapping words to their unique Word IDs
    :return: A dictionary representing the forward index with Word IDs and positions
    """
    forward_index = defaultdict(list)  # Dictionary to store forward index

    for datasetPath, columnList in zip(datasetPaths, columnLists):
        print(f"Processing dataset: {datasetPath}")
        try:
            for chunk in pd.read_csv(datasetPath, chunksize=10_000):
                if 'DocID' not in chunk.columns:
                    print(f"Error: 'DocID' column not found in the dataset '{datasetPath}'.")
                    continue

                for column in columnList:
                    if column not in chunk.columns:
                        print(f"Warning: Column '{column}' not found in the dataset '{datasetPath}'.")
                        continue

                    # Fill missing values
                    chunk[column] = chunk[column].fillna('')

                    # Preprocess text and add positions
                    for _, row in chunk.iterrows():
                        print(f"Processing DocID: {row['DocID']}")

                        doc_id = row['DocID']  # Use the DocID from the dataset
                        text = row[column]
                        words_with_positions = preprocessTextWithPositions(text)

                        # Convert words to Word IDs using the lexicon
                        word_ids_with_positions = [
                            (lexicon[word], position) for word, position in words_with_positions if word in lexicon
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
    Save the forward index to a JSON file.
    :param forward_index: The forward index dictionary with positions
    :param output_file_path: Path to the output JSON file
    """
    try:
        # Prepare forward index for JSON serialization
        json_ready_index = {str(doc_id): [[word_id, position] for word_id, position in words_with_positions]
            for doc_id, words_with_positions in forward_index.items()}

        # Save to JSON file
        with open(output_file_path, 'w') as json_file:
            json.dump(json_ready_index, json_file, indent=2)
    except Exception as e:
        print(f"Error saving forward index to JSON file: {e}")


# Main execution
if __name__ == "__main__":
    # File paths and configuration
    datasetsPaths = [
        os.path.join('../..', 'data', 'FilteredDatasets', 'ModifiedGlobalNewsDataset13_Language_English.csv')
    ]
    columnLists = [
        ['source_name', 'author', 'title', 'description', 'content', 'category', 'full_content']
    ]

    lexiconFilePath = os.path.join('../..', 'data', 'Lexicons', 'LexiconGlobalNewsEnglish6.json')
    outputFilePath = os.path.join('../..', 'data', 'ForwardIndexData', 'ForwardIndex_GlobalNews_English.json')

    print("Loading lexicon...")
    with open(lexiconFilePath, 'rb') as lexicon_file:
        lexicon = orjson.loads(lexicon_file.read())  # Load lexicon from JSON and convert to dict

    startTime = time.time()

    print("Building forward index with Word IDs...")
    forward_index = createForwardIndexWithLexicon(datasetsPaths, columnLists, lexicon)

    print(f"Saving forward index to {outputFilePath}...")
    saveForwardIndexToJSON(forward_index, outputFilePath)

    endTime = time.time()
    print(f"Forward index built and saved successfully. Time taken: {endTime - startTime:.2f} seconds")
