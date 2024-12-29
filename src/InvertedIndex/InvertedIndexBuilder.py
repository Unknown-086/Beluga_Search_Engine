import os
import json
from collections import defaultdict

def buildInvertedIndexWithRank(forward_index_paths, output_file_path):
    """Build inverted index with document-aware ranking"""
    
    # Ranking configuration
    weights = {
        "title_only": {"title": 1.0, "freq": 0.3},
        "with_content": {"title": 0.5, "freq": 0.1}
    }
    
    def calculate_length_norm(doc_length, has_content):
        if not has_content or doc_length <= 50:
            return 1.5  # Boost very short/title-only docs
        elif doc_length <= 200:
            return 1.2  # Small boost for short docs
        else:
            return 1.0 / (0.25 + 0.75 * (doc_length / 500))
    
    inverted_index = defaultdict(dict)
    total_docs = 0
    forward_index = {}

    try:
        # Load and combine all forward indices
        print("Loading and combining forward indices...")
        for idx, forward_path in enumerate(forward_index_paths, 1):
            if not os.path.exists(forward_path):
                raise FileNotFoundError(f"Forward index not found: {forward_path}")
                
            print(f"Loading forward index {idx}/{len(forward_index_paths)}: {forward_path}")
            with open(forward_path, 'r') as forward_file:
                forward_data = json.load(forward_file)
                forward_index.update(forward_data)
            print(f"Added {len(forward_data)} documents from {forward_path}")

        print(f"\nTotal documents in combined forward index: {len(forward_index)}")
        print("Building inverted index with rank...")
        
        for doc_id, doc_data in forward_index.items():
            try:
                # Get document metadata
                metadata = doc_data.get("metadata", {})
                has_content = metadata.get("has_content", False)
                doc_length = metadata.get("doc_length", 0)
                length_norm = calculate_length_norm(doc_length, has_content)
                w = weights["with_content"] if has_content else weights["title_only"]
                
                # Process words
                for word_id, word_data in doc_data.get("words", {}).items():
                    rank = 0
                    frequency = word_data.get("frequency", 0)
                    
                    if word_data.get("in_title", False):
                        rank += w["title"]
                        frequency -= 1
                    
                    rank += frequency * w["freq"]
                    rank *= length_norm
                    
                    inverted_index[word_id][doc_id] = round(rank, 4)  # Round to 4 decimal places
                
                total_docs += 1
                if total_docs % 10000 == 0:
                    print(f"Processed {total_docs:,} documents")
                    
            except Exception as e:
                print(f"Error processing document {doc_id}: {e}")
                continue

        print(f"\nProcessed total of {total_docs:,} documents")
        print(f"Saving inverted index to {output_file_path}...")
        
        output_dir = os.path.dirname(output_file_path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        with open(output_file_path, 'w') as output_file:
            json.dump(inverted_index, output_file)

        print("Inverted index built and saved successfully.")
        
    except Exception as e:
        print(f"Error building inverted index: {e}")
        raise

    return inverted_index



def sortInvertedIndexByRank(inverted_index_path, output_path):
    """Sort document IDs by their rank in inverted index"""
    try:
        if not os.path.exists(inverted_index_path):
            raise FileNotFoundError(f"Inverted index not found: {inverted_index_path}")

        print(f"Loading inverted index from {inverted_index_path}...")
        with open(inverted_index_path, 'r') as file:
            inverted_index = json.load(file)

        total_words = len(inverted_index)
        print(f"Found {total_words:,} words to process...")
        
        print("Sorting documents by rank...")
        sorted_index = {}
        for i, (word_id, docs) in enumerate(inverted_index.items(), 1):
            try:
                # Sort docs by rank in descending order
                sorted_docs = dict(
                    sorted(
                        docs.items(), 
                        key=lambda x: float(x[1]), 
                        reverse=True
                    )
                )
                sorted_index[word_id] = sorted_docs
                
                if i % 10000 == 0:
                    print(f"Processed {i:,}/{total_words:,} words...")
                    
            except Exception as e:
                print(f"Error sorting word_id {word_id}: {e}")
                continue

        # Create output directory if needed
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        print(f"Saving sorted inverted index to {output_path}...")
        with open(output_path, 'w') as file:
            json.dump(sorted_index, file)
        
        print("Inverted index sorted and saved successfully")
        return sorted_index

    except Exception as e:
        print(f"Error sorting inverted index: {e}")
        raise