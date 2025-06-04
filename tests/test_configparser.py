from ConfigParser.ConfigParser import ConfigParser

from pathlib import Path

TEST_DIR_PATH = Path(__file__).parent


def test_read_config():
    config_path = Path(TEST_DIR_PATH, "resources", "testconfig.toml").absolute()
    config_parser = ConfigParser(config_path.as_posix())

    config_parser.read_config()
    config = config_parser.config

    assert config["Project"]["name"] == "dpt-media-control"
    assert config["Pins"][0]["name"] == "pin1"
