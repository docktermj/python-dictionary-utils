#! /usr/bin/env python

# -----------------------------------------------------------------------------
# migrate.py Migration tool for Senzing
# -----------------------------------------------------------------------------

import argparse
import json
import os.path
import time

# -----------------------------------------------------------------------------
# Define argument parser
# -----------------------------------------------------------------------------


def get_parser():
    '''Parse commandline arguments.'''
    parser = argparse.ArgumentParser(prog="json-utils", description="Work with JSON files")
    subparsers = parser.add_subparsers(dest="subcommand", help='sub-command help')

    subparser_1 = subparsers.add_parser('sort', help='Sort and pretty print a file of JSON')
    subparser_1.add_argument("--input-file", dest="input_filename", required=True, help="Input file pathname")
    subparser_1.add_argument("--output-file", dest="output_filename", help="Output file pathname")

    subparser_2 = subparsers.add_parser('prune', help='Delete children below a certain depth')
    subparser_2.add_argument("--input-file", dest="input_filename", required=True, help="Input file pathname")
    subparser_2.add_argument("--output-file", dest="output_filename", help="Output file pathname")
    subparser_2.add_argument("--depth", type=int, dest="depth", help="Maximum depth to output")

    return parser

# -----------------------------------------------------------------------------
# Utility functions
# -----------------------------------------------------------------------------


def prune_dictionaries(level, depth, input_dictionary):
    result_dictionary = {}
    if level < depth:
        for key, value in input_dictionary.items():
            if type(value) is dict:
                result_dictionary[key] = prune_dictionaries(level + 1, depth, value)
            else:
                result_dictionary[key] = {}
    return result_dictionary

# -----------------------------------------------------------------------------
# compare-keys
# -----------------------------------------------------------------------------


def do_prune(args):

    # Parse command line arguments

    input_filename = args.input_filename
    depth = args.depth
    output_filename = args.output_filename or "json-utils-prune-{0}.json".format(int(time.time()))

    # Verify existence of file.

    if not os.path.isfile(input_filename):
        print("Error: --input-file {0} does not exist".format(input_filename))
        os._exit(1)

    # Load the JSON file.

    with open(input_filename) as input_file:
        input_dictionary = json.load(input_file)

    # Do the transformation.

    current_level = 0
    result_dictionary = prune_dictionaries(current_level, depth, input_dictionary)

    # Write the output JSON file.

    with open(output_filename, "w") as output_file:
        json.dump(result_dictionary, output_file, sort_keys=True, indent=4)

    # Epilog.

    print("Output file: {0}".format(output_filename))

# -----------------------------------------------------------------------------
# sort
# -----------------------------------------------------------------------------


def do_sort(args):

    # Parse command line arguments

    input_filename = args.input_filename
    output_filename = args.output_filename or "json-utils-sort-{0}.json".format(int(time.time()))

    # Verify existence of file.

    if not os.path.isfile(input_filename):
        print("Error: --input-file {0} does not exist".format(input_filename))
        os._exit(1)

    # Load the JSON file.

    with open(input_filename) as input_file:
        input_dictionary = json.load(input_file)

    # Write the output JSON file.

    with open(output_filename, "w") as output_file:
        json.dump(input_dictionary, output_file, sort_keys=True, indent=4)

    # Epilog.

    print("Output file: {0}".format(output_filename))

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------


if __name__ == "__main__":

    # Parse the command line arguments.

    parser = get_parser()
    args = parser.parse_args()

    # Transform subcommand from CLI to function name string.

    subcommand = args.subcommand
    subcommand_function_name = "do_{0}".format(subcommand.replace('-', '_'))

    # Tricky code for calling function based on string.

    globals()[subcommand_function_name](args)
