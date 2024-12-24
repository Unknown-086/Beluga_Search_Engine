import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

import os
import time
import orjson
from src.ForwardIndex.ForwardIndexBuilder import buildForwardIndex, saveForwardIndexToJSON


# Main execution
if __name__ == "__main__":
    # File paths and configuration
    datasetPaths = [
        # os.path.join('../..', 'data', 'Testing', 'ModifiedGlobalNewsDataset13_Language_English_Langauge.csv')
        os.path.join('../..', 'data', 'FilteredDatasets', 'ModifiedGlobalNewsDataset13_Language_English_Langauge.csv'),
        os.path.join('../..', 'data', 'FilteredDatasets', 'ModifiedReddit_database11_English.csv'),
        os.path.join('../..', 'data', 'FilteredDatasets', 'ModifiedNews-week-17aug8_English.csv'),
        os.path.join('../..', 'data', 'FilteredDatasets', 'ModifiedNews-week-18aug7_English.csv')
    ]

    columnLists = [
        [ 'published_at', 'source_name', 'author', 'title', 'description', 'url', 'url_to_image', 'content', 'category', 'full_content' ],
        [ 'created_date', 'subreddit', 'title', 'author', 'full_link', 'post'],
        [ 'publish_time', 'feed_code', 'source_url', 'headline_text'] ,
        [ 'publish_time', 'feed_code', 'source_url', 'headline_text' ]
    ]


    lexiconFilePath = os.path.join('../..', 'data', 'Lexicons', 'Testing', 'Lexicon_Testing.json')
    outputFilePath = os.path.join('../..', 'data', 'ForwardIndexData', 'Testing', 'ForwardIndex_Testing.json')

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
    print(f"Time taken: {end - start:.6f} seconds")
