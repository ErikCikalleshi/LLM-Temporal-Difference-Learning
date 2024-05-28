import os
from datasets import Dataset
import xml.etree.ElementTree as ET

root_dir = r'C:\Users\Th3RapidK1ller\Downloads\nyt_corpus\nyt_corpus\data'
data = []
stop = False
for dir_path, dir_names, filenames in os.walk(root_dir):
    if stop:
        break
    # skip directories that are not years
    years = [str(year) for year in range(1987, 1999)]
    if any(dir_path.endswith(year) for year in years):
        continue
    index = 0
    for file in filenames:
        if file.endswith('.xml'):
            file_path = os.path.join(dir_path, file)
            tree = ET.parse(file_path)
            root = tree.getroot()

            # Extract the date, title, and content
            date = root.find(".//doc.copyright").get('year') if root.find(".//doc.copyright") is not None else ""
            title = root.find(".//title").text if root.find(".//title") is not None else ""
            content_blocks = root.findall(".//block")
            content = ""
            for block in content_blocks:
                for p in block.findall('p'):
                    if p.text is not None and len(p.text) > 3:
                        content += p.text + "\n"
            if len(content) <= 1000:
                continue

            if date.isdigit() and 2000 <= int(date) <= 2007:
                data.append({'date': int(date), 'title': title, 'content': content})
            elif date.isdigit() and int(date) > 2007:
                stop = True
                break
            if index == 10000:
                print(date)

            index += 1

# dataset = Dataset.from_dict({'date': [item['date'] for item in data], 'title': [item['title'] for item in data],
#                              'content': [item['content'] for item in data]})
dates = []
titles = []
contents = []
for item in data:
    dates.append(item['date'])
    titles.append(item['title'])
    contents.append(item['content'])

dataset = Dataset.from_dict({'date': dates, 'title': titles, 'content': contents})

# Save the dataset to hugging face

# Save the dataset to hugging face
load_token = open("C:/Users/Th3RapidK1ller/Documents/BA/LLM-Temporal-Difference-Learning/token.txt", "r")
load_token = load_token.read()

train_dataset = dataset.train_test_split(test_size=0.1, seed=42)

train_dataset.push_to_hub("ErikCikalleshi/new_york_times_news_2000_2007", private=True,
                          token=load_token)

# split the dataset

# train_dataset['train'].push_to_hub("ErikCikalleshi/new_york_times_news_10k_1987_1997", private=True, split="train_ift",
#                                    token=load_token)
# train_dataset['test'].push_to_hub("ErikCikalleshi/new_york_times_news_10k_1987_1997", private=True, split="test_ift",
#                                   token=load_token)
