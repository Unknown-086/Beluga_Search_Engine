import os
import time
from src.RetrieveData.RetrieveData import retrieveDocIds


def test_retrieve_doc_ids(word, lexicon_path, hashed_metadata_path, iterations=100):
    total_time = 0
    for _ in range(iterations):
        start = time.time()
        barrel_path, doc_id_list = retrieveDocIds(word, lexicon_path, hashed_metadata_path)
        end = time.time()
        total_time += (end - start)

    avg_time = total_time / iterations
    return avg_time, barrel_path, doc_id_list


if __name__ == "__main__":
    word = "hadi"
    lexiconPath = os.path.join('../..', 'data', 'Lexicons', 'Testing', 'LexiconGlobalNewsDataset13_English2_Testing.json')
    hashedMetadataPath = os.path.join('../..', 'data', 'BarrelData', 'Testing', 'PathData', 'Barrels_GlobalNews_English2_Hashed_Metadata.json')
    # rangedMetadataPath = os.path.join('../..', 'data', 'BarrelData', 'Testing', 'PathData', 'Barrels_GlobalNews_English2_Metadata.json')

    iterations = 100
    avg_time, barrel_path, doc_id_list = test_retrieve_doc_ids(word, lexiconPath, hashedMetadataPath, iterations)

    print(f"Barrel Path: {barrel_path}")
    print(f"Document IDs: {doc_id_list}")
    print(f"Number of Document IDs: {len(doc_id_list)}")
    print(f"Average time taken over {iterations} iterations: {avg_time:.6f} seconds.")