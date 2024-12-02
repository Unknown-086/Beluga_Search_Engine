import os
import pandas as pd
from TextPreprocess import preprocessText, preprocessLanguageText
from collections import defaultdict
import orjson


def buildLexicon(datasetPaths, ColumnLists):
    """
    Create a combined lexicon from multiple datasets.
    :param datasetPaths: List of paths to the datasets
    :param ColumnLists: List of lists containing column names to process for each dataset
    """

    startID = 1
    lexicon = defaultdict(lambda: len(lexicon) + startID)  # Assign unique IDs starting from 1
    currentID = len(lexicon) + startID

    for datasetPath, columnList in zip(datasetPaths, ColumnLists):
        print(f"Processing dataset: {datasetPath}")
        try:
            for chunk in pd.read_csv(datasetPath, chunksize = 10_000):
                for column in columnList:
                    if column not in chunk.columns:
                        print(f"Warning: Column '{column}' not found in the dataset '{datasetPath}'.")
                        continue

                    chunk[column] = chunk[column].fillna('')
                    chunk[column] = chunk.apply(lambda row: preprocessLanguageText(row[column], row['language'])
                                                    if row['language'] != 'en'
                                                    else preprocessText(row[column]), axis=1)

                    for text in chunk[column]:
                        words = set(text) # Avoid Duplicate for the local Record
                        for word in words:
                            if word not in lexicon:
                                lexicon[word] = currentID
                                currentID += 1


        except FileNotFoundError:
            print(f"Error: File '{datasetPath}' not found.")
        except Exception as e:
            print(f"Unexpected error while processing '{datasetPath}': {e}")

    return dict(lexicon) # Convert default dictionary to a regular dictionary


def saveLexiconToJSON(lexicon, outputPath):
    """
    Save the lexicon to a JSON file.
    :param lexicon: The lexicon dictionary
    :param outputPath: Path to the output JSON file
    """
    try:
        # Ensure the directory exists or create it
        os.makedirs(os.path.dirname(outputPath), exist_ok=True)

        with open(outputPath, 'wb') as json_file:
            json_file.write(orjson.dumps(lexicon, option=orjson.OPT_INDENT_2))
    except Exception as e:
        print(f"Error saving lexicon to JSON file: {e}")