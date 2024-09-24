#!/usr/bin/python3
import sys
from pathlib import Path

sys.path.insert(1, str(Path(__file__, '..', 'src').resolve()))

from nominatim_data_analyser.cli import cli

sys.exit(cli())
