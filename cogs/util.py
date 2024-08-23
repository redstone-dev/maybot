import json

class Config:
    def __init__(self, file_path: str) -> None:
        with open(file_path, "rt") as config_file:
            self.config = json.load(fp=config_file)
    
    def __getitem__(self, key: str):
        try:
            return self.config[key]
        except KeyError:
            return None