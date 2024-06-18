import os
import tarfile

root_dir = r'C:\Users\Th3RapidK1ller\Downloads\nyt_corpus\nyt_corpus\data'

for dirpath, dirnames, filenames in os.walk(root_dir):

    for file in filenames:
        if file.endswith('.tgz'):
            print(file)
            tgz_file_path = os.path.join(dirpath, file)
            print(tgz_file_path)
            with tarfile.open(tgz_file_path, 'r:gz') as tar:
                tar.extractall(path=dirpath)