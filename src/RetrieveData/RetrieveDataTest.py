import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

import os
import time
from src.RetrieveData.RetrieveData import retrieveDocIds
from src.RetrieveData.RetrieveDataContentGPU import get_content, clear_cache


if __name__ == "__main__":

#     word = "fast"
#     lexiconPath = os.path.join('../..', 'data', 'Lexicons', 'SampleTesting', 'Lexicon_5000.json')
#     hashedMetadataPath = os.path.join('../..', 'data', 'BarrelData', 'SampleTesting', 'PathData', 'barrel_Hashed_metadata_5000.json')
#     # rangedMetadataPath = os.path.join('../..', 'data', 'BarrelData', 'Testing', 'PathData', 'Barrels_GlobalNews_English2_Metadata.json')
#
#     start = time.time()
#     barrelPath, DocIDList = retrieveDocIds(word, lexiconPath, hashedMetadataPath)
#     end = time.time()
#     print(f"Barrel Path: {barrelPath}")
#     print(f"Document IDs: {DocIDList}")
#     print(f"Number of Document IDs: {len(DocIDList)}")
#     print(f"Time taken: {end - start:.6f} seconds.")


    word = "obama"
    lexiconPath = os.path.join('../..', 'data', 'Lexicons', 'SampleTesting', 'Lexicon_5000.json')
    hashedMetadataPath = os.path.join('../..', 'data', 'BarrelData', 'SampleTesting', 'PathData', 'barrel_Hashed_metadata_5000.json')

    start = time.time()
    barrelPath, DocIDList = retrieveDocIds(word, lexiconPath, hashedMetadataPath)
    print(f"Barrel Path: {barrelPath}")
    print(f"Document IDs: {DocIDList}")
    print(f"Number of Document IDs: {len(DocIDList)}")

    # Retrieve and display content for each DocID
    content = []

    content = get_content(DocIDList)

    end = time.time()
    for content in content:
        print(f"Content for DocID {content.get('docId')}: {content}")

    print(f"Time taken: {end - start:.6f} seconds.")
    # Clear GPU memory cache
    clear_cache()