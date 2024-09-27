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
    Config.values.clear()

    # First load the default settings.
    _get_config_file_contents(Path(__file__, '..', 'default_config.yaml').resolve())

    # Then overwrite with potential custom settings.
    if config_file is not None and config_file.is_file():
        LOG.info(f"Loading config from {config_file}.")
        _get_config_file_contents(config_file)


def _get_config_file_contents(config_file: Path) -> None:
    with config_file.open('r') as file:
        try:
            contents = yaml.safe_load(file)
        except yaml.YAMLError as exc:
            LOG.error(f"Error while loading the config file: {exc}")
            raise

        if not isinstance(contents, dict):
            raise RuntimeError('Error in config file, expected key-value entries.')

        for k, v in contents.items():
            if not isinstance(k, str):
                raise RuntimeError(f"Error in config file, non-string key {k}.")
            Config.values[k] = str(v)
