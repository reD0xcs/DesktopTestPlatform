import json
from pathlib import Path

class Settings:
    
    def __init__(self):
        
        config_file = Path("config.json")
        
        with open(config_file, "r") as file:
            self.data = json.load(file)
            
    @property
    def raspberry_pi(self):
        return self.data["raspberry_pi"]
    
    @property
    def application(self):
        return self.data["application"]
    
settings = Settings()