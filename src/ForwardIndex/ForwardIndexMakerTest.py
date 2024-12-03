import os
import time
import orjson
from src.ForwardIndex.ForwardIndexBuilder import buildForwardIndex, saveForwardIndexToJSON


# Main execution
if __name__ == "__main__":
    # File paths and configuration
    datasetPaths = [
        os.path.join('../..', 'data', 'FilteredDatasets', 'ModifiedGlobalNewsDataset13_English.csv')
    ]
    columnLists = [
        [ 'source_name', 'author', 'title', 'description', 'content', 'category', 'full_content']
    ]

    lexiconFilePath = os.path.join('../..', 'data', 'Lexicons', 'LexiconModifiedGlobalNewsDataset13_7.json')
    outputFilePath = os.path.join('../..', 'data', 'ForwardIndexData', 'ForwardIndex_GlobalNews_English3.json')

    start = time.time()
    print("Loading lexicon...")
    with open(lexiconFilePath, 'rb') as lexicon_file:
        lexicon = orjson.loads(lexicon_file.read())  # Load lexicon from JSON and convert to dict

    print("Building forward index...")
    forward_index = buildForwardIndex(datasetPaths, columnLists, lexicon)

    print(f"Saving forward index to {outputFilePath}...")
    saveForwardIndexToJSON(forward_index, outputFilePath)

    end = time.time()
    print("Forward index built and saved successfully.")
    print(f"Time taken: {end - start:.2f} seconds")
