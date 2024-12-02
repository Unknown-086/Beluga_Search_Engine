import os
import pandas as pd


def changeColumnName(inputFile, outputPath, oldColumnName, newColumnName):
    print(f"Reading the CSV file from {inputFile}...")
    df = pd.read_csv(inputFile)

    if oldColumnName not in df.columns:
        print(f"Error: Column '{oldColumnName}' not found in the dataset.")
        return

    print(f"Renaming column '{oldColumnName}' to '{newColumnName}'...")
    df.rename(columns={oldColumnName: newColumnName}, inplace=True)

    print(f"Saving the updated DataFrame to {outputPath}...")
    df.to_csv(outputPath, index=False)
    print("Column name changed and file saved successfully.")


if __name__ == '__main__':

    filePath = os.path.join('../../..', 'data', 'FilteredDatasets', 'ModifiedReddit_database11_English.csv')
    outputPath = os.path.join('../../..', 'data', 'FilteredDatasets', 'ModifiedReddit_database11_English_date.csv')
    oldColumnName = 'created_date'
    newColumnName = 'date'

    changeColumnName(filePath, outputPath, oldColumnName, newColumnName)