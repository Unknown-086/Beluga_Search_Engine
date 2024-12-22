import json
import os
from src.Barrels.RangeBarrelMaker import getBarrelForRanged
from src.Barrels.HashBarrelMaker import getBarrelForHashed

def getWordIdFromLexicon(word, lexicon_path):
    """
    Retrieve the WordID for a given word from the lexicon.
    :param word: The word to search for.
    :param lexicon_path: Path to the lexicon JSON file.
    :return: WordID for the given word, or None if not found.
    """
    try:
        print(f"Loading lexicon from {lexicon_path}...")
        with open(lexicon_path, 'r', encoding='utf-8') as lexicon_file:
                lexicon = json.load(lexicon_file)
        word_id = lexicon.get(word)
        if word_id is not None:
            print(f"Word '{word}' found with WordID: {word_id}")
            return word_id
        else:
            print(f"Word '{word}' not found in lexicon.")
            return None

    except FileNotFoundError:
        print(f"Error: Lexicon file '{lexicon_path}' not found.")
        return None
    except UnicodeDecodeError:
        # Fallback to read with error handling
        with open(lexicon_path, 'r', encoding='utf-8', errors='ignore') as file:
            return json.load(file)
    except Exception as e:
        print(f"Unexpected error while loading lexicon: {e}")
        return None

def retrieveDocIds(word, lexiconPath, hashedMetadataPath):
    """
    Retrieve the DocumentIDs for a given word using the hashed barrel method.
    :param word: The word to search for.
    :param lexiconPath: Path to the lexicon JSON file.
    :param hashedMetadataPath: Path to the hashed barrel metadata JSON file.
    :return: The barrel path and list of DocumentIDs for the word (if found).
    """
    print(f"Retrieving WordID for '{word}'...")
    wordId = getWordIdFromLexicon(word, lexiconPath)
    if wordId is None:
        # print(f"Word '{word}' not found in lexicon.")
        return None, []

    print(f"Fetching barrel for WordID {wordId}...")
    try:
        return getBarrelForHashed(wordId, hashedMetadataPath)
    except Exception as e:
        print(f"Unexpected error while retrieving barrel: {e}")
        return None, []
