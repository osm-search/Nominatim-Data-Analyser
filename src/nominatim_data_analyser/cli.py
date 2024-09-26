from .core.core import Core
import argparse

def cli() -> int:
    parser = argparse.ArgumentParser(prog='nominatim-analyser')

    parser.add_argument('--execute-all', action='store_true',
                        help='Executes all the QA rules')
    parser.add_argument('--filter', metavar='<QA rules names>', nargs='+',
                        help='Filters some QA rules so they are not executed.')
    parser.add_argument('--execute-one', metavar='<QA rule name>', action='store',
                        type=str, help='Executes the given QA rule')

    args = parser.parse_args()

    # Executes all the QA rules. If a filter is given, these rules are excluded from the execution.
    if args.execute_all:
        if args.filter:
            Core().execute_all(args.filter)
        else:
            Core().execute_all()
    elif args.execute_one:
        # Execute the given QA rule.
        Core().execute_one(args.execute_one)

    return 0
