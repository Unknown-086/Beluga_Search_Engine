import json
import os
import time
from src.Barrels.BarrelMakerRange import getBarrelForRanged
from src.Barrels.BarrelMakerHash import getBarrelForHashed




# Example Usage
if __name__ == "__main__":
    word_id = 65000

    # Hashed Barrel Example
    # hashedMetadataPath = os.path.join('../..', 'data', 'BarrelData', 'Testing', 'PathData', 'barrel_metadata_GlobalEnglish2_Hashed.json')
    # numBarrels = 2000
    # start = time.time()
    # barrel_path, doc_ids = getBarrelForHashed(word_id, hashedMetadataPath, numBarrels)
    # end = time.time()
    # print(f"Hashed Barrel Path: {barrel_path}, DocumentIDs: {doc_ids}")
    # print(f"Time taken: {end - start:.6f} seconds")
    #

    # Ranged Barrel Example
    rangedMetadataPath = os.path.join('../..', 'data', 'BarrelData', 'Testing', 'PathData', 'barrel_metadata_GlobalEnglish2.json')
    start = time.time()
    barrel_path, doc_ids = getBarrelForRanged(word_id, rangedMetadataPath)
    end = time.time()
    print(f"Ranged Barrel Path: {barrel_path}, DocumentIDs: {doc_ids}")
    print(f'Time taken: {end - start:.6f} seconds')