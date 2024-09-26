from typing import Any
from ..logger.logger import LOG
from pathlib import Path
import yaml

class Config():
    values: dict[str, Any] = dict()
    default_config_folder_path = Path(__file__).parent

    @staticmethod
    def load_config(config_folder_path: Path = default_config_folder_path) -> None:
        """
            Load the YAML config file into the
            config global variable.
        """
        path = config_folder_path / 'config.yaml'
        if not path.is_file():
            path = config_folder_path / 'default.yaml'
            LOG.info('Loading the default.yaml config file.')
        else:
            LOG.info('Loading the config.yaml file.')

        with open(path, 'r') as file:
            try:
                Config.values = yaml.safe_load(file)
            except yaml.YAMLError as exc:
                LOG.error(f'Error while loading the config file: {exc}')
                raise
