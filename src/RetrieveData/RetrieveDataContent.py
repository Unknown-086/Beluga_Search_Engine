import os

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

import pandas as pd

def retrieve_content(doc_id):
    dataset_name = identify_dataset(doc_id)
    if not dataset_name:
        print(f"Error: DocID {doc_id} not found in any dataset range.")
        return None

    dataset_path = DATASET_PATHS[dataset_name]
    try:
        dataset = pd.read_csv(dataset_path)
        document = dataset[dataset['DocID'] == doc_id]
        if document.empty:
            print(f"Error: DocID {doc_id} not found in dataset {dataset_name}.")
            return None
        return document.to_dict(orient='records')[0]
    except Exception as e:
        print(f"Error retrieving content for DocID {doc_id}: {e}")
        return None