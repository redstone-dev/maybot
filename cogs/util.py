import json
from os.path import exists

class Config:
    def __init__(self) -> None:
        with open("data/config/default_settings.json", "rt") as config_file:
            self.config = dict(json.load(fp=config_file))
    
    def __getitem__(self, key: str):
        try:
            if key.startswith("guild:"):
                return self.guild_conf(key.split(":", 1)[1])
            else:
                return self.config[key]
        except KeyError:
            return None
    
    def reload_config(self):
        with open("./data/config/default_settings.json", "rt") as config_file:
            self.config = dict(json.load(fp=config_file))
    
    def guild_conf(self, guild_id: str):
        if not exists("./data/guilds/" + guild_id + ".json"):
            return self.config # fall back to defaults
        with open("./data/guilds/" + guild_id + ".json", "rt") as guild_config:
            return dict(json.load(fp=guild_config))
        
global_conf = Config()