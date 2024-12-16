import os
import time
from src.Barrels.RangeBarrelMaker import createBarrels
from src.Barrels.HashBarrelMaker import createHashedBarrels

# Main execution
if __name__ == "__main__":
    invertedIndexPath = os.path.join('../..', 'data', 'InvertedIndexData', 'SampleTesting', 'InvertedIndex_5000.json')


    # For Testing Range Barrels
    barrelOutputDirectory = os.path.join('../..', 'data', 'BarrelData', 'SampleTesting', 'Barrels', 'Barrels_5000')
    metadataPath = os.path.join('../..', 'data', 'BarrelData', 'SampleTesting', 'PathData', 'barrel_metadata_5000.json')

    targetBarrelSize = 10_000  # Maximum number of DocumentIDs per barrel
    tolerance = 500  # Allowable range for barrel sizes

    start = time.time()
    print("Creating Ranged barrels...")
    createBarrels(invertedIndexPath, barrelOutputDirectory, metadataPath, targetBarrelSize, tolerance)
    end = time.time()
    print("Barrels created successfully.")
    print(f"Time taken: {end - start:.6f} seconds")



    # For Testing Hashed Barrels
    # barrelOutputDirectory = os.path.join('../..', 'data', 'BarrelData', 'Testing', 'Barrels', 'Barrels_GlobalEnglish2_Hashed')
    # metadataPath = os.path.join('../..', 'data', 'BarrelData', 'Testing', 'PathData', 'barrel_metadata_GlobalEnglish2_Hashed.json')
    #
    # numBarrels = 2000  # Number of barrels
    #
    # start = time.time()
    # print("Creating hashed barrels...")
    # createHashedBarrels(invertedIndexPath, barrelOutputDirectory, metadataPath, numBarrels)
    # end = time.time()
    # print("Barrels created successfully.")
    # print(f"Time taken: {end - start:.6f} seconds")

