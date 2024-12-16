import os
import time

from src.RetrieveData.RetrieveData import retrieveDocIds
if __name__ == "__main__":
    word = "hadi"
    lexiconPath = os.path.join('../..', 'data', 'Lexicons', 'SampleTesting', 'Lexicon_5000.json')
    hashedMetadataPath = os.path.join('../..', 'data', 'BarrelData', 'SampleTesting', 'PathData', 'barrel_Hashed_metadata_5000.json')

    start = time.time()
    barrelPath, DocIDList = retrieveDocIds(word, lexiconPath, hashedMetadataPath)
    end = time.time()
    print(f"Barrel Path: {barrelPath}")
    print(f"Document IDs: {DocIDList}")
    print(f"Number of Document IDs: {len(DocIDList)}")
    print(f"Time taken: {end - start:.6f} seconds.")