"""
CLI argument parser for animated video thumbnails.

This module provides comprehensive command-line argument parsing with
validation and help text for the animated video thumbnails application.
Follows functional programming principles with immutable configurations.
"""

import argparse
import os
import sys
from typing import List, Optional, Tuple
from pathlib import Path
from dataclasses import replace

from ..types.models import Config


def create_cli_parser() -> argparse.ArgumentParser:
    """
    Create the main CLI argument parser with all subcommands and options.

    Returns:
        Configured ArgumentParser with all CLI options
    """
    parser = argparse.ArgumentParser(
        prog="animated-thumbnails",
        description="Create animated GIF thumbnails from video files using functional programming principles",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s generate video.mp4                          # Basic usage with defaults
  %(prog)s generate video.mp4 -o output.gif           # Custom output filename
  %(prog)s generate video.mp4 --preset fast           # Use fast preset
  %(prog)s generate video.mp4 --grid 4x3              # Custom grid size
  %(prog)s generate video.mp4 --quality high          # High quality preset
  %(prog)s preview video.mp4                          # Quick preview
  %(prog)s batch *.mp4                                # Process multiple files
  %(prog)s info video.mp4                             # Show video information

Presets:
  default  - Balanced quality and speed (3x5 grid, 25fps)
  fast     - Speed optimized (2x3 grid, 15fps)
  quality  - Quality optimized (4x6 grid, 30fps)
        """
    )

    # Global options
    parser.add_argument(
        "--version",
        action="version",
        version="Animated Video Thumbnails 1.0.0"
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
    )

    # Create subparsers for different commands
    subparsers = parser.add_subparsers(
        dest="command",
        help="Available commands",
        metavar="COMMAND"
    )

    # Generate command
    _add_generate_parser(subparsers)

    # Preview command
    _add_preview_parser(subparsers)

    # Batch command
    _add_batch_parser(subparsers)

    # Info command
    _add_info_parser(subparsers)

    return parser


def _add_generate_parser(subparsers) -> None:
    """Add the generate command parser."""
    generate_parser = subparsers.add_parser(
        "generate",
        help="Generate animated thumbnail from video",
        description="Create an animated GIF thumbnail from a video file with customizable settings"
    )

    # Input/Output
    generate_parser.add_argument(
        "input",
        help="Input video file path"
    )

    generate_parser.add_argument(
        "-o", "--output",
        help="Output GIF file path (default: input_name.gif)"
    )

    generate_parser.add_argument(
        "--no-compress",
        action="store_true",
        help="Skip compression step"
    )

    generate_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without actually processing"
    )

    # Presets
    generate_parser.add_argument(
        "--preset",
        choices=["default", "fast", "quality"],
        default="default",
        help="Use predefined configuration preset (default: %(default)s)"
    )

    # Grid layout
    generate_parser.add_argument(
        "--grid",
        metavar="COLSxROWS",
        help="Grid layout (e.g., 3x5, 4x3)"
    )

    # Timing options
    generate_parser.add_argument(
        "--clip-duration",
        type=int,
        metavar="SECONDS",
        help="Duration of each clip in seconds"
    )

    generate_parser.add_argument(
        "--interval",
        type=int,
        metavar="SECONDS",
        help="Interval between clips in seconds"
    )

    generate_parser.add_argument(
        "--fps",
        type=int,
        metavar="FPS",
        help="Final output frames per second"
    )

    # Processing options
    generate_parser.add_argument(
        "--workers",
        type=int,
        metavar="N",
        help="Number of parallel workers (default: auto-detect)"
    )

    generate_parser.add_argument(
        "--no-parallel",
        action="store_true",
        help="Disable parallel processing"
    )

    generate_parser.add_argument(
        "--processing-fps",
        type=int,
        metavar="FPS",
        help="Processing frames per second (lower = faster)"
    )

    generate_parser.add_argument(
        "--height",
        type=int,
        metavar="PIXELS",
        help="Processing height in pixels"
    )

    # Compression options
    generate_parser.add_argument(
        "--lossy",
        type=int,
        metavar="LEVEL",
        help="Lossy compression level (0-200)"
    )

    generate_parser.add_argument(
        "--colors",
        type=int,
        metavar="N",
        help="Maximum number of colors"
    )

    generate_parser.add_argument(
        "--optimization",
        type=int,
        choices=[1, 2, 3],
        metavar="LEVEL",
        help="Optimization level (1-3)"
    )


def _add_preview_parser(subparsers) -> None:
    """Add the preview command parser."""
    preview_parser = subparsers.add_parser(
        "preview",
        help="Generate quick preview thumbnail",
        description="Create a fast, low-quality preview for quick feedback"
    )

    preview_parser.add_argument(
        "input",
        help="Input video file path"
    )

    preview_parser.add_argument(
        "-o", "--output",
        help="Output preview file path (default: input_name_preview.gif)"
    )

    preview_parser.add_argument(
        "--grid",
        metavar="COLSxROWS",
        default="2x2",
        help="Preview grid layout (default: %(default)s)"
    )


def _add_batch_parser(subparsers) -> None:
    """Add the batch command parser."""
    batch_parser = subparsers.add_parser(
        "batch",
        help="Process multiple videos",
        description="Process multiple video files with the same settings"
    )

    batch_parser.add_argument(
        "inputs",
        nargs="+",
        help="Input video file paths (supports wildcards)"
    )

    batch_parser.add_argument(
        "--preset",
        choices=["default", "fast", "quality"],
        default="fast",
        help="Configuration preset for batch processing (default: %(default)s)"
    )

    batch_parser.add_argument(
        "--output-dir",
        help="Output directory (default: same as input files)"
    )

    batch_parser.add_argument(
        "--suffix",
        default="_thumb",
        help="Suffix for output files (default: %(default)s)"
    )

    batch_parser.add_argument(
        "--continue-on-error",
        action="store_true",
        help="Continue processing other files if one fails"
    )

    batch_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without actually processing"
    )


def _add_info_parser(subparsers) -> None:
    """Add the info command parser."""
    info_parser = subparsers.add_parser(
        "info",
        help="Show video information",
        description="Display information about a video file"
    )

    info_parser.add_argument(
        "input",
        help="Input video file path"
    )

    info_parser.add_argument(
        "--suggest-config",
        action="store_true",
        help="Suggest optimal configuration for this video"
    )


def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """
    Parse command-line arguments.

    Args:
        args: List of arguments to parse (default: sys.argv)

    Returns:
        Parsed arguments namespace
    """
    parser = create_cli_parser()

    # If no arguments provided, show help
    if args is None:
        args = sys.argv[1:]

    if not args:
        parser.print_help()
        sys.exit(1)

    return parser.parse_args(args)


def validate_cli_args(args: argparse.Namespace) -> Tuple[bool, List[str]]:
    """
    Validate parsed command-line arguments.

    Args:
        args: Parsed arguments namespace

    Returns:
        Tuple of (is_valid, error_messages)
    """
    errors = []

    # Validate input files exist
    if hasattr(args, 'input'):
        if not os.path.exists(args.input):
            errors.append(f"Input file does not exist: {args.input}")
        elif not _is_video_file(args.input):
            errors.append(f"Input file does not appear to be a video: {args.input}")

    if hasattr(args, 'inputs'):
        for input_file in args.inputs:
            if not os.path.exists(input_file):
                errors.append(f"Input file does not exist: {input_file}")
            elif not _is_video_file(input_file):
                errors.append(f"Input file does not appear to be a video: {input_file}")

    # Validate grid format
    if hasattr(args, 'grid') and args.grid:
        if not _validate_grid_format(args.grid):
            errors.append(f"Invalid grid format: {args.grid}. Use format like '3x5' or '4x3'")

    # Validate numeric ranges
    if hasattr(args, 'clip_duration') and args.clip_duration is not None:
        if args.clip_duration <= 0:
            errors.append("Clip duration must be positive")

    if hasattr(args, 'interval') and args.interval is not None:
        if args.interval <= 0:
            errors.append("Interval must be positive")

    if hasattr(args, 'fps') and args.fps is not None:
        if args.fps <= 0 or args.fps > 60:
            errors.append("FPS must be between 1 and 60")

    if hasattr(args, 'workers') and args.workers is not None:
        if args.workers <= 0:
            errors.append("Number of workers must be positive")

    if hasattr(args, 'lossy') and args.lossy is not None:
        if args.lossy < 0 or args.lossy > 200:
            errors.append("Lossy compression level must be between 0 and 200")

    if hasattr(args, 'colors') and args.colors is not None:
        if args.colors < 2 or args.colors > 256:
            errors.append("Number of colors must be between 2 and 256")

    # Validate output directory exists (for batch command)
    if hasattr(args, 'output_dir') and args.output_dir:
        if not os.path.isdir(args.output_dir):
            errors.append(f"Output directory does not exist: {args.output_dir}")

    return len(errors) == 0, errors


def args_to_config(args: argparse.Namespace) -> Config:
    """
    Convert CLI arguments to a Config object.

    Args:
        args: Parsed CLI arguments

    Returns:
        Config object with settings from CLI args
    """
    from ..config.defaults import (
        create_default_config,
        create_fast_config,
        create_quality_config
    )

    # Start with preset configuration
    preset = getattr(args, 'preset', 'default')

    if preset == 'fast':
        config = create_fast_config(args.input)
    elif preset == 'quality':
        config = create_quality_config(args.input)
    else:
        config = create_default_config(args.input)

    # Override with CLI arguments
    updates = {}

    # Output path
    if hasattr(args, 'output') and args.output:
        updates['output_path'] = args.output
        updates['compressed_output_path'] = args.output

    # Grid layout
    if hasattr(args, 'grid') and args.grid:
        cols, rows = _parse_grid(args.grid)
        updates['cols'] = cols
        updates['rows'] = rows

    # Timing
    if hasattr(args, 'clip_duration') and args.clip_duration is not None:
        updates['clip_duration'] = args.clip_duration

    if hasattr(args, 'interval') and args.interval is not None:
        updates['interval'] = args.interval

    if hasattr(args, 'fps') and args.fps is not None:
        updates['fps'] = args.fps

    # Processing options
    processing_updates = {}

    if hasattr(args, 'workers') and args.workers is not None:
        processing_updates['max_workers'] = args.workers

    if hasattr(args, 'no_parallel') and args.no_parallel:
        processing_updates['enable_parallel'] = False

    if hasattr(args, 'processing_fps') and args.processing_fps is not None:
        processing_updates['processing_fps'] = args.processing_fps

    if hasattr(args, 'height') and args.height is not None:
        processing_updates['processing_height'] = args.height

    if processing_updates:
        new_processing = replace(config.processing, **processing_updates)
        updates['processing'] = new_processing

    # Compression options
    compression_updates = {}

    if hasattr(args, 'lossy') and args.lossy is not None:
        compression_updates['lossy_level'] = args.lossy

    if hasattr(args, 'colors') and args.colors is not None:
        compression_updates['max_colors'] = args.colors

    if hasattr(args, 'optimization') and args.optimization is not None:
        compression_updates['optimization_level'] = args.optimization

    if compression_updates:
        new_compression = replace(config.compression, **compression_updates)
        updates['compression'] = new_compression

    # Apply updates
    if updates:
        config = replace(config, **updates)

    return config


def _is_video_file(filepath: str) -> bool:
    """Check if file appears to be a video file."""
    video_extensions = {
        '.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm',
        '.m4v', '.3gp', '.ogv', '.ts', '.mts', '.m2ts'
    }
    return Path(filepath).suffix.lower() in video_extensions


def _validate_grid_format(grid: str) -> bool:
    """Validate grid format string (e.g., '3x5')."""
    try:
        parts = grid.lower().split('x')
        if len(parts) != 2:
            return False
        cols, rows = int(parts[0]), int(parts[1])
        return cols > 0 and rows > 0
    except (ValueError, IndexError):
        return False


def _parse_grid(grid: str) -> Tuple[int, int]:
    """Parse grid string into (cols, rows) tuple."""
    parts = grid.lower().split('x')
    return int(parts[0]), int(parts[1])


def get_default_output_path(input_path: str, suffix: str = "") -> str:
    """
    Generate default output path from input path.

    Args:
        input_path: Input video file path
        suffix: Optional suffix to add before extension

    Returns:
        Default output path with .gif extension
    """
    path = Path(input_path)
    stem = path.stem + suffix
    return str(path.parent / f"{stem}.gif")


def print_help_and_exit(parser: argparse.ArgumentParser) -> None:
    """Print help message and exit."""
    parser.print_help()
    sys.exit(0)
