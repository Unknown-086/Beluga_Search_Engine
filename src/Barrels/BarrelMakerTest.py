import os
import time
from src.Barrels.BarrelMaker1 import createBarrels

# Main execution
if __name__ == "__main__":
    invertedIndexPath = os.path.join('../..', 'data', 'InvertedIndexData', 'SampleTesting', 'InvertedIndex_5000.json')
    barrelOutputDirectory = os.path.join('../..', 'data', 'BarrelData', 'SampleTesting', 'Barrels', 'Barrels_5000')
    metadataPath = os.path.join('../..', 'data', 'BarrelData', 'SampleTesting', 'PathData', 'barrel_metadata_5000.json')

    targetBarrelSize = 50_000  # Maximum number of DocumentIDs per barrel
    tolerance = 1_000  # Allowable range for barrel sizes

    start = time.time()
    print("Creating barrels...")
    createBarrels(invertedIndexPath, barrelOutputDirectory, metadataPath, targetBarrelSize, tolerance)
    end = time.time()

    print("Barrels created successfully.")
    print(f"Time taken: {end - start:.6f} seconds")
