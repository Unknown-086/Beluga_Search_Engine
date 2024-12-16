import os
import time
from src.Barrels.BarrelMaker1 import createBarrels
from src.Barrels.BarrelMaker2 import createHashedBarrels

# Main execution
if __name__ == "__main__":
    invertedIndexPath = os.path.join('../..', 'data', 'InvertedIndexData', 'Testing', 'InvertedIndex_GlobalNews_English2.json')


    barrelOutputDirectory = os.path.join('../..', 'data', 'BarrelData', 'Testing', 'Barrels', 'Barrels_GlobalEnglish2')
    metadataPath = os.path.join('../..', 'data', 'BarrelData', 'Testing', 'PathData', 'barrel_metadata_GlobalEnglish2.json')

    targetBarrelSize = 10_000  # Maximum number of DocumentIDs per barrel
    tolerance = 500  # Allowable range for barrel sizes

    start = time.time()
    print("Creating barrels...")
    createBarrels(invertedIndexPath, barrelOutputDirectory, metadataPath, targetBarrelSize, tolerance)
    end = time.time()

    print("Barrels created successfully.")
    print(f"Time taken: {end - start:.6f} seconds")



    # For Testing Hashed Barrels
    barrelOutputDirectory = os.path.join('../..', 'data', 'BarrelData', 'Testing', 'Barrels_GlobalEnglish2_Hashed')
    metadataPath = os.path.join('../..', 'data', 'BarrelData', 'Testing', 'PathData', 'barrel_metadata_GlobalEnglish2_Hashed.json')

    numBarrels = 2000  # Number of barrels

    start = time.time()
    print("Creating hashed barrels...")
    createHashedBarrels(invertedIndexPath, barrelOutputDirectory, metadataPath, numBarrels)
    end = time.time()
    print("Barrels created successfully.")
    print(f"Time taken: {end - start:.6f} seconds")

