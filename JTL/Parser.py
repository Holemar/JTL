# -*- coding:utf-8 -*-

# Copyright (c) 2015-2019 Agalmic Ventures LLC (www.agalmicventures.com)
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

import shlex

from JTL import Utility
from JTL import json_util


def parseTransform(transform):
    """
    Parses a single JTL transform into tokens.

    :param transform: str
    :return: [[str]]
    """
    # Create a lexer with some slight tweaks
    lexer = shlex.shlex(transform, posix=False)
    lexer.wordchars += '.+-*=<>!'

    # Split into operations
    operations = []
    operation = []
    for token in lexer:
        # Split tokens on $
        if token == '$':
            operations.append(operation)
            operation = []
        else:
            operation.append(token)

    # Append any final operation
    operations.append(operation)

    return operations


def parseArgument(argument, data):
    """
    Parses an argument to an operation.

    :param argument: str from tokenization
    :param data: dict of original data to extract more fields from
    :return: a valid JSON value
    """
    # Try loading as a constrant first
    # TODO: strings are awkward and require escaping, so figure that out
    value = json_util.load_json(argument)
    if value is not None:
        return value
    # If that fails, it might be a name
    return Utility.extractPath(data, argument)

