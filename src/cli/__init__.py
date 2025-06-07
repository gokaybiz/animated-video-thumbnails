"""
CLI module for animated video thumbnails.

This module provides command-line interface utilities and argument parsing
for the animated video thumbnails application. It includes parsers for
different commands and validation functions.
"""

from .parser import (
    create_cli_parser,
    parse_args,
    validate_cli_args,
)

from .commands import (
    cmd_generate,
    cmd_preview,
    cmd_batch,
    cmd_info,
)

from .utils import (
    print_config_summary,
    print_progress,
    format_duration,
    format_file_size,
    validate_video_file,
    suggest_config,
)

__all__ = [
    # Parser functions
    "create_cli_parser",
    "parse_args",
    "validate_cli_args",

    # Command handlers
    "cmd_generate",
    "cmd_preview",
    "cmd_batch",
    "cmd_info",

    # Utility functions
    "print_config_summary",
    "print_progress",
    "format_duration",
    "format_file_size",
    "validate_video_file",
    "suggest_config",
]
