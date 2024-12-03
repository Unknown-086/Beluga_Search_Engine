import os
import time
from src.InvertedIndex.InvertedIndexBuilder import buildInvertedIndex

# Main execution
if __name__ == "__main__":
    forwardIndexPath = os.path.join('../..', 'data', 'ForwardIndexData', 'SampleTesting', 'ForwardIndex_5000.json')
    invertedIndexPath = os.path.join('../..', 'data', 'InvertedIndexData', 'SampleTesting', 'InvertedIndex_5000.json')

    start = time.time()
    print("Building inverted index...")
    buildInvertedIndex(forwardIndexPath, invertedIndexPath)
    end = time.time()
    print(f"Inverted index built and saved successfully.")
    print(f"Time taken: {end - start:.6f} seconds")