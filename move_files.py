import os

years = [str(year) for year in range(1988, 2007)]

base_dir = r'C:\Users\Th3RapidK1ller\Downloads\nyt_corpus\nyt_corpus\data'

for year in years:
    root_dir = os.path.join(base_dir, year)
    target_dir = os.path.join(base_dir, year)

    for dir_path, dir_names, filenames in os.walk(root_dir):
        for file in filenames:
            if file.endswith('.xml'):
                source_file_path = os.path.join(dir_path, file)
                target_file_path = os.path.join(target_dir, file)
                os.rename(source_file_path, target_file_path)