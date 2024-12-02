import pandas as pd
import os

# Construct the relative path to the dataset
file_path = os.path.join('../../..', 'data', 'ModifiedDatasets', 'ModifiedNews-week-18aug6_WithoutDocID.csv')
df = pd.read_csv(file_path)

# Specify the starting value for numbering
start_value = 1_979_143  # Change this to your desired start value

# Create a new column for numbering
df.insert(0, 'DocID', range(start_value, start_value + len(df)))

# Print the start and end numbering
end_value = start_value + len(df) - 1  # Calculate the end numbering
print(f"Start Numbering: {start_value}")
print(f"End Numbering: {end_value}")

# Save the updated dataset to a new file using a relative path
output_file = os.path.join('../../..', 'data', 'ModifiedDatasets', 'ModifiedNews-week-18aug7.csv')
df.to_csv(output_file, index=False)

print(f"Updated dataset with numbering column saved to {output_file}")