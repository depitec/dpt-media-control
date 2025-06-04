import tomllib


class ConfigParser:
    def __init__(self, config_file_path: str):
        self.config_file_path = config_file_path
        self.config = {}

    def read_config(self):
        with open(self.config_file_path, "rb") as f:
            self.config = tomllib.load(f)
