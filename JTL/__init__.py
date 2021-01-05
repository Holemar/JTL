#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# https://github.com/AgalmicVentures/JTL


# Copyright (c) 2015-2021 Agalmic Ventures LLC (www.agalmicventures.com)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import argparse
import json
import sys


def main():
    """
    Runs the main JTL program.

    :return: int
    """

    # Parse arguments
    parser = argparse.ArgumentParser(description='JSON Transformation Language')
    parser.add_argument('-i', '--indent', default=4, type=int, help='Indentation amount.')
    parser.add_argument('-t', '--transform-file', help='The name of the JSON file containing the transformation to run.')
    parser.add_argument('-s', '--source-file', help='The name of the JSON file containing the source data to run.')
    parser.add_argument('-r', '--result-file', help='The name of the JSON file containing the result data of run.')
    parser.add_argument('transform', nargs='?', help='The transformation to run.')
    arguments = parser.parse_args(sys.argv[1:])

    sys.path.append('.')
    import Interpreter, json_util

    # Load the transformation
    if arguments.transform is None and arguments.transform_file is not None:
        # From a file
        transform_data = json_util.load_json_file(arguments.transform_file)
    elif arguments.transform is not None and arguments.transform_file is None:
        # From the command line
        transform_data = json_util.load_json(arguments.transform)
    else:
        print('ERROR: Specify either a transform file or a transform')
        return 1

    # Read the JSON in from stdin
    data = None
    if arguments.source_file:
        data = json_util.load_json_file(arguments.source_file)
    if not data:
        data = json_util.load_json(sys.stdin.read())

    # Transform the JSON
    # TODO: cleaner way to do this
    result = Interpreter.transformJson(data, transform_data)

    # Output the result
    if arguments.result_file:
        file_result = json_util.load_json_file(arguments.result_file)
        assert result == file_result
    else:
        print(json.dumps(result, indent=arguments.indent, sort_keys=True))

    return 0


if __name__ == '__main__':
    sys.exit(main())
