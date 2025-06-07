#!/usr/bin/env python3
"""
Main CLI entry point for animated video thumbnails.

This script provides a command-line interface for generating animated GIF
thumbnails from video files. It integrates all the CLI utilities and provides
a clean entry point for the application.

Usage:
    python cli.py generate video.mp4
    python cli.py preview video.mp4
    python cli.py batch *.mp4
    python cli.py info video.mp4
"""

import sys
import os
from typing import Optional, List

# Add the src directory to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.cli.parser import parse_args, validate_cli_args
from src.cli.commands import execute_command
from src.cli.utils import (
    print_error,
    print_warning,
    check_dependencies,
    print_version_info
)


def main(args: Optional[List[str]] = None) -> int:
    """
    Main CLI entry point.

    Args:
        args: Command-line arguments (default: sys.argv[1:])

    Returns:
        Exit code (0 for success, 1 for error)
    """
    parsed_args = None

    try:
        parsed_args = parse_args(args)

        # Handle version request
        if hasattr(parsed_args, 'version') and parsed_args.version:
            print_version_info()
            return 0

        # Check dependencies before proceeding
        deps_available, missing_deps = check_dependencies()
        if not deps_available:
            print_error("Missing required dependencies:")
            for dep in missing_deps:
                print(f"  - {dep}")
            print("\nPlease install missing dependencies:")
            if 'moviepy' in missing_deps:
                print("  pip install moviepy")
            if 'Pillow' in missing_deps:
                print("  pip install Pillow")
            if 'gifsicle' in missing_deps:
                print("  # Ubuntu/Debian: sudo apt-get install gifsicle")
                print("  # macOS: brew install gifsicle")
                print("  # Windows: Download from https://www.lcdf.org/gifsicle/")
            return 1

        # Validate arguments
        valid, errors = validate_cli_args(parsed_args)
        if not valid:
            print_error("Invalid arguments:")
            for error in errors:
                print(f"  - {error}")
            return 1

        # Execute the appropriate command
        return execute_command(parsed_args)

    except KeyboardInterrupt:
        print("\n🛑 Operation cancelled by user")
        return 1

    except ImportError as e:
        print_error(f"Import error: {e}")
        print_warning("Make sure all dependencies are installed")
        return 1

    except Exception as e:
        print_error(f"Unexpected error: {e}")
        if parsed_args is not None and hasattr(parsed_args, 'verbose') and parsed_args.verbose:
            import traceback
            traceback.print_exc()
        return 1


def cli_help():
    """Print CLI help information."""
    print("""
🎬 Animated Video Thumbnails CLI

Generate animated GIF thumbnails from video files using functional programming principles.

Commands:
  generate    Generate animated thumbnail from video
  preview     Generate quick preview thumbnail
  batch       Process multiple videos
  info        Show video information

Examples:
  python cli.py generate video.mp4
  python cli.py generate video.mp4 --preset fast
  python cli.py generate video.mp4 --grid 4x3 --fps 30
  python cli.py preview video.mp4
  python cli.py batch *.mp4 --preset quality
  python cli.py info video.mp4 --suggest-config

For detailed help on any command:
  python cli.py COMMAND --help

Global Options:
  -h, --help     Show this help message
  -v, --verbose  Enable verbose output
  --dry-run      Show what would be done without processing
  --version      Show version information

Presets:
  default  - Balanced quality and speed (3x5 grid, 25fps)
  fast     - Speed optimized (2x3 grid, 15fps)
  quality  - Quality optimized (4x6 grid, 30fps)

Requirements:
  - Python 3.7+
  - moviepy (pip install moviepy)
  - Pillow (pip install Pillow)
  - gifsicle (system package)
""")


if __name__ == "__main__":
    # If no arguments provided, show help
    if len(sys.argv) == 1:
        cli_help()
        sys.exit(0)

    # Handle help requests
    if sys.argv[1] in ['-h', '--help', 'help']:
        cli_help()
        sys.exit(0)

    # Execute main CLI
    exit_code = main()
    sys.exit(exit_code)
