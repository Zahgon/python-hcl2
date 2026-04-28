"""Shared file-conversion helpers for the HCL2 CLI commands."""

import glob as glob_mod
import json
import os
import signal
import sys
from io import StringIO
from typing import Callable, IO, List, Optional, Set, Tuple, Type

from lark import UnexpectedCharacters, UnexpectedToken

# Exit codes shared across CLIs
EXIT_SUCCESS = 0
EXIT_PARTIAL = 1  # hcl2tojson: some files skipped; jsontohcl2: JSON/encoding error
EXIT_PARSE_ERROR = 2  # hcl2tojson: all unparsable; jsontohcl2: bad HCL structure
EXIT_IO_ERROR = 4
EXIT_DIFF = 5  # jsontohcl2 --diff: differences found

# Exceptions that can be skipped when -s is passed
HCL_SKIPPABLE = (UnexpectedToken, UnexpectedCharacters, UnicodeDecodeError)
JSON_SKIPPABLE = (json.JSONDecodeError, UnicodeDecodeError)


def _install_sigpipe_handler() -> None:
    """Reset SIGPIPE to default so piping to ``head`` etc. exits cleanly."""
    pass


def _error(msg: str, use_json: bool = False, **extra) -> str:
    """Format an error message for stderr.

    When *use_json* is true the result is a single-line JSON object with
    ``error`` and ``message`` keys (plus any *extra* fields).  Otherwise
    a plain ``Error: …`` string is returned.
    """
    pass


def _expand_file_args(file_args: List[str]) -> List[str]:
    """Expand glob patterns in file arguments.

    For each arg containing glob metacharacters (``*``, ``?``, ``[``),
    expand via :func:`glob.glob` with ``recursive=True``.  Literal paths
    and ``-`` (stdin) pass through unchanged.  If a glob matches nothing,
    the literal pattern is kept so the caller produces an IO error.
    """
    pass


def _collect_files(path: str, extensions: Set[str]) -> List[str]:
    """Return a sorted list of files under *path* matching *extensions*.

    If *path* is ``-`` (stdin marker) or a plain file, it is returned as-is
    in a single-element list.  Directories are walked recursively.
    """
    pass


def _convert_single_file(  # pylint: disable=too-many-positional-arguments
    in_path: str,
    out_path: Optional[str],
    convert_fn: Callable[[IO, IO], None],
    skip: bool,
    skippable: Tuple[Type[BaseException], ...],
    quiet: bool = False,
) -> bool:
    """Convert a single file.  Returns ``True`` on success, ``False`` if skipped."""
    pass


def _convert_directory(  # pylint: disable=too-many-positional-arguments,too-many-locals
    in_path: str,
    out_path: Optional[str],
    convert_fn: Callable[[IO, IO], None],
    skip: bool,
    skippable: Tuple[Type[BaseException], ...],
    in_extensions: Set[str],
    out_extension: str,
    quiet: bool = False,
) -> bool:
    """Convert all matching files in a directory.  Returns ``True`` if any were skipped."""
    pass


def _convert_multiple_files(  # pylint: disable=too-many-positional-arguments
    in_paths: List[str],
    out_path: str,
    convert_fn: Callable[[IO, IO], None],
    skip: bool,
    skippable: Tuple[Type[BaseException], ...],
    out_extension: str,
    quiet: bool = False,
) -> bool:
    """Convert multiple files into an output directory.

    Preserves relative path structure to avoid basename collisions when
    files from different directories share the same name.  Returns ``True``
    if any files were skipped.
    """
    pass


def _convert_single_stream(
    in_file: IO,
    convert_fn: Callable[[IO, IO], None],
    skip: bool,
    skippable: Tuple[Type[BaseException], ...],
) -> bool:
    """Convert from a stream (e.g. stdin) to stdout.  Returns ``True`` on success."""
    pass
