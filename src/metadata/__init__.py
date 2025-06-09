"""
Metadata module for animated video thumbnails.

This module provides comprehensive metadata extraction and rendering capabilities
using pymediainfo for accurate and detailed media information. All functions
follow functional programming principles.
"""

from .extraction import (
    extract_complete_metadata,
    extract_file_metadata,
    extract_video_track_metadata,
    extract_audio_metadata,
    format_file_size,
    format_duration_ms,
    calculate_aspect_ratio,
    validate_media_file,
    get_pymediainfo_version,
    extract_audio_info,
)

__all__ = [
    "extract_complete_metadata",
    "extract_file_metadata",
    "extract_video_track_metadata",
    "extract_audio_metadata",
    "format_file_size",
    "format_duration_ms",
    "calculate_aspect_ratio",
    "validate_media_file",
    "get_pymediainfo_version",
    "extract_audio_info",
]
