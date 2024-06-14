import csv
import pandas as pd
# Read the CSV file exported from the Google Form
csv_file_path = 'responses.csv'
responses_df = pd.read_csv(csv_file_path)

# Read the Google Sheet containing the formatted text
sheet_file_path = 'formatted_text_order.csv'

pd_formatted_text = pd.read_csv(sheet_file_path)

# Merge the data based on section number
merged_data = []
for index, row in responses_df.iterrows():
    section_number = row['Select the section you were instructed to complete:'].split()[1]
    # merge all the data from the pd_formatted_text with the responses of the responses_df


# Write the merged data to a new CSV file
merged_file_path = 'merged_responses.csv'
fieldnames = list(responses[0].keys()) + ['Formatted Text']
with open(merged_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(merged_data)

print('Merged responses saved to', merged_file_path)
