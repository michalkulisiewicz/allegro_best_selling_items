from pathlib import Path
import json
import os


def create_output_directory(dir_name):
    Path(dir_name).mkdir(parents=True, exist_ok=True)


def save_output_to_json_file(dir_name, filename, output):
    create_output_directory(dir_name)
    with open(os.path.join(dir_name, filename), 'w') as f:
        json.dump(output, f, indent=4, ensure_ascii=False)
        print('Output saved as a file: {}. In directory: {}'.format(filename, dir_name))
