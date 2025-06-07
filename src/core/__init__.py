"""
Core module for animated video thumbnails.

This module contains pure functions and business logic without side effects.
All functions in this module are deterministic and can be safely composed.
"""

from .functions import (
    generate_timestamps,
    create_processing_metadata,
    build_gifsicle_command,
    create_temp_filename,
    create_grid_layout,
    pad_clips_to_grid_size,
)

from .processing import (
    create_annotation_function,
    process_single_clip,
)

__all__ = [
    "generate_timestamps",
    "create_processing_metadata",
    "build_gifsicle_command",
    "create_temp_filename",
    "create_grid_layout",
    "pad_clips_to_grid_size",
    "create_annotation_function",
    "process_single_clip",
]
