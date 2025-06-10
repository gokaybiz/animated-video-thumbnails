"""
Animated Video Thumbnails - A functional programming approach to video preview generation.

This package provides tools for creating animated GIF thumbnails from video files
using functional programming principles with immutable data structures and functions.

Main Components:
- types: Immutable data models and type definitions
- core: Functions and business logic
- io: Side effect operations (file I/O, external processes)
- pipeline: Main orchestration and workflow
- config: Configuration management and defaults

Example Usage:
    from src.config import create_default_config
    from src.pipeline import create_video_preview

    config = create_default_config("path/to/video.mp4")
    create_video_preview(config)
"""

from .types import (
    ProcessingConfig,
    CompressionConfig,
    Config,
    TimeStamp,
    ClipMetadata,
    ClipTask,
)

from .core import (
    generate_timestamps,
    create_processing_metadata,
    build_gifsicle_command,
    create_temp_filename,
    create_grid_layout,
    pad_clips_to_grid_size,
    create_annotation_function,
    process_single_clip,
)

from .io import (
    load_video,
    create_clips_parallel,
    create_clips_sequential,
    export_gif_optimized,
    compress_gif,
)

from .pipeline import (
    create_video_thumbnails,
)

from .config import (
    create_default_processing_config,
    create_default_compression_config,
    create_default_config,
)

from .cli import (
    create_cli_parser,
    parse_args,
    validate_cli_args,
    cmd_generate,
    cmd_preview,
    cmd_batch,
    cmd_info,
    print_config_summary,
    print_progress,
    format_duration,
    format_file_size,
    validate_video_file,
    suggest_config,
)

__version__ = "1.0.0"
__author__ = "Animated Video Thumbnails Team"

__all__ = [
    # Types
    "ProcessingConfig",
    "CompressionConfig",
    "Config",
    "TimeStamp",
    "ClipMetadata",
    "ClipTask",

    # Core functions
    "generate_timestamps",
    "create_processing_metadata",
    "build_gifsicle_command",
    "create_temp_filename",
    "create_grid_layout",
    "pad_clips_to_grid_size",
    "create_annotation_function",
    "process_single_clip",

    # IO operations
    "load_video",
    "create_clips_parallel",
    "create_clips_sequential",
    "export_gif_optimized",
    "compress_gif",

    # Pipeline
    "create_video_thumbnails",

    # Configuration
    "create_default_processing_config",
    "create_default_compression_config",
    "create_default_config",

    # CLI utilities
    "create_cli_parser",
    "parse_args",
    "validate_cli_args",
    "cmd_generate",
    "cmd_preview",
    "cmd_batch",
    "cmd_info",
    "print_config_summary",
    "print_progress",
    "format_duration",
    "format_file_size",
    "validate_video_file",
    "suggest_config",
]
