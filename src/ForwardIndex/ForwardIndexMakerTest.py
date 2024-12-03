import os
import time
import orjson
from src.ForwardIndex.ForwardIndexBuilder import buildForwardIndex, saveForwardIndexToJSON


# Main execution
if __name__ == "__main__":
    # File paths and configuration
    datasetPaths = [
        os.path.join('../..', 'data', 'SampleDatasets_ForTesting', 'GlobalNewsDataset_Sample_5000.csv'),
        os.path.join('../..', 'data', 'SampleDatasets_ForTesting', 'RedditDataset_Sample_5000.csv'),
        os.path.join('../..', 'data', 'SampleDatasets_ForTesting', 'WeeklyNewsDataset_Aug17_5000.csv'),
        os.path.join('../..', 'data', 'SampleDatasets_ForTesting', 'WeeklyNewsDataset_Aug18_5000.csv')
    ]

    columnLists = [
        [ 'published_at', 'source_name', 'author', 'title', 'description', 'content', 'category', 'full_content' ],
        [ 'date', 'subreddit', 'title', 'author' ],
        [ 'publish_time', 'feed_code', 'headline_text'] ,
        [ 'publish_time', 'feed_code', 'headline_text' ]
    ]
    lexiconFilePath = os.path.join('../..', 'data', 'Lexicons', 'SampleTesting', 'Lexicon_5000.json')
    outputFilePath = os.path.join('../..', 'data', 'ForwardIndexData', 'SampleTesting', 'ForwardIndex_5000.json')

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
