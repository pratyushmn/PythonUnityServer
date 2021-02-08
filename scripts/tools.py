import yaml, os

from yaml.events import DocumentEndEvent

class FileNotFound(Exception): pass 

def get_content(file_path, config=None):
    if os.path.exists(file_path): 
        with open(file_path) as file: 
            data = yaml.load(file, Loader=yaml.FullLoader)
        return data[config] if config else data
    else: 
        raise FileNotFound(f'File {file_path} not found')

def save_content(file_path, data):
    if os.path.exists(file_path): 
        with open(file_path, 'w') as file: 
            doucment = yaml.dump(data, file)
            return doucment
    else: 
        raise FileNotFound(f'File {file_path} not found')