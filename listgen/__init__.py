from .jokes import joke
from .listgen import cli
import argparse


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Generates specific list ARC users")
    parser.add_argument(
        "group", help="retreives users from a group.  available groups: www, share, compute")
    parser.add_argument("-A", "--addgroup",
                        action="store_true", help="and add to google group")
    args = parser.parse_args(argv)
    cli(args.group)
