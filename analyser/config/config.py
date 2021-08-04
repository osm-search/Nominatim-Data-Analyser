from analyser.logger.logger import LOG
from pathlib import Path
import yaml

class Config():
    values: dict = dict()

    @staticmethod
    def load_config() -> None:
        """
            Load the YAML config file into the
            config global variable.
        """
        current_folder = Path(__file__).parent
        path = current_folder / Path('config.yaml')
        if not path.is_file():
            path = current_folder / Path('default.yaml')
            LOG.info('Loading the default.yaml config file.')
        else:
            LOG.info('Loading the config.yaml file.')

        with open(path, 'r') as file:
            try:
                Config.values = yaml.safe_load(file)
            except yaml.YAMLError as exc:
                LOG.error(f'Error while loading the config file: {exc}')