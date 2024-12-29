import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

import os
import time
from src.InvertedIndex.InvertedIndexBuilder import buildInvertedIndexWithRank, sortInvertedIndexByRank

# Main execution
if __name__ == "__main__":

    forwardIndexPaths = [
        os.path.join('../..', 'data', 'ForwardIndexData', 'Testing', 'ForwardIndex_GlobalNews_Testing.json'),
        os.path.join('../..', 'data', 'ForwardIndexData', 'Testing', 'ForwardIndex_Reddit_Testing_.json'),
        os.path.join('../..', 'data', 'ForwardIndexData', 'Testing', 'ForwardIndex_WeeklyNews_Testing.json')
    ]

    invertedIndexPath = os.path.join('../..', 'data', 'InvertedIndexData', 'Testing', 'InvertedIndex_Testing.json')

    start = time.time()
    print("Building inverted index...")
    buildInvertedIndexWithRank(forwardIndexPaths, invertedIndexPath)
    end = time.time()
    print(f"Inverted index built and saved successfully.")
    print(f"Time taken: {end - start:.6f} seconds")


    sortedInvertedIndexPath = os.path.join('../..', 'data', 'InvertedIndexData', 'Testing', 'InvertedIndex_Sorted_Testing.json')

    print("\n")
    start = time.time()
    print("Sorting inverted index...")
    sortInvertedIndexByRank(invertedIndexPath, sortedInvertedIndexPath)
    end = time.time()
    print(f"Inverted index sorted and saved successfully.")
    print(f"Time taken: {end - start:.6f} seconds")