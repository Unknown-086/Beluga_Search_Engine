import orjson
from collections import defaultdict
import json
import pandas as pd
import os
from src.ForwardIndex.ForwardIndexBuilder import buildForwardIndex, saveForwardIndexToJSON
from src.Lexicon.TextPreprocess import preprocessText

def updateLexiconWithUserContent(userDatasetPath, existingLexiconPath, columnList):
    """
    Update existing lexicon with new words from user content.
    :param userDatasetPath: Path to user content dataset
    :param existingLexiconPath: Path to existing lexicon JSON
    :param columnList: List of columns to process from user dataset
    """
    print(f"Loading existing lexicon from: {existingLexiconPath}")
    try:
        with open(existingLexiconPath, 'rb') as f:
            lexicon = orjson.loads(f.read())
        
        # Convert to defaultdict with max ID + 1 as start
        updatedLexicon = defaultdict(lambda: len(updatedLexicon) + 1)
        updatedLexicon.update(lexicon)
        
        print(f"Processing user dataset: {userDatasetPath}")
        try:
            df = pd.read_csv(userDatasetPath)
            for column in columnList:
                if column not in df.columns:
                    print(f"Warning: Column '{column}' not found in user dataset")
                    continue

                # Fill missing values and preprocess
                df[column] = df[column].fillna('')
                df[column] = df[column].apply(preprocessText)

                # Update lexicon with new words
                for text in df[column]:
                    words = set(text)  # Avoid duplicates
                    new_words = words - set(lexicon.keys())
                    updatedLexicon.update({word: updatedLexicon[word] for word in new_words})

            # Save updated lexicon
            with open(existingLexiconPath, 'wb') as f:
                f.write(orjson.dumps(dict(updatedLexicon), option=orjson.OPT_INDENT_2))

            new_words_count = len(updatedLexicon) - len(lexicon)
            print(f"Lexicon updated. Added {new_words_count} new words.")
            return dict(updatedLexicon)

        except Exception as e:
            print(f"Error processing user dataset: {e}")
            return lexicon

    except Exception as e:
        print(f"Error loading existing lexicon: {e}")
        return None
    

def calculate_rank(word_data, metadata):
    """Calculate rank for word in document"""
    # Add ranking constants
    weights = {
        "title": 1.0,
        "description": 0.5,
        "content": 0.3,
        "frequency": 0.2
    }
    
    rank = 0
    if word_data.get("in_title", False):
        rank += weights["title"]
    if word_data.get("in_description", False):
        rank += weights["description"]
    
    frequency = word_data.get("frequency", 0)
    rank += frequency * weights["frequency"]
    
    # Length normalization
    doc_length = len(metadata.get("content", ""))
    if doc_length > 0:
        rank *= (1.0 / (0.25 + 0.75 * (doc_length / 500)))
    
    return round(rank, 4)


def updateBarrelsWithUserContent(forward_index_path, barrels_dir, metadata_path):
    """Update existing barrels with new user content"""
    try:
        # Load forward index
        if not os.path.exists(forward_index_path):
            raise FileNotFoundError(f"Forward index not found: {forward_index_path}")
            
        # Load metadata
        if not os.path.exists(metadata_path):
            raise FileNotFoundError(f"Barrel metadata not found: {metadata_path}")
            
        with open(forward_index_path, 'r') as f:
            forward_index = json.load(f)
            
        with open(metadata_path, 'r') as f:
            barrel_metadata = json.load(f)
            
        num_barrels = max(int(key) for key in barrel_metadata.keys())
            
        for doc_id, doc_data in forward_index.items():
            metadata = doc_data.get("metadata", {})
            
            for word_id, word_data in doc_data.get("words", {}).items():
                rank = calculate_rank(word_data, metadata)
                barrel_num = int(word_id) % num_barrels + 1
                barrel_path = barrel_metadata[str(barrel_num)]
                
                # Ensure barrel directory exists
                os.makedirs(os.path.dirname(barrel_path), exist_ok=True)
                
                # Load or create barrel
                if os.path.exists(barrel_path):
                    with open(barrel_path, 'r') as f:
                        barrel_data = json.load(f)
                else:
                    barrel_data = {}
                    
                word_id_str = str(word_id)
                if word_id_str in barrel_data:
                    barrel_data[word_id_str][doc_id] = rank
                    barrel_data[word_id_str] = dict(
                        sorted(
                            barrel_data[word_id_str].items(),
                            key=lambda x: float(x[1]),
                            reverse=True
                        )
                    )
                else:
                    barrel_data[word_id_str] = {doc_id: rank}
                
                with open(barrel_path, 'w') as f:
                    json.dump(barrel_data, f, indent=2)
                    
        return True
        
    except Exception as e:
        print(f"Error updating barrels: {e}")
        return False    

def updateContent(userDatasetPath, existingLexiconPath, forwardIndexPath, barrelsPath, metadataPath):
    try:
        print("Starting content update process...")
        
        # 1. Update lexicon with new words
        columnList = ['title', 'description', 'content', 'url']
        updatedLexicon = updateLexiconWithUserContent(
            userDatasetPath, 
            existingLexiconPath, 
            columnList
        )
        if not updatedLexicon:
            return False
            
        # 2. Build forward index for user content
        print("Building forward index for user content...")
        # Wrap path in list to match ForwardIndexBuilder format
        forwardIndex = buildForwardIndex(
            [userDatasetPath],  # Pass as list
            [columnList],       # Pass as list of lists
            updatedLexicon
        )
        
        # 3. Save forward index
        print("Saving user forward index...")
        saveForwardIndexToJSON(forwardIndex, forwardIndexPath)
        
        # 4. Create barrel metadata if doesn't exist
        if not os.path.exists(metadataPath):
            print("Creating barrel metadata...")
            os.makedirs(os.path.dirname(metadataPath), exist_ok=True)
            num_barrels = 100  # Default number of barrels
            metadata = {
                str(i): os.path.join(barrelsPath, f"barrel_{i}.json")
                for i in range(1, num_barrels + 1)
            }
            with open(metadataPath, 'w') as f:
                json.dump(metadata, f, indent=2)
        
        # 5. Update barrels
        print("Updating barrels...")
        success = updateBarrelsWithUserContent(
            forwardIndexPath,
            barrelsPath,
            metadataPath
        )
        
        if success:
            print("Content update completed successfully")
            return True
        else:
            print("Failed to update barrels")
            return False
            
    except Exception as e:
        print(f"Error during content update: {e}")
        return False