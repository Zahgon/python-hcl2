"""``hcl2tojson`` CLI entry point — convert HCL2 files to JSON."""

import argparse
import json
import os
import sys
from typing import IO, List, Optional, TextIO

from hcl2 import load
from hcl2.utils import SerializationOptions
from hcl2.version import __version__
from cli.helpers import (
    EXIT_IO_ERROR,
    EXIT_PARSE_ERROR,
    EXIT_PARTIAL,
    EXIT_SUCCESS,
    HCL_SKIPPABLE,
    _collect_files,
    _convert_directory,
    _convert_multiple_files,
    _convert_single_file,
    _error,
    _expand_file_args,
    _install_sigpipe_handler,
)

_HCL_EXTENSIONS = {".tf", ".hcl"}


def _filter_data(
    data: dict,
    only: Optional[str] = None,
    exclude: Optional[str] = None,
    fields: Optional[str] = None,
) -> dict:
    """Apply block-type filtering and field projection to parsed HCL data."""
    pass


def _project_fields(data, field_set):
    """Keep only specified fields (plus metadata keys) in nested dicts.

    Structural keys (whose values are dicts or lists) are always preserved
    so the block hierarchy stays intact.  Only leaf attribute keys are
    filtered.
    """
    pass


def _hcl_to_json(  # pylint: disable=too-many-arguments,too-many-positional-arguments
    in_file: TextIO,
    out_file: IO,
    options: SerializationOptions,
    json_indent: Optional[int] = None,
    compact_separators: bool = False,
    only: Optional[str] = None,
    exclude: Optional[str] = None,
    fields: Optional[str] = None,
) -> None:
    pass


def _load_to_dict(
    in_file: TextIO,
    options: SerializationOptions,
    only: Optional[str] = None,
    exclude: Optional[str] = None,
    fields: Optional[str] = None,
) -> dict:
    """Load HCL2 and return the parsed dict (no JSON serialization)."""
    pass


def _stream_ndjson(  # pylint: disable=too-many-arguments,too-many-positional-arguments
    file_paths: List[str],
    options: SerializationOptions,
    json_indent: Optional[int],
    skip: bool,
    quiet: bool,
    add_provenance: bool,
    only: Optional[str] = None,
    exclude: Optional[str] = None,
    fields: Optional[str] = None,
) -> int:
    """Stream one JSON object per file to stdout (NDJSON).

    Returns the worst exit code encountered.
    """
    pass


_EXAMPLES = """\
examples:
  hcl2tojson file.tf                        # single file to stdout
  hcl2tojson --ndjson dir/                  # directory to stdout (NDJSON)
  hcl2tojson a.tf b.tf -o out/             # multiple files to output dir
  hcl2tojson --ndjson a.tf b.tf            # multiple files as NDJSON
  hcl2tojson --ndjson 'modules/**/*.tf'    # glob + NDJSON streaming
  hcl2tojson --only resource,module file.tf # block type filtering
  hcl2tojson --exclude variable file.tf     # exclude block types
  hcl2tojson --fields cpu,memory file.tf    # field projection
  hcl2tojson --compact file.tf             # single-line JSON
  echo 'x = 1' | hcl2tojson               # stdin (no args needed)

exit codes:
  0  Success
  1  Partial success (some files skipped via -s)
  2  Parse error (all input unparsable)
  4  I/O error (file not found)
"""


def main():  # pylint: disable=too-many-branches,too-many-statements,too-many-locals
    """The ``hcl2tojson`` console_scripts entry point."""
    pass


def _resolve_file_paths(paths: List[str], parser) -> List[str]:
    """Expand directories into individual file paths for NDJSON streaming."""
    pass


if __name__ == "__main__":
    main()
