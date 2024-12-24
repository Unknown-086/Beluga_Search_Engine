import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

import os
import time
from src.InvertedIndex.InvertedIndexBuilder import buildInvertedIndex

# Main execution
if __name__ == "__main__":
    forwardIndexPath = os.path.join('../..', 'data', 'ForwardIndexData', 'Testing', 'ForwardIndex_Testing.json')
    invertedIndexPath = os.path.join('../..', 'data', 'InvertedIndexData', 'Testing', 'InvertedIndex_Testing.json')

    start = time.time()
    print("Building inverted index...")
    buildInvertedIndex(forwardIndexPath, invertedIndexPath)
    end = time.time()
    print(f"Inverted index built and saved successfully.")
    print(f"Time taken: {end - start:.6f} seconds")