"""
IO module for animated video thumbnails.

This module contains all side effect operations including video loading,
clip creation, GIF export, and compression. These functions interact with
the filesystem and external processes.
"""

from .video_io import (
    load_video,
    create_clips_parallel,
    create_clips_sequential,
)

from .gif_io import (
    export_gif_optimized,
    compress_gif,
)

__all__ = [
    "load_video",
    "create_clips_parallel",
    "create_clips_sequential",
    "export_gif_optimized",
    "compress_gif",
]
