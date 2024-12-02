import pandas
import os

def changeColumnName(inputFile, outputPath, oldColumnName, newColumnName):
    df.rename(columns={'old_column_name': 'new_column_name'}, inplace=True)




if __name__ == '__main__':

    file_path = os.path.join('..', 'data', 'ModifiedDatasets', 'ModifiedGlobalNewsDatasetWithLanguage.csv')
    oldColumnName = ''
    newColumnName = ''