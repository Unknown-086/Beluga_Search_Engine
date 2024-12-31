import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

import os
import time
from src.ContentAddition.ContentAdditionToExistingData import updateContent
from src.ForwardIndex.ForwardIndexBuilder import buildForwardIndex, saveForwardIndexToJSON


# Define base paths
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
data_dir = os.path.join(base_dir, 'data')

# Update paths to ensure directories exist
paths = {
    "userDataset": os.path.join(data_dir, 'UserContent', 'UserContent.csv'),
    "lexicon": os.path.join(data_dir, 'Lexicons', 'Testing', 'Lexicon_Testing_User.json'),
    "forwardIndex": os.path.join(data_dir, 'ForwardIndexData', 'Testing', 'UserForwardIndex.json'),
    "barrels": os.path.join(data_dir, 'BarrelData', 'Testing', 'Barrels', 'Barrels_Testing'),  # Simplified path
    "metadata": os.path.join(data_dir, 'BarrelData', 'Testing', 'PathData', 'Barrels_Testing_Metadata.json')  # Simplified path
}

# Create directories before running
for path in paths.values():
    dir_path = os.path.dirname(path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

startTime = time.time()

success = updateContent(
    paths["userDataset"],
    paths["lexicon"],
    paths["forwardIndex"],
    paths["barrels"],
    paths["metadata"]
)

endTime = time.time()

if success:
    print(f"Content update completed in {endTime - startTime:.6f} seconds")
else:
    print("Content update failed")
