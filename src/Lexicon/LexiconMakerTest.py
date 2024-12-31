import os
import time
from src.Lexicon.LexiconBuilder import saveLexiconToJSON, buildLexicon


# Test file for LexiconBuilder.py
if __name__ == "__main__":
    datasetPaths = [
        # os.path.join('../..', 'data', 'Testing', 'ModifiedGlobalNewsDataset13_Language_English_Langauge.csv')
        os.path.join('../..', 'data', 'FilteredDatasets', 'ModifiedGlobalNewsDataset13_Language_English_Langauge.csv'),
        os.path.join('../..', 'data', 'FilteredDatasets', 'ModifiedReddit_database11_English.csv'),
        os.path.join('../..', 'data', 'FilteredDatasets', 'ModifiedNews-week-17aug8_English.csv'),
        os.path.join('../..', 'data', 'FilteredDatasets', 'ModifiedNews-week-18aug7_English.csv')
    ]

    columnLists = [
        [ 'published_at', 'source_name', 'author', 'title', 'description', 'url', 'url_to_image', 'content', 'category', 'full_content' ],
        [ 'created_date', 'subreddit', 'title', 'author', 'full_link', 'content'],
        [ 'publish_time', 'feed_code', 'source_url', 'headline_text'] ,
        [ 'publish_time', 'feed_code', 'source_url', 'headline_text' ]
    ]

    startTime = time.time()
    lexiconOutputPath = os.path.join('../..', 'data', 'Lexicons', 'Testing', 'Lexicon_Testing.json')

    print("Building the combined lexicon...")
    lexicon = buildLexicon(datasetPaths, columnLists)

    print(f"Saving the combined lexicon to {lexiconOutputPath}...")
    saveLexiconToJSON(lexicon, lexiconOutputPath)
    endTime = time.time()
    print(f"Combined lexicon built and saved successfully. Total unique words: {len(lexicon)}")
    print(f"Time taken: {endTime - startTime:.6f} seconds")
