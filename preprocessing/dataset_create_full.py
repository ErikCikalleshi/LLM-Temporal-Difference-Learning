# create a hugging face dataset
import os
from datasets import Dataset
import xml.etree.ElementTree as ET

root_dir = r'C:\Users\Th3RapidK1ller\Downloads\nyt_corpus\nyt_corpus\data'
data = []

for dir_path, dir_names, filenames in os.walk(root_dir):
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
            print(date, title, content[:10])
            data.append({'date': date, 'title': title, 'content': content})
            break

dataset = Dataset.from_dict({'date': [item['date'] for item in data], 'title': [item['title'] for item in data],
                             'content': [item['content'] for item in data]})

print(dataset)

# Save the dataset to hugging face

dataset.push_to_hub("ErikCikalleshi/new_york_times_news", private=True, token="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")
