#!/usr/bin/python3
import sys
import sysconfig
from pathlib import Path

SRC_DIR = Path(__file__, '..').resolve()

BUILD_DIR = f"build/lib.{sysconfig.get_platform()}-{sys.version_info[0]}.{sys.version_info[1]}"

if not (SRC_DIR / BUILD_DIR).exists():
    BUILD_DIR = f"build/lib.{sysconfig.get_platform()}-{sys.implementation.cache_tag}"

if (SRC_DIR / BUILD_DIR).exists():
    sys.path.insert(0, str(SRC_DIR / BUILD_DIR))


from nominatim_data_analyser.cli import cli

sys.exit(cli())
