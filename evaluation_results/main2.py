import numpy
import pandas as pd

# Read CSV files into pandas DataFrames
formatted_text_df = pd.read_csv('Part 1 - Tabellenblatt1.csv')
responses_df = pd.read_csv('Historical Model Evaluation Survey - Part 1 (Antworten) - Formularantworten 1.csv')

# Initialize an empty list to store the split rows
split_rows = []

# Iterate over each row in the responses DataFrame
for _, row in responses_df.iterrows():
    section_number = row['Select the section you were instructed to complete:'].split()[1]
    # Iterate over each pair of Historical Informativeness and Truthfulness
    # skip the first 3 rows because they are not relevant
    print(int(section_number))
    row = row[2:]
    count_responses = 0
    for i in range(0, len(row), 2):
        info = row[i]
        fluency = row[i + 1]
        print({'sectionNumber': int(section_number), 'Historical Informativeness': info, 'Historical Fluency': fluency})
        split_rows.append({'sectionNumber': int(section_number),
                           'Historical Informativeness': info,
                           'Historical Fluency': fluency})
        if not pd.isna(info) or not pd.isna(fluency):
            count_responses += 1
    if count_responses < 12:
        print('Error: Expected 15 responses for section', section_number, 'but found', count_responses)

split_rows_df = pd.DataFrame(split_rows)

print(split_rows_df)

# remove for each section nan values of Historical Informativeness and Truthfulness
split_rows_df = split_rows_df.dropna()

# Ensure the column 'Historical Informativeness' exists in formatted_text_df
if 'Historical Informativeness' not in formatted_text_df.columns and 'Historical Fluency' not in formatted_text_df.columns:
    formatted_text_df['Historical Informativeness'] = None
    formatted_text_df['Historical Fluency'] = None

for section_number in split_rows_df['sectionNumber'].unique():
    # get historical informativeness for each section
    section_data_hist_info = split_rows_df[split_rows_df['sectionNumber'] == int(section_number)][
        'Historical Informativeness'].values
    section_data_hist_fluency = split_rows_df[split_rows_df['sectionNumber'] == int(section_number)][
        'Historical Fluency'].values

    formatted_text_df.loc[
        formatted_text_df['sectionNumber'] == int(
            section_number), 'Historical Informativeness'] = section_data_hist_info.astype(int)
    formatted_text_df.loc[
        formatted_text_df['sectionNumber'] == int(
            section_number), 'Historical Fluency'] = section_data_hist_fluency.astype(int)

print(formatted_text_df)
# Save the merged DataFrame to a new CSV file
merged_file_path = 'merged_responses.csv'
formatted_text_df.to_csv(merged_file_path, index=False)
print('Merged responses saved to', merged_file_path)
