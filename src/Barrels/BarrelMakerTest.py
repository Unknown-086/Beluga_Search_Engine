import os
import time
from src.Barrels.RangeBarrelMaker import createBarrels
from src.Barrels.HashBarrelMaker import createHashedBarrels

# Main execution
if __name__ == "__main__":
    invertedIndexPath = os.path.join('../..', 'data', 'InvertedIndexData', 'SampleTesting', 'InvertedIndex_5000.json')


    # For Testing Range Barrels
    # barrelOutputDirectory = os.path.join('../..', 'data', 'BarrelData', 'SampleTesting', 'Barrels', 'Barrels_5000')
    # metadataPath = os.path.join('../..', 'data', 'BarrelData', 'SampleTesting', 'PathData', 'barrel_metadata_5000.json')
    #
    # targetBarrelSize = 10_000  # Maximum number of DocumentIDs per barrel
    # tolerance = 500  # Allowable range for barrel sizes
    #
    # start = time.time()
    # print("Creating Ranged barrels...")
    # createBarrels(invertedIndexPath, barrelOutputDirectory, metadataPath, targetBarrelSize, tolerance)
    # end = time.time()
    # print("Barrels created successfully.")
    # print(f"Time taken: {end - start:.6f} seconds")


    ### I will be using this Hash Based Barrels for My Project for now
    # For Testing Hashed Barrels
    barrelOutputDirectory = os.path.join('../..', 'data', 'BarrelData', 'SampleTesting', 'Barrels', 'Barrels_Hashed_5000')
    metadataPath = os.path.join('../..', 'data', 'BarrelData', 'SampleTesting', 'PathData', 'barrel_Hashed_metadata_5000.json')

    ### Still to get the Optimal number!!!
    numBarrels = 2000  # Number of barrels

    start = time.time()
    print("Creating hashed barrels...")
    createHashedBarrels(invertedIndexPath, barrelOutputDirectory, metadataPath, numBarrels)
    end = time.time()
    print("Barrels created successfully.")
    print(f"Time taken: {end - start:.6f} seconds")

