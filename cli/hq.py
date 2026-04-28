"""``hq`` CLI entry point — query HCL2 files."""

import argparse
import dataclasses
import json
import multiprocessing
import os
import sys
from typing import Any, List, Optional, Tuple

from hcl2.query._base import NodeView
from hcl2.utils import SerializationOptions
from hcl2.query.body import DocumentView
from hcl2.query.introspect import build_schema, describe_results
from hcl2.query.path import QuerySyntaxError
from hcl2.query.pipeline import classify_stage, execute_pipeline, split_pipeline
from hcl2.query.resolver import resolve_path
from hcl2.query.safe_eval import (
    UnsafeExpressionError,
    _SAFE_CALLABLE_NAMES,
    safe_eval,
)
from hcl2.version import __version__
from .helpers import _expand_file_args  # noqa: F401 — re-exported for tests

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

EXIT_SUCCESS = 0
EXIT_NO_RESULTS = 1
EXIT_PARSE_ERROR = 2
EXIT_QUERY_ERROR = 3
EXIT_IO_ERROR = 4

_EXIT_TO_ERROR_TYPE = {
    EXIT_IO_ERROR: "io_error",
    EXIT_PARSE_ERROR: "parse_error",
    EXIT_QUERY_ERROR: "query_error",
}

_HCL_EXTENSIONS = {".tf", ".hcl", ".tfvars"}

_EVAL_PREFIXES = tuple(f"{name}(" for name in sorted(_SAFE_CALLABLE_NAMES)) + ("doc",)

EXAMPLES_TEXT = """\
examples:
  # Structural queries
  hq 'resource.aws_instance.main.ami' main.tf
  hq 'variable[*]' variables.tf --json
  echo 'x = 1' | hq 'x' --value

  # Multiple files and globs
  hq 'resource[*]' file1.tf file2.tf --json
  hq 'variable[*]' modules/ --ndjson
  hq 'resource[*]' 'modules/**/*.tf' --json

  # Pipes
  hq 'resource.aws_instance[*] | .tags' main.tf
  hq 'variable[*] | select(.default) | .default' vars.tf --json

  # Builtins
  hq 'x | keys' file.tf --json
  hq 'x | length' file.tf --value

  # Select (bracket syntax)
  hq '*[select(.name == "x")]' file.tf --value

  # String functions (jq-compatible)
  hq 'module~[select(.source | contains("docker"))]' dir/
  hq 'resource~[select(.ami | test("^ami-"))]' dir/
  hq 'resource~[select(has("tags"))]' main.tf
  hq 'resource~[select(.tags | not)]' main.tf

  # Object construction (jq-style)
  hq 'resource[*] | {type: .block_type, name: .name_labels}' main.tf --json

  # Optional (exit 0 on empty results)
  hq 'nonexistent?' file.tf --value

  # Raw output (strip quotes, ideal for shell piping)
  hq 'resource.aws_instance.main.ami' main.tf --raw

  # NDJSON (one JSON object per line, ideal for streaming)
  hq 'resource[*]' dir/ --ndjson

  # Source location metadata
  hq 'resource[*]' main.tf --json --with-location

  # Comments in output
  hq 'resource[*]' main.tf --json --with-comments

  # Structural diff
  hq file1.tf --diff file2.tf
  hq file1.tf --diff file2.tf --json

  # Hybrid (structural::eval)
  hq 'resource.aws_instance[*]::name_labels' main.tf
  hq 'variable[*]::block_type' variables.tf --value

  # Pure eval (-e)
  hq -e 'doc.blocks("variable")[0].attribute("default").value' variables.tf --json

  # Introspection
  hq --describe 'variable[*]' variables.tf
  hq --schema

docs: https://github.com/amplify-education/python-hcl2/tree/main/docs
"""

# ---------------------------------------------------------------------------
# Helpers: strings
# ---------------------------------------------------------------------------


def _strip_dollar_wrap(text: str) -> str:
    """Strip ``${...}`` wrapping from a serialized expression string."""
    pass


def _strip_quotes(text: str) -> str:
    """Strip surrounding quotes from a string value."""
    pass


def _rawify(value: Any) -> Any:
    """Recursively strip quotes and ${} wrapping from all string values."""
    pass


# ---------------------------------------------------------------------------
# Helpers: I/O & errors
# ---------------------------------------------------------------------------


def _read_input(path: str) -> str:
    """Read from a file path, or stdin if path is ``-``."""
    pass


def _collect_files(path: str) -> List[str]:
    """Return a list of HCL file paths from a file path, directory, or stdin marker."""
    pass


# _expand_file_args is imported from .helpers and re-exported at module level.


def _error(msg: str, use_json: bool, **extra) -> str:
    """Format an error message."""
    pass


# ---------------------------------------------------------------------------
# Helpers: JSON conversion & result metadata
# ---------------------------------------------------------------------------


def _convert_for_json(
    value: Any,
    options: Optional[SerializationOptions] = None,
) -> Any:
    """Recursively convert NodeViews to dicts for JSON serialization."""
    pass


def _inject_provenance(converted: Any, file_path: str) -> Any:
    """Add ``__file__`` key to dict results for multi-file provenance."""
    pass


def _extract_location(result: Any, file_path: str) -> dict:
    """Extract source location metadata from a result."""
    pass


def _merge_location(converted: Any, location: dict) -> Any:
    """Merge location metadata into a converted JSON value."""
    pass


# ---------------------------------------------------------------------------
# Query dispatch
# ---------------------------------------------------------------------------


def _normalize_eval_expr(expr_part: str) -> str:
    """Normalize the eval expression after '::' for ergonomics."""
    pass


def _dispatch_query(
    query_str: str,
    is_eval: bool,
    doc_view: DocumentView,
    file_path: str = "",
) -> List[Any]:
    """Dispatch a query and return results."""
    pass


# ---------------------------------------------------------------------------
# Output: formatting & lifecycle
# ---------------------------------------------------------------------------


@dataclasses.dataclass
class OutputConfig:
    """Output mode configuration for hq results.

    All fields are primitives or dataclasses, ensuring picklability
    for ``multiprocessing.Pool`` workers.
    """

    output_json: bool = False
    output_value: bool = False
    output_raw: bool = False
    json_indent: Optional[int] = None
    ndjson: bool = False
    with_location: bool = False
    with_comments: bool = False
    no_filename: bool = False
    serialization_options: Optional[SerializationOptions] = None

    def format_result(self, result: Any) -> str:
        """Format a single result for output."""
        pass

    def format_list(self, items: list) -> str:
        """Format a list result (e.g. from hybrid mode returning a list)."""
        pass

    def format_output(self, results: List[Any]) -> str:
        """Format results for final output."""
        pass


def _convert_results(
    results: List[Any],
    file_path: str,
    multi: bool,
    output_config: OutputConfig,
) -> List[Any]:
    """Convert query results for JSON output with location/provenance metadata."""
    pass


class OutputSink:
    """Owns the result output lifecycle: stream or accumulate, then flush."""

    def __init__(self, output_config: OutputConfig, multi: bool):
        self.config = output_config
        self.multi = multi
        self._accumulator: List[Any] = []

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        self.flush()
        return False

    def emit(self, results: List[Any], file_path: str) -> None:
        """Emit raw query results for one file (serial path)."""
        pass

    def emit_converted(self, converted: List[Any]) -> None:
        """Emit pre-converted results (parallel path)."""
        pass

    def flush(self) -> None:
        """Sort and emit accumulated JSON results."""
        pass


# ---------------------------------------------------------------------------
# File-level query execution
# ---------------------------------------------------------------------------


def _run_query_on_file(
    file_path: str,
    query: str,
    is_eval: bool,
    use_json: bool,
    raw_query: str,
) -> Tuple[Optional[List[Any]], int]:
    """Parse a file and run a query.

    Returns ``(results, exit_code)``.  On error, results is ``None`` and
    exit_code is one of the ``EXIT_*`` constants.
    """
    pass


def _process_file(args_tuple):
    """Worker: parse, query, and convert results for one file.

    Returns ``(file_path, exit_code, converted_results, error_msg)``.
    All return values are picklable plain Python objects.
    """
    pass


def _run_diff(
    file1: str, file2: str, use_json: bool, json_indent: Optional[int]
) -> int:
    """Run structural diff between two HCL files.

    Returns an exit code: 0 if files are identical, 1 if they differ.
    Exits directly on I/O or parse errors (matching ``diff(1)`` convention).
    """
    pass


# ---------------------------------------------------------------------------
# CLI: argument parsing & orchestration
# ---------------------------------------------------------------------------


def _build_parser() -> argparse.ArgumentParser:
    """Build the argument parser for ``hq``."""
    pass


def _validate_and_configure(
    parser: argparse.ArgumentParser,
    args: argparse.Namespace,
) -> Tuple[bool, OutputConfig]:
    """Validate argument combinations and build output configuration."""
    pass


def _resolve_query(
    args: argparse.Namespace,
    parser: argparse.ArgumentParser,
    use_json: bool,
    output_config: OutputConfig,
) -> Tuple[str, bool]:
    """Handle early exits and resolve the query string.

    May call ``sys.exit`` for ``--schema``/``--diff`` or ``parser.error``
    for invalid arguments and never return.  Otherwise returns
    ``(query, optional)``.
    """
    pass


def _execute_and_emit(
    args: argparse.Namespace,
    query: str,
    optional: bool,
    use_json: bool,
    output_config: OutputConfig,
) -> int:
    """Execute queries across files and emit results. Returns an exit code."""
    pass


def main():
    """The ``hq`` console_scripts entry point."""
    pass


if __name__ == "__main__":
    main()
