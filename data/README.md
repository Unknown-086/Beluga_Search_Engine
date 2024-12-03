# Data Directory

This folder stores all the datasets, indexes, and lexicons used or generated in the search engine project. The directory is organized into subfolders to separate raw and processed data for better management and scalability.

## Directory Structure

### 1. `Datasets/`
- **Purpose:** This folder contains the original datasets used in the project.  
- **Datasets Used:**
  1. [Harvard Weekly News Dataset](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/ILAT5B)
  2. [Kaggle Reddit Data Science Posts](https://www.kaggle.com/datasets/maksymshkliarevskyi/reddit-data-science-posts)
  3. [Kaggle Global News Dataset](https://www.kaggle.com/datasets/everydaycodings/global-news-dataset)
- **Instructions:**
  - Download the datasets from the provided links.
  - Place them in this folder before running the code.

### 2. `CombiningDatasets/`
- Contains scripts and output files for merging multiple datasets into a single file.
- Useful for preprocessing datasets to create a unified dataset for indexing.


### 3. `FilteredDatasets/`
- Stores filtered versions of the datasets based on specific criteria, such as removing irrelevant rows or limiting datasets to certain topics.

### 4. `ForwardIndexData/`
- #### `SampleTesting/`
  - Contains sample forward index files used for testing the forward index generation process.
- #### `Testing/`
  - Contains the generated forward index files.
  - Each file maps document IDs to the words they contain along with positional information.

### 5. `InvertedIndexData/`
- #### `SampleTesting/`
  - Contains sample inverted index files used for testing the inverted index generation process.
- #### `Testing/`
  - Contains the generated inverted index files.
  - Each file maps Word IDs to the list of document IDs where they appear.

### 6. `Lexicons/`
- #### `SampleTesting/`
  - Contains sample lexicon files used for testing the lexicon generation process.
- #### `Testing/`
  - Stores lexicon files which map words to unique Word IDs.
  - These files are critical for building forward and inverted indexes.

### 7. `ModifiedAfterDeletedData/`
- Stores updated datasets after rows or columns are deleted during preprocessing.

### 8. `ModifiedDatasets/`
- Contains modified datasets after transformations or additions (e.g., language translations, structure updates).

### 9. `SampleDatasets_ForTesting/`
- Contains sample datasets used for testing Lexicon, Forward Index, and Inverted Index generation.

---

## Notes
- Ensure all downloaded or generated datasets are placed in their respective folders.
- **Data Consistency:** 
  - Any changes in datasets (filtering, translation, etc.) should reflect in corresponding files in this directory.
- **Backup:** Always maintain a backup of the original datasets in the `/Datasets/` folder.

---
