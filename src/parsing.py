import pandas as pd


# def parse_dataset(file_path, output_path, start_row=None, end_row=None, date_range=None):
#     """
#     Parse and extract a portion of the dataset based on row range or publish_time.
#
#     Args:
#         file_path (str): Path to the input dataset file.
#         output_path (str): Path to save the parsed portion of the dataset.
#         start_row (int, optional): Starting row number for extraction.
#         end_row (int, optional): Ending row number for extraction.
#         date_range (tuple, optional): Tuple containing start and end dates (YYYY-MM-DD).
#
#     Returns:
#         None
#     """
#     # Load the dataset
#     dataset = pd.read_csv(file_path, delimiter=',')  # Adjust delimiter if necessary (e.g., ',' for comma)
#
#     # Check and process date range
#     if date_range:
#         start_date, end_date = date_range
#         dataset['publish_time'] = pd.to_datetime(dataset['publish_time'], errors='coerce')
#         dataset = dataset[(dataset['publish_time'] >= start_date) & (dataset['publish_time'] <= end_date)]
#
#     # Check and process row range
#     if start_row is not None and end_row is not None:
#         dataset = dataset.iloc[start_row:end_row]
#
#     # Save the extracted portion to a new file
#     dataset.to_csv(output_path, index=False, sep='\t')
#     print(f"Extracted dataset saved to {output_path}")

def parse_dataset(input_file, output_file, num_rows=50000):
    """
    Extract the first 'num_rows' records from the dataset.

    Args:
        input_file (str): Path to the input dataset file.
        output_file (str): Path to save the extracted dataset.
        num_rows (int): Number of rows to extract (default: 50,000).
    """
    # Load the dataset
    dataset = pd.read_csv(input_file)

    # Extract the first 'num_rows' rows
    extracted_data = dataset.head(num_rows)

    # Save the extracted rows to a new CSV file
    extracted_data.to_csv(output_file, index=False)
    print(f"Extracted {num_rows} rows and saved to {output_file}")

# Example usage:
file_path = "D:\\zDSA Project\\DataSets\\dataverse_files\\news-week-18aug24.csv"  # Path to your input dataset
output_path = "D:\\zDSA Project\\DataSets\\dataverse_files\\extracted_dataset2.csv"  # Path to save the extracted portion

# Extract rows 1000 to 5000
parse_dataset(file_path, output_path, 25000)

# OR Extract data from a specific date range
# parse_dataset(file_path, output_path, date_range=('2018-01-01', '2018-12-31'))
