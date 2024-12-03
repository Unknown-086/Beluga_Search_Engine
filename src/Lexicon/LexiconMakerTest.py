import os
import time
from src.Lexicon.LexiconBuilder import saveLexiconToJSON, buildLexicon


# Test file for LexiconBuilder.py
if __name__ == "__main__":
    datasetsPaths = [
        os.path.join('../..', 'data', 'FilteredDatasets', 'ModifiedGlobalNewsDataset13_English.csv')
    ]

    columnLists = [
        [ 'source_name', 'author', 'title', 'description', 'content', 'category', 'full_content']
    ]

    startTime = time.time()
    lexiconOutputPath = os.path.join('../..', 'data', 'Lexicons', 'LexiconModifiedGlobalNewsDataset13_7.json')

    print("Building the combined lexicon...")
    lexicon = buildLexicon(datasetsPaths, columnLists)

    print(f"Saving the combined lexicon to {lexiconOutputPath}...")
    saveLexiconToJSON(lexicon, lexiconOutputPath)
    endTime = time.time()
    print(f"Combined lexicon built and saved successfully. Total unique words: {len(lexicon)}")
    print(f"Time taken: {endTime - startTime:.2f} seconds")
