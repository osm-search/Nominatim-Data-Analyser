import argparse

from .core.core import Core

def cli() -> int:
    parser = argparse.ArgumentParser(prog='nominatim-analyser')

    parser.add_argument('--execute-all', action='store_true',
                        help='Executes all the QA rules')
    parser.add_argument('--filter', metavar='<QA rules names>', nargs='+',
                        help='Filters some QA rules so they are not executed.')
    parser.add_argument('--execute-one', metavar='<QA rule name>', action='store',
                        type=str, help='Executes the given QA rule')
    parser.add_argument('--config', metavar='<YAML file>', default='config.yaml',
                        help='Location of config file (default: config.yaml)')

    args = parser.parse_args()

    core = Core(config_file=args.config)

    # Executes all the QA rules. If a filter is given, these rules are excluded from the execution.
    if args.execute_all:
        core.execute_all(args.filter)
    elif args.execute_one:
        # Execute the given QA rule.
        core.execute_one(args.execute_one)
    else:
        return 1

    return 0
