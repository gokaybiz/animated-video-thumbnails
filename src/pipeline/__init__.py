"""
Pipeline module for animated video thumbnails.

This module contains the main orchestration pipeline that coordinates
all the processing steps to create animated video thumbnails.
"""

from .main_pipeline import create_video_thumbnails

__all__ = [
    "create_video_thumbnails",
]
