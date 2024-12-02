import boto3
import pandas as pd
import os


def get_supported_languages():
    # Initialize the boto3 client for AWS Translate
    client = boto3.client('translate', region_name='us-east-1')  # Specify the region you are working in

    try:
        # Get the list of supported languages
        response = client.list_languages(DisplayLanguageCode='en')

        # Extract and return the list of languages
        languages = response['Languages']
        return languages

    except Exception as e:
        return f"Error: {str(e)}"



if __name__ == "__main__":
    supported_languages = get_supported_languages()

    if isinstance(supported_languages, str):
        print(supported_languages)
    else:
        # Create a DataFrame from the list of supported languages
        df = pd.DataFrame(supported_languages)

        # Save the DataFrame to a CSV file
        output_file = os.path.join('..', '..', 'data', 'Datasets', 'AWS_supported_languages.csv')
        df.to_csv(output_file, index=False)

        print(f"Supported languages saved to {output_file}")