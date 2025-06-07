"""
Config module for animated video thumbnails.

This module contains configuration management including default settings
and configuration factory functions following functional programming principles.
"""

from .defaults import (
    create_default_processing_config,
    create_default_compression_config,
    create_default_config,
)

__all__ = [
    "create_default_processing_config",
    "create_default_compression_config",
    "create_default_config",
]
