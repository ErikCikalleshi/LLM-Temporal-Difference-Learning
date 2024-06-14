import pandas as pd

# Read CSV files into pandas DataFrames
formatted_text_df = pd.read_csv('formatted_text_order.csv')
responses_df = pd.read_csv('responses.csv')

# the responses_df DataFrame is for each section just one row with the multiple anwsers -> split every tuple of historical informativeness and truthfulness into a new row with the same sectionNumber
# "2024/06/12 12:30:06 PM OESZ","","","Section 1","1","2","2","1" to
# "1", "2", "Section 1"
# "2", "1", "Section 1"
# ...

# Initialize an empty list to store the split rows
split_rows = []

# Iterate over each row in the responses DataFrame
for _, row in responses_df.iterrows():
    section_number = row['Select the section you were instructed to complete:'].split()[1]
    # Iterate over each pair of Historical Informativeness and Truthfulness
    # skip the first 3 rows because they are not relevant
    row = row[3:]
    for i in range(1, len(row), 2):
        info = row[i]
        truth = row[i + 1]
        split_rows.append({'sectionNumber': int(section_number),
                           'Historical Informativeness': info,
                           'Historical Truthfulness': truth})

split_rows_df = pd.DataFrame(split_rows)

print(split_rows_df)
# remove for each section nan values of Historical Informativeness and Truthfulness
split_rows_df = split_rows_df.dropna()
for section_number in split_rows_df['sectionNumber'].unique():
    # get historical informativeness and truthfulness for each section
    section_data = split_rows_df[split_rows_df['sectionNumber'] == int(section_number)]
    # add to the formatted_text_df DataFrame the section data without the sectionNumber but Historical Informativeness and Truthfulness do not exist in the formatted_text_df DataFrame
    formatted_text_df.loc[formatted_text_df['sectionNumber'] == int(section_number), 'Historical Informativeness'] = \
        section_data['Historical Informativeness'].values
    formatted_text_df.loc[formatted_text_df['sectionNumber'] == int(section_number), 'Historical Truthfulness'] = \
        section_data['Historical Truthfulness'].values

print(formatted_text_df)
# Save the merged DataFrame to a new CSV file
merged_file_path = 'merged_responses.csv'
formatted_text_df.to_csv(merged_file_path, index=False)
print('Merged responses saved to', merged_file_path)
