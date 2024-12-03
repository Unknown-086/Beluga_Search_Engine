import os
import time
from src.Lexicon.LexiconBuilder import saveLexiconToJSON, buildLexicon


# Test file for LexiconBuilder.py
if __name__ == "__main__":
    datasetPaths = [
        os.path.join('../..', 'data', 'SampleDatasets_ForTesting', 'GlobalNewsDataset_Sample_1000.csv'),
        os.path.join('../..', 'data', 'SampleDatasets_ForTesting', 'RedditDataset_Sample_1000.csv'),
        os.path.join('../..', 'data', 'SampleDatasets_ForTesting', 'WeeklyNewsDataset_Aug17_1000.csv'),
        os.path.join('../..', 'data', 'SampleDatasets_ForTesting', 'WeeklyNewsDataset_Aug18_1000.csv')
    ]

    columnLists = [
        [ 'published_at', 'source_name', 'author', 'title', 'description', 'content', 'category', 'full_content' ],
        [ 'date', 'subreddit', 'title', 'author', 'domain' ],
        [ 'publish_time', 'feed_code', 'headline_text'] ,
        [ 'publish_time', 'feed_code', 'headline_text' ]
    ]

    startTime = time.time()
    lexiconOutputPath = os.path.join('../..', 'data', 'Lexicons', 'SampleTesting', 'Lexicon_1000.json')

    print("Building the combined lexicon...")
    lexicon = buildLexicon(datasetPaths, columnLists)

    print(f"Saving the combined lexicon to {lexiconOutputPath}...")
    saveLexiconToJSON(lexicon, lexiconOutputPath)
    endTime = time.time()
    print(f"Combined lexicon built and saved successfully. Total unique words: {len(lexicon)}")
    print(f"Time taken: {endTime - startTime:.6f} seconds")
