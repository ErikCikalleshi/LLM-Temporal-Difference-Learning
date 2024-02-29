import os
from datasets import Dataset
import xml.etree.ElementTree as ET

root_dir = r'C:\Users\Th3RapidK1ller\Downloads\nyt_corpus\nyt_corpus\data'
data = []

for dir_path, dir_names, filenames in os.walk(root_dir):
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
            content = " ".join([block.find('p').text for block in content_blocks if block.find('p') is not None])
            # print(date, title, content[:10])
            if date >= "1998" or date <= "2007":
                data.append({'date': date, 'title': title, 'content': content})
            if index == 1000:
                print(date)
                print("Breaking")
                break
            index += 1

dataset = Dataset.from_dict({'date': [item['date'] for item in data], 'title': [item['title'] for item in data],
                             'content': [item['content'] for item in data]})

print(dataset.num_rows)

# Save the dataset to hugging face
load_token = open("C:/Users/Th3RapidK1ller/Documents/BA/LLM-Temporal-Difference-Learning/token.txt", "r")
load_token = load_token.read()

dataset.push_to_hub("ErikCikalleshi/new_york_times_news", private=True, config_name="1998_2007_1k",
                    token=load_token)

# split the dataset
train_dataset = dataset.train_test_split(test_size=0.1, seed=42)
train_dataset['train'].push_to_hub("ErikCikalleshi/new_york_times_news", private=True, config_name="1998_2007_1k_train",
                                   token=load_token)
train_dataset['test'].push_to_hub("ErikCikalleshi/new_york_times_news", private=True, config_name="1998_2007_1k_test",
                                    token=load_token)
