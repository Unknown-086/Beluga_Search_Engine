import pandas as pd
import os


def get_row_by_doc_id(file_path, doc_id):
    """
    Retrieve a row from the dataset using the DocID.

    :param file_path: Path to the dataset CSV file.
    :param doc_id: The DocID to search for.
    :return: The row as a pandas Series if found, otherwise None.
    """
    try:
        df = pd.read_csv(file_path)
        row = df[df['DocID'] == doc_id]
        if not row.empty:
            return row.iloc[0]
        else:
            print(f"DocID '{doc_id}' not found in the dataset.")
            return None
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"Unexpected error while processing the dataset: {e}")
        return None


# Example usage
file_path = os.path.join('../../..', 'data', 'FilteredDatasets', 'ModifiedReddit_database11_English.csv')
doc_id = 1497713
row = get_row_by_doc_id(file_path, doc_id)
print(row['post'])
# if row is not None:
#     print(row)