import pandas as pd

# Read CSV files into pandas DataFrames
formatted_text_df = pd.read_csv('Formatted Text Order - Tabellenblatt1.csv')
responses_df = pd.read_csv('Historical Model Evaluation Survey (Antworten) - Formularantworten 1.csv')

# Initialize an empty list to store the split rows
split_rows = []

# Iterate over each row in the responses DataFrame
for _, row in responses_df.iterrows():
    section_number = row['Select the section you were instructed to complete:'].split()[1]
    # Iterate over each pair of Historical Informativeness and Truthfulness
    # skip the first 3 rows because they are not relevant
    print(int(section_number))
    row = row[3:]
    for i in range(1, len(row)):
        info = row[i]
        # truth = row[i + 1]
        # print({'sectionNumber': int(section_number), 'Historical Informativeness': info})
        split_rows.append({'sectionNumber': int(section_number),
                           'Historical Informativeness': info})
        # 'Historical Truthfulness': truth})

split_rows_df = pd.DataFrame(split_rows)

print(split_rows_df)

# remove for each section nan values of Historical Informativeness and Truthfulness
split_rows_df = split_rows_df.dropna()

# Ensure the column 'Historical Informativeness' exists in formatted_text_df
if 'Historical Informativeness' not in formatted_text_df.columns:
    formatted_text_df['Historical Informativeness'] = None

for section_number in split_rows_df['sectionNumber'].unique():
    # get historical informativeness for each section
    section_data = split_rows_df[split_rows_df['sectionNumber'] == int(section_number)][
        'Historical Informativeness'].values

    # Ensure the lengths match by repeating or trimming the data as necessary
    formatted_text_len = formatted_text_df[formatted_text_df['sectionNumber'] == int(section_number)].shape[0]
    if len(section_data) > formatted_text_len:
        section_data = section_data[:formatted_text_len]
    elif len(section_data) < formatted_text_len:
        section_data = list(section_data) + [None] * (formatted_text_len - len(section_data))

    formatted_text_df.loc[
        formatted_text_df['sectionNumber'] == int(section_number), 'Historical Informativeness'] = section_data

print(formatted_text_df)
# Save the merged DataFrame to a new CSV file
merged_file_path = 'merged_responses.csv'
formatted_text_df.to_csv(merged_file_path, index=False)
print('Merged responses saved to', merged_file_path)
