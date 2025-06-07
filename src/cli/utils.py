"""
CLI utility functions for animated video thumbnails.

This module provides helper functions for the command-line interface including
formatting, validation, progress display, and configuration helpers.
All functions follow functional programming principles.
"""

import os
import importlib.util
import sys
from typing import Tuple, Dict, Any
from pathlib import Path

from ..types.models import Config


def print_config_summary(config: Config) -> None:
    """
    Print a formatted summary of the configuration.

    Args:
        config: Configuration object to summarize
    """
    print("📋 Configuration Summary")
    print("=" * 40)
    print(f"📹 Input:         {config.video_path}")
    print(f"📄 Output:        {config.compressed_output_path}")
    print(f"📐 Grid:          {config.cols}x{config.rows}")
    print(f"⏱️  Clip duration: {config.clip_duration}s")
    print(f"📏 Interval:      {config.interval}s")
    print(f"🎞️  Final FPS:     {config.fps}")
    print("📊 Processing:")
    print(f"   Height:        {config.processing.processing_height}px")
    print(f"   Processing FPS: {config.processing.processing_fps}")
    print(f"   Parallel:      {config.processing.enable_parallel}")
    print(f"   Workers:       {config.processing.max_workers or 'auto'}")
    print("🗜️  Compression:")
    print(f"   Lossy level:   {config.compression.lossy_level}")
    print(f"   Colors:        {config.compression.max_colors}")
    print(f"   Optimization:  {config.compression.optimization_level}")
    print("=" * 40)


def print_progress(current: int, total: int, message: str = "", width: int = 50) -> None:
    """
    Print a progress bar to the console.

    Args:
        current: Current progress value
        total: Total progress value
        message: Optional message to display
        width: Width of the progress bar in characters
    """
    if total <= 0:
        return

    percent = min(100, (current / total) * 100)
    filled = int(width * current // total)
    bar = "█" * filled + "-" * (width - filled)

    prefix = f"{message} " if message else ""
    print(f"\r{prefix}|{bar}| {percent:.1f}% ({current}/{total})", end="", flush=True)

    if current >= total:
        print()  # New line when complete


def format_duration(seconds: float) -> str:
    """
    Format duration in seconds to human-readable string.

    Args:
        seconds: Duration in seconds

    Returns:
        Formatted duration string (e.g., "2m 30s", "1h 15m 30s")
    """
    if seconds < 60:
        return f"{seconds:.1f}s"

    minutes = int(seconds // 60)
    remaining_seconds = seconds % 60

    if minutes < 60:
        return f"{minutes}m {remaining_seconds:.0f}s"

    hours = minutes // 60
    remaining_minutes = minutes % 60

    if remaining_minutes == 0 and remaining_seconds < 1:
        return f"{hours}h"
    elif remaining_seconds < 1:
        return f"{hours}h {remaining_minutes}m"
    else:
        return f"{hours}h {remaining_minutes}m {remaining_seconds:.0f}s"


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in bytes to human-readable string.

    Args:
        size_bytes: Size in bytes

    Returns:
        Formatted size string (e.g., "1.5 MB", "234 KB")
    """
    if size_bytes == 0:
        return "0 B"

    units = ["B", "KB", "MB", "GB", "TB"]
    unit_index = 0
    size = float(size_bytes)

    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1

    if unit_index == 0:
        return f"{int(size)} {units[unit_index]}"
    else:
        return f"{size:.1f} {units[unit_index]}"


def validate_video_file(filepath: str) -> bool:
    """
    Validate if a file is a supported video file.

    Args:
        filepath: Path to the file to validate

    Returns:
        True if file appears to be a valid video file
    """
    if not os.path.exists(filepath):
        return False

    if not os.path.isfile(filepath):
        return False

    # Check file extension
    video_extensions = {
        '.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm',
        '.m4v', '.3gp', '.ogv', '.ts', '.mts', '.m2ts', '.mpg',
        '.mpeg', '.m2v', '.vob', '.asf', '.rm', '.rmvb', '.dv'
    }

    extension = Path(filepath).suffix.lower()
    if extension not in video_extensions:
        return False

    # Check file size (should be > 0)
    try:
        if os.path.getsize(filepath) == 0:
            return False
    except OSError:
        return False

    return True


def suggest_config(video_duration: float, video_size: Tuple[int, int]) -> Dict[str, Any]:
    """
    Suggest optimal configuration based on video properties.

    Args:
        video_duration: Duration of video in seconds
        video_size: Video resolution as (width, height) tuple

    Returns:
        Dictionary with suggested configuration parameters
    """
    width, height = video_size

    suggestions = {}

    # Suggest grid size based on duration
    if video_duration < 60:  # Short video
        suggestions['grid'] = (2, 2)
        suggestions['interval'] = 15
        suggestions['clip_duration'] = 2
    elif video_duration < 300:  # Medium video (< 5 min)
        suggestions['grid'] = (3, 3)
        suggestions['interval'] = 30
        suggestions['clip_duration'] = 2
    elif video_duration < 1800:  # Long video (< 30 min)
        suggestions['grid'] = (4, 4)
        suggestions['interval'] = 60
        suggestions['clip_duration'] = 3
    else:  # Very long video
        suggestions['grid'] = (5, 5)
        suggestions['interval'] = 120
        suggestions['clip_duration'] = 3

    # Suggest processing height based on source resolution
    if height >= 1080:
        suggestions['processing_height'] = 240
    elif height >= 720:
        suggestions['processing_height'] = 180
    elif height >= 480:
        suggestions['processing_height'] = 120
    else:
        suggestions['processing_height'] = max(80, height // 4)

    # Suggest FPS based on source quality
    if width * height > 1920 * 1080:  # 4K+
        suggestions['fps'] = 20
        suggestions['processing_fps'] = 8
    elif width * height > 1280 * 720:  # HD+
        suggestions['fps'] = 25
        suggestions['processing_fps'] = 10
    else:  # SD
        suggestions['fps'] = 30
        suggestions['processing_fps'] = 12

    return suggestions


def get_terminal_width() -> int:
    """
    Get the current terminal width.

    Returns:
        Terminal width in characters (default 80 if unable to determine)
    """
    try:
        return os.get_terminal_size().columns
    except OSError:
        return 80


def print_banner(text: str, char: str = "=") -> None:
    """
    Print a banner with text centered and surrounded by characters.

    Args:
        text: Text to display in banner
        char: Character to use for banner border
    """
    width = get_terminal_width()
    text_len = len(text)

    if text_len + 4 >= width:
        print(text)
        return

    padding = (width - text_len - 2) // 2
    border = char * width

    print(border)
    print(f"{char}{' ' * padding}{text}{' ' * padding}{char}")
    print(border)


def print_error(message: str) -> None:
    """
    Print an error message to stderr with formatting.

    Args:
        message: Error message to display
    """
    print(f"❌ Error: {message}", file=sys.stderr)


def print_warning(message: str) -> None:
    """
    Print a warning message with formatting.

    Args:
        message: Warning message to display
    """
    print(f"⚠️  Warning: {message}")


def print_success(message: str) -> None:
    """
    Print a success message with formatting.

    Args:
        message: Success message to display
    """
    print(f"✅ {message}")


def print_info(message: str) -> None:
    """
    Print an info message with formatting.

    Args:
        message: Info message to display
    """
    print(f"ℹ️  {message}")


def confirm_action(message: str, default: bool = False) -> bool:
    """
    Ask user for confirmation.

    Args:
        message: Confirmation message to display
        default: Default response if user just presses Enter

    Returns:
        True if user confirms, False otherwise
    """
    suffix = " [Y/n]" if default else " [y/N]"

    try:
        response = input(f"{message}{suffix}: ").strip().lower()

        if not response:
            return default

        return response.startswith('y')

    except (KeyboardInterrupt, EOFError):
        print()
        return False


def create_output_directory(output_path: str) -> bool:
    """
    Create output directory if it doesn't exist.

    Args:
        output_path: Output file path

    Returns:
        True if directory exists or was created successfully
    """
    output_dir = os.path.dirname(output_path)

    if not output_dir:
        return True

    if os.path.exists(output_dir):
        return True

    try:
        os.makedirs(output_dir, exist_ok=True)
        print_info(f"Created output directory: {output_dir}")
        return True
    except OSError as e:
        print_error(f"Failed to create directory {output_dir}: {e}")
        return False


def check_dependencies() -> Tuple[bool, list]:
    """
    Check if required dependencies are available.

    Returns:
        Tuple of (all_available, missing_dependencies)
    """
    missing = []

    # Check Python packages
    if importlib.util.find_spec('moviepy') is None:
        missing.append("moviepy")


    if importlib.util.find_spec('PIL') is None:
        missing.append("Pillow")

    # Check external tools
    import subprocess
    try:
        subprocess.run(['gifsicle', '--version'],
                      capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        missing.append("gifsicle")

    return len(missing) == 0, missing


def print_version_info() -> None:
    """Print version information for the application and dependencies."""
    print("🎬 Animated Video Thumbnails v0.0.1")
    print("Dependencies:")

    try:
        import moviepy
        print(f"  - MoviePy: {moviepy.__version__}")
    except (ImportError, AttributeError):
        print("  - MoviePy: Not available")

    try:
        import PIL
        print(f"  - Pillow: {PIL.__version__}")
    except (ImportError, AttributeError):
        print("  - Pillow: Not available")

    import subprocess
    try:
        result = subprocess.run(['gifsicle', '--version'],
                               capture_output=True, text=True)
        version_line = result.stdout.split('\n')[0]
        print(f"  - gifsicle: {version_line}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("  - gifsicle: Not available")


def estimate_processing_time(config: Config, video_duration: float) -> float:
    """
    Estimate processing time based on configuration and video duration.

    Args:
        config: Configuration object
        video_duration: Video duration in seconds

    Returns:
        Estimated processing time in seconds
    """
    # Base time estimation factors
    base_time_per_clip = 2.0  # seconds per clip

    # Calculate number of clips
    num_clips = min(
        config.cols * config.rows,
        max(1, int(video_duration // config.interval))
    )

    # Adjust for processing settings
    processing_factor = 1.0

    # FPS factor
    if config.processing.processing_fps <= 5:
        processing_factor *= 0.7
    elif config.processing.processing_fps >= 15:
        processing_factor *= 1.5

    # Height factor
    if config.processing.processing_height <= 120:
        processing_factor *= 0.8
    elif config.processing.processing_height >= 240:
        processing_factor *= 1.3

    # Parallel processing factor
    if config.processing.enable_parallel:
        workers = config.processing.max_workers or 4
        processing_factor *= (1.0 / min(workers, num_clips))

    # Compression factor
    compression_factor = 1.2  # Additional time for compression

    estimated_time = (
        num_clips * base_time_per_clip * processing_factor * compression_factor
    )

    return max(10, estimated_time)  # Minimum 10 seconds


def show_progress_estimate(config: Config, video_duration: float) -> None:
    """
    Show estimated processing time and progress information.

    Args:
        config: Configuration object
        video_duration: Video duration in seconds
    """
    estimated_time = estimate_processing_time(config, video_duration)
    num_clips = min(
        config.cols * config.rows,
        max(1, int(video_duration // config.interval))
    )

    print("📊 Processing estimate:")
    print(f"   Clips to process: {num_clips}")
    print(f"   Estimated time: {format_duration(estimated_time)}")

    if config.processing.enable_parallel:
        workers = config.processing.max_workers or "auto"
        print(f"   Parallel workers: {workers}")
