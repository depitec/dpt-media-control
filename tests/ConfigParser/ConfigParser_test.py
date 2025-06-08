from ConfigParser.ConfigParser import ConfigParser

from pathlib import Path

TEST_DIR_PATH = Path(__file__).parent


class TestConfigParser:
    def test_read_config(self):
        config_path = Path(TEST_DIR_PATH, "resources", "testconfig.toml").absolute()
        config_parser = ConfigParser(config_path.as_posix())
        config = config_parser.read_config()

        assert config["Project"]["name"] == "dpt-media-control"
        assert config["InputPins"][0]["hold_time"] == 10
        assert config["InputPins"][1]["name"] == "pin2"
