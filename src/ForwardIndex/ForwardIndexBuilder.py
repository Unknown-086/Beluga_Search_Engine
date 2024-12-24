import pandas as pd
import json
from collections import defaultdict
from src.Lexicon.TextPreprocess import preprocessText


def buildForwardIndex(datasetPaths, columnLists, lexicon):
    """
    Build a forward index with Word IDs based on the lexicon.
    :param datasetPaths: List of paths to the datasets
    :param columnLists: List of lists containing column names to process for each dataset
    :param lexicon: Dictionary mapping words to their unique Word IDs
    :return: Forward index dictionary
    """
    forward_index = defaultdict(list)

    for datasetPath, columnList in zip(datasetPaths, columnLists):
        print(f"Processing dataset: {datasetPath}")
        try:
            for chunk in pd.read_csv(datasetPath, chunksize=10_000):
                if 'DocID' not in chunk.columns:
                    print(f"Error: 'DocID' column not found in the dataset '{datasetPath}'.")
                    continue

                for _, row in chunk.iterrows():
                    doc_id = row['DocID']
                    combined_text = []

                    # Combine and preprocess text from all specified columns
                    for column in columnList:
                        if column in row and pd.notna(row[column]):
                            combined_text.extend(preprocessText(row[column]))

                    # Replace words with Word IDs
                    word_ids_with_positions = [
                        (lexicon[word], position) for position, word in enumerate(combined_text) if word in lexicon
                    ]

                    # Add to the forward index
                    forward_index[doc_id].extend(word_ids_with_positions)

        except FileNotFoundError:
            print(f"Error: File '{datasetPath}' not found.")
        except Exception as e:
            print(f"Unexpected error while processing '{datasetPath}': {e}")

    return forward_index



def saveForwardIndexToJSON(forward_index, output_file_path):
    """
    Save the forward index to a JSON file using the standard JSON library.
    :param forward_index: The forward index dictionary
    :param output_file_path: Path to the output JSON file
    """
    try:
        # Prepare forward index for JSON serialization
        json_ready_index = {
            str(doc_id): [[word_id, position] for word_id, position in words_with_positions]
            for doc_id, words_with_positions in forward_index.items()
        }

        # Save to JSON file
        with open(output_file_path, 'w') as json_file:
            json.dump(json_ready_index, json_file, indent=2)

        print(f"Forward index saved successfully to {output_file_path}")
    except Exception as e:
        print(f"Error saving forward index to JSON file: {e}")






# import numpy as np
# from numba import cuda
# import pandas as pd
# import json
# import os
# from collections import defaultdict
# from src.Lexicon.TextPreprocess import preprocessText
#
#
# @cuda.jit
# def process_text_gpu(text_array, word_ids, lexicon_keys, lexicon_vals, positions):
#     idx = cuda.grid(1)
#     if idx < text_array.shape[0]:
#         word = text_array[idx]
#         for i in range(lexicon_keys.shape[0]):
#             if word == lexicon_keys[i]:
#                 word_ids[idx] = lexicon_vals[i]
#                 positions[idx] = idx
#                 break
#
#
# def buildForwardIndexGPU(datasetPaths, columnLists, lexicon):
#     forward_index = defaultdict(list)
#     BATCH_SIZE = 1024 * 4  # GPU threads batch size
#
#     # Convert lexicon to arrays for GPU
#     lexicon_keys = np.array(list(lexicon.keys()), dtype=np.str_)
#     lexicon_vals = np.array(list(lexicon.values()), dtype=np.int32)
#
#     # Copy lexicon to GPU
#     d_lexicon_keys = cuda.to_device(lexicon_keys)
#     d_lexicon_vals = cuda.to_device(lexicon_vals)
#
#     for datasetPath, columns in zip(datasetPaths, columnLists):
#         print(f"Processing {datasetPath}")
#         df = pd.read_csv(datasetPath, chunksize=BATCH_SIZE)
#
#         for chunk in df:
#             for _, row in chunk.iterrows():
#                 doc_id = int(row['DocID'])
#                 text = []
#
#                 # Combine text from specified columns
#                 for col in columns:
#                     if col in row and pd.notna(row[col]):
#                         text.extend(preprocessText(str(row[col])))
#
#                 if not text:
#                     continue
#
#                 # Convert text to array
#                 text_array = np.array(text)
#                 word_ids = np.zeros(len(text), dtype=np.int32)
#                 positions = np.zeros(len(text), dtype=np.int32)
#
#                 # Copy to GPU
#                 d_text = cuda.to_device(text_array)
#                 d_word_ids = cuda.to_device(word_ids)
#                 d_positions = cuda.to_device(positions)
#
#                 # Configure kernel
#                 threadsperblock = 256
#                 blockspergrid = (text_array.shape[0] + threadsperblock - 1) // threadsperblock
#
#                 # Launch kernel
#                 process_text_gpu[blockspergrid, threadsperblock](
#                     d_text, d_word_ids, d_lexicon_keys, d_lexicon_vals, d_positions
#                 )
#
#                 # Get results
#                 word_ids = d_word_ids.copy_to_host()
#                 positions = d_positions.copy_to_host()
#
#                 # Add to forward index
#                 for wid, pos in zip(word_ids, positions):
#                     if wid > 0:
#                         forward_index[doc_id].append((wid, pos))
#
#     return forward_index




# @cuda.jit
# def transform_data_gpu(doc_ids, word_positions, output):
#     """Transform word-position pairs in parallel"""
#     idx = cuda.grid(1)
#     if idx < doc_ids.shape[0]:
#         output[idx][0] = word_positions[idx][0]  # word_id
#         output[idx][1] = word_positions[idx][1]  # position
#
#
# def saveForwardIndexToJSONGPU(forward_index, output_file_path, batch_size=10000):
#     try:
#         # Create temporary storage for batches
#         temp_dir = os.path.dirname(output_file_path)
#         temp_files = []
#
#         # Process in batches
#         doc_ids = list(forward_index.keys())
#         for i in range(0, len(doc_ids), batch_size):
#             batch_docs = doc_ids[i:i + batch_size]
#
#             # Prepare batch data
#             batch_data = {}
#             for doc_id in batch_docs:
#                 words_positions = forward_index[doc_id]
#                 if words_positions:
#                     # Convert to numpy arrays
#                     words_arr = np.array(words_positions, dtype=np.int32)
#
#                     # Allocate GPU memory
#                     d_words = cuda.to_device(words_arr)
#                     d_output = cuda.device_array_like(words_arr)
#
#                     # Configure kernel
#                     threadsperblock = 256
#                     blockspergrid = (words_arr.shape[0] + threadsperblock - 1) // threadsperblock
#
#                     # Transform data on GPU
#                     transform_data_gpu[blockspergrid, threadsperblock](
#                         cuda.to_device(np.array([doc_id] * len(words_positions))),
#                         d_words,
#                         d_output
#                     )
#
#                     # Get results back
#                     result = d_output.copy_to_host()
#                     batch_data[str(doc_id)] = result.tolist()
#
#             # Write batch to temporary file
#             temp_file = f"{output_file_path}.{i}.tmp"
#             with open(temp_file, 'w') as f:
#                 json.dump(batch_data, f)
#             temp_files.append(temp_file)
#
#         # Merge temporary files
#         with open(output_file_path, 'w') as outfile:
#             outfile.write('{')
#             for i, temp_file in enumerate(temp_files):
#                 with open(temp_file, 'r') as infile:
#                     content = infile.read().strip('{}')
#                     if i > 0:
#                         outfile.write(',')
#                     outfile.write(content)
#                 os.remove(temp_file)
#             outfile.write('}')
#
#         print(f"Forward index saved successfully to {output_file_path}")
#
#     except Exception as e:
#         print(f"Error saving forward index to JSON file: {e}")
#         raise