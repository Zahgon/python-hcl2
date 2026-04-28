"""``jsontohcl2`` CLI entry point — convert JSON files to HCL2."""

import argparse
import difflib
import json
import os
import sys
from io import StringIO
from typing import TextIO

import hcl2
from hcl2 import dump
from hcl2.deserializer import DeserializerOptions
from hcl2.formatter import FormatterOptions
from hcl2.query.diff import diff_dicts, format_diff_json, format_diff_text
from hcl2.utils import SerializationOptions
from hcl2.version import __version__
from cli.helpers import (
    EXIT_DIFF,
    EXIT_IO_ERROR,
    EXIT_PARSE_ERROR,
    EXIT_PARTIAL,
    JSON_SKIPPABLE,  # used in _convert_* calls for skip handling
    _convert_directory,
    _convert_multiple_files,
    _convert_single_file,
    _error,
    _expand_file_args,
    _install_sigpipe_handler,
)


def _json_to_hcl(
    in_file: TextIO,
    out_file: TextIO,
    d_opts: DeserializerOptions,
    f_opts: FormatterOptions,
) -> None:
    pass


def _json_to_hcl_string(
    in_file: TextIO,
    d_opts: DeserializerOptions,
    f_opts: FormatterOptions,
) -> str:
    """Convert JSON input to an HCL string (for --diff / --dry-run)."""
    pass


def _json_to_hcl_fragment(
    in_file: TextIO,
    d_opts: DeserializerOptions,
    f_opts: FormatterOptions,
) -> str:
    """Convert a JSON fragment to HCL attribute assignments.

    Unlike normal conversion, this strips ``__is_block__`` markers so the
    input is always treated as flat attributes — even if it came from
    ``hcl2tojson`` output.
    """
    pass


def _strip_block_markers(data):
    """Recursively remove ``__is_block__`` keys from nested dicts."""
    pass


_EXAMPLES = """\
examples:
  jsontohcl2 file.json                                   # single file to stdout
  jsontohcl2 a.json b.json -o out/                      # multiple files to output dir
  jsontohcl2 --diff original.tf modified.json            # preview text changes
  jsontohcl2 --semantic-diff original.tf modified.json   # semantic-only changes
  jsontohcl2 --semantic-diff original.tf --diff-json m.json  # semantic diff as JSON
  jsontohcl2 --dry-run file.json                         # convert without writing
  jsontohcl2 --fragment -                                # attribute snippet from stdin
  echo '{"x": 1}' | jsontohcl2                          # stdin (no args needed)

fragment string format:
  Strings use python-hcl2's inner-quote convention. To produce HCL "value",
  the JSON string must be: "\\"value\\"". Unquoted strings become identifiers.
  Example: {"name": "\\"test\\"", "count": 3}  =>  name = "test"  count = 3

exit codes:
  0  Success
  1  JSON/encoding parse error
  2  Valid JSON but incompatible HCL structure
  4  I/O error (file not found)
  5  Differences found (--diff / --semantic-diff)
"""


def main():  # pylint: disable=too-many-branches,too-many-statements,too-many-locals
    """The ``jsontohcl2`` console_scripts entry point."""
    pass


if __name__ == "__main__":
    main()
