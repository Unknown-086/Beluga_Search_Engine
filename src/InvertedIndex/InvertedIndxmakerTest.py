import os
import time
from InvertedIndexBuilder import buildInvertedIndex

# Main execution
if __name__ == "__main__":
    forwardIndexPath = os.path.join('../..', 'data', 'ForwardIndexData', 'ForwardIndex_GlobalNews_English2.json')
    invertedIndexPath = os.path.join('../..', 'data', 'InvertedIndexData', 'InvertedIndex_GlobalNews_English2.json')

    start = time.time()
    print("Building inverted index...")
    buildInvertedIndex(forwardIndexPath, invertedIndexPath)
    end = time.time()
    print(f"Inverted index built and saved successfully.")
    print(f"Time taken: {end - start:.2f} seconds")