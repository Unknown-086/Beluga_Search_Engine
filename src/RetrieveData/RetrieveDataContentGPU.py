import os
import pandas as pd
from numba import jit, cuda
import numpy as np

DATASET_RANGES = {
    "GlobalNewsDataset": (1000000, 1105351),
    "RedditDataset": (1105352, 1519554),
    "WeeklyNewsDataset_Aug17": (1519555, 1979142),
    "WeeklyNewsDataset_Aug18": (1979143, 2455685)
}

DATASET_PATHS = {

    "GlobalNewsDataset": os.path.join('../..', 'data', 'SampleDatasets_ForTesting', 'GlobalNewsDataset_Sample_5000.csv'),
    "RedditDataset": os.path.join('../..', 'data', 'SampleDatasets_ForTesting', 'RedditDataset_Sample_5000.csv'),
    "WeeklyNewsDataset_Aug17": os.path.join('../..', 'data', 'SampleDatasets_ForTesting', 'WeeklyNewsDataset_Aug17_5000.csv'),
    "WeeklyNewsDataset_Aug18": os.path.join('../..', 'data', 'SampleDatasets_ForTesting', 'WeeklyNewsDataset_Aug18_5000.csv')
}

def identify_dataset(doc_id):
    for dataset, (start_id, end_id) in DATASET_RANGES.items():
        if start_id <= doc_id <= end_id:
            return dataset
    return None

# Cache for loaded datasets
DATASET_CACHE = {}


@jit(nopython=True)
def search_doc_id(doc_ids, target_id):
    """GPU-accelerated binary search for document ID"""
    return np.searchsorted(doc_ids, target_id)


def load_dataset(dataset_path):
    """Load dataset with caching"""
    if dataset_path in DATASET_CACHE:
        return DATASET_CACHE[dataset_path]

    try:
        df = pd.read_csv(dataset_path)
        # Sort by DocID for better search performance
        df = df.sort_values('DocID')
        DATASET_CACHE[dataset_path] = df
        return df
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return None


def retrieve_content(doc_id):
    dataset_name = identify_dataset(doc_id)
    if not dataset_name:
        print(f"Error: DocID {doc_id} not found in any dataset range.")
        return None

    dataset_path = DATASET_PATHS[dataset_name]
    try:
        dataset = load_dataset(dataset_path)
        if dataset is None:
            return None

        # Convert DocIDs to numpy array for GPU acceleration
        doc_ids = dataset['DocID'].values
        idx = search_doc_id(doc_ids, doc_id)

        if idx >= len(dataset) or dataset.iloc[idx]['DocID'] != doc_id:
            print(f"Error: DocID {doc_id} not found in dataset {dataset_name}.")
            return None

        return dataset.iloc[idx].to_dict()

    except Exception as e:
        print(f"Error retrieving content for DocID {doc_id}: {e}")
        return None


def clear_cache():
    """Clear dataset cache to free memory"""
    global DATASET_CACHE
    DATASET_CACHE.clear()