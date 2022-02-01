import argparse
import pathlib
import sys
import json


def file_path(path):
    p = pathlib.Path(path)
    if p.is_file():
        return p
    else:
        raise argparse.ArgumentTypeError(
            f"Invalid argument ({path}), not a file path or file does not exist."
        )


def main(argv=None):
    parser = argparse.ArgumentParser(description="JSON usage example.")
    # positional/required argument
    parser.add_argument("parameters_filename", type=file_path)
    args = parser.parse_args(argv)
    with open(args.parameters_filename) as fp:
        configuration_dict = json.load(fp)
    print(configuration_dict)


if __name__ == "__main__":
    # for debugging
    sys.exit(main(["parameters.json"]))
    # for running the program
    # sys.exit(main())
