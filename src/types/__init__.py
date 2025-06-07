"""
Types module for animated video thumbnails.

This module contains all data models and type definitions used throughout the application.
All types are immutable (frozen dataclasses) following functional programming principles.
"""

from .models import (
    ProcessingConfig,
    CompressionConfig,
    Config,
    TimeStamp,
    ClipMetadata,
    ClipTask,
)

__all__ = [
    "ProcessingConfig",
    "CompressionConfig",
    "Config",
    "TimeStamp",
    "ClipMetadata",
    "ClipTask",
]
