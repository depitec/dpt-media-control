from pathlib import Path

from ConfigParser.ConfigParser import ConfigParser

TEST_DIR_PATH = Path(__file__).parent


class TestConfigParser:
    def test_loading_config(self):
        parser = ConfigParser(TEST_DIR_PATH / "resources" / "testconfig.toml", {"name": "dpt-media-control"})
        parser.load_config()

        assert parser.config is not None

    def test_correctly_loaded_config(self):
        parser = ConfigParser(TEST_DIR_PATH / "resources" / "testconfig.toml", {"name": "dpt-media-control"})
        parser.load_config()

        config = parser.config
        assert config["Project"]["name"] == "dpt-media-control"

        assert config["InputPins"] == [
            {"name": "pin1", "gpio": 1, "hold_time": 10},
            {"name": "pin2", "gpio": 2, "hold_time": 20},
        ]

    def test_setting_config(self):
        pass
