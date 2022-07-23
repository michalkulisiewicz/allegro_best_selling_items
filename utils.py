from pathlib import Path
import json
import os


def create_output_directory(dir_name):
    Path(dir_name).mkdir(parents=True, exist_ok=True)

def check_if_directory_exists(dir_name):
    return os.path.isdir(dir_name)

def save_output_to_json_file(dir_name, filename, output):
    create_output_directory(dir_name)
    with open(os.path.join(dir_name, filename), 'w') as f:
        json.dump(output, f, indent=4, ensure_ascii=False)
        print('Output saved as a file: {}. In directory: {}'.format(filename, dir_name))

def extract_cat_num_from_filename(filename):
    category_num = filename.split('.')[0]
    return int(category_num)

def read_auctions_from_json(auctions_dir_name):
    file_list = list(Path(auctions_dir_name).glob("*.json"))
    auctions = {}
    for file in file_list:
        cat_num = extract_cat_num_from_filename(file.name)
        with open(file, 'r') as f:
            json_file = json.load(f)
            auctions[cat_num] = json_file
    return auctions
