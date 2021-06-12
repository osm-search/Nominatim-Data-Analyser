from analyser.logic import Core
import argparse

parser = argparse.ArgumentParser(prog='nominatim-analyser')
parser.add_argument('execute')
args = parser.parse_args()

if args.execute:
    Core().execute_all()