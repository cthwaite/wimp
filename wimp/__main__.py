"""Summarise Python imports in a given context."""

import argparse
import logging

from .collector import ImportCollector
from .handler import get_handler
from .utility import get_stdlib


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Print non-standard-library imports made in a package, module or Jupyter"
            " notebook"
        )
    )
    parser.add_argument("path")
    parser.add_argument(
        "-v", "--verbose", help="Enable verbose output", action="store_true"
    )
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    try:
        handler = get_handler(args.path)
    except ValueError:
        print(f"Unrecognised path: {args.path}")
        return

    collector = ImportCollector()
    handler.collect_into(collector)
    stdlib = get_stdlib()
    module_list = sorted(set(collector.imports) - set(stdlib))
    for item in module_list:
        print(item)


if __name__ == "__main__":
    main()
