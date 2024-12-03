# Search_Engine_DSA_project - Source Code (`src`)

This folder contains the source code for the search engine project. The project is modularized into various subdirectories to maintain clean and efficient code organization.

## Directory Structure

### 1. `CrawlingWebLinks/`
- Contains functions for crawling and extracting data from web links.
- Will be used in future extensions of the project for dynamic dataset creation.

### 2. `DatasetModificationFunctions/`
- Houses functions for modifying datasets during preprocessing:
  - **AddFunctions:** Functions to add new data columns or rows.
  - **CountFunctions:** Functions to count occurrences of specific items in datasets.
  - **DatasetFunctions:** General utility functions for handling datasets.
  - **DeleteFunctions:** Functions to delete irrelevant or unwanted data.
  - **FilterFunctions:** Functions to filter datasets based on criteria like keywords, topics, or length.
  - **UpdateFunctions:** Functions to update and transform dataset columns.

### 3. `ForwardIndex/`
- Code for building and saving the forward index:
  - **ForwardIndexBuilder.py:** Builds a forward index where each document ID maps to a list of `(Word ID, Position)` tuples.
  - **ForwardMakerTest.py:** Test file for building and saving the forward index.

### 4. `InvertedIndex/`
- Code for building and saving the inverted index:
  - **InvertedIndexBuilder.py:** Converts the forward index into an inverted index where each `Word ID` maps to a list of document IDs.
  - **InvertedMakerTest.py:** Test file for building and saving the inverted index.

### 5. `LanguageFunctions/`
- Reserved for handling multi-language datasets or language-specific text processing.

### 6. `Lexicon/`
- Contains scripts for creating and handling the lexicon (word-to-WordID mappings):
  - **TextPreprocess.py:** Preprocesses text by converting to lowercase, removing punctuation, tokenizing and removing stopwords.
  - **LexiconBuilder.py:** Builds a lexicon from datasets by assigning unique Word IDs to words.
  - **LexiconMakerTest.py:** Test file for generating and validating the lexicon.

### 7. `Testing/`
- Reserved for unit tests and performance evaluations of individual modules.

### 8. `WebTranslateAPI/`
- Integrates the **AWS Translation API** for translating datasets into a common language (e.g., English).
- Includes:
  - **AWSTranslationAPI.py:** Wrapper functions for interacting with AWS Translation API.

---

## Python Version
- This project uses **Python 3.10**.

---

## Libraries Used
- `pandas`
- `nltk`
- `orjson`
- `os`
- `json`
- `shutil`
- `collections`
- `boto3`

---

## Notes
- All output files are saved in the `data/` directory under appropriate subfolders.
- To modify or test any module, edit the corresponding test files in the `Testing/` folder.
