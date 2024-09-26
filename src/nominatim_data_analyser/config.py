from pathlib import Path

import yaml

from .logger.logger import LOG


class Config:
    values: dict[str, str] = {}


def load_config(config_file: Path | None) -> None:
    """
       Load the YAML config file into the
       config global variable.
    """
    if config_file is None or not config_file.is_file():
        config_file = Path(__file__, '..', 'default_config.yaml').resolve()
        LOG.info('Loading the default.yaml config file.')
    else:
        LOG.info(f"Loading config from {config_file}.")

    with config_file.open('r') as file:
        try:
            contents = yaml.safe_load(file)
        except yaml.YAMLError as exc:
            LOG.error(f"Error while loading the config file: {exc}")
            raise

        if not isinstance(contents, dict):
            raise RuntimeError('Error in config file, expected key-value entries.')

        Config.values.clear()
        for k, v in contents.items():
            if not isinstance(k, str):
                raise RuntimeError(f"Error in config file, non-string key {k}.")
            Config.values[k] = str(v)
