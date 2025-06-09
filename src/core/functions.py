"""
Pure functions for animated video thumbnails.

This module contains deterministic functions without side effects.
All functions are pure - they return the same output for the same input
and don't modify external state.
"""

import os
import uuid
from typing import List
from moviepy.editor import VideoFileClip, ColorClip, CompositeVideoClip

from ..types.models import TimeStamp, ClipMetadata, Config, CompressionConfig


def generate_timestamps(video_duration: float, clip_duration: int, interval: int, max_clips: int) -> List[TimeStamp]:
    """
    Generate timestamps for video clips.

    Args:
        video_duration: Total duration of the video in seconds
        clip_duration: Duration of each clip in seconds
        interval: Interval between clips in seconds
        max_clips: Maximum number of clips to generate

    Returns:
        List of TimeStamp objects representing clip start times
    """
    return [
        TimeStamp(t)
        for t in range(0, int(video_duration) - clip_duration, interval)
    ][:max_clips]


def create_processing_metadata(timestamps: List[TimeStamp], config: Config) -> List[ClipMetadata]:
    """
    Create metadata for clip processing.

    Args:
        timestamps: List of start timestamps for clips
        config: Main application configuration

    Returns:
        List of ClipMetadata objects with processing information
    """
    return [
        ClipMetadata(
            start_time=ts,
            duration=config.clip_duration,
            height=config.processing.processing_height,
            index=i
        )
        for i, ts in enumerate(timestamps)
    ]


def build_gifsicle_command(input_path: str, output_path: str, config: CompressionConfig) -> List[str]:
    """
    Build comprehensive gifsicle command with optimization and lossy compression.

    Args:
        input_path: Path to input GIF file
        output_path: Path for output compressed GIF
        config: Compression configuration settings

    Returns:
        List of command arguments for gifsicle
    """
    cmd = [
        "gifsicle",
        f"-O{config.optimization_level}",
        f"--lossy={config.lossy_level}",
        f"--colors={config.max_colors}",
        input_path
    ]

    if config.careful_optimization:
        cmd.insert(-1, "--careful")

    cmd.extend(["-o", output_path])
    return cmd


def create_temp_filename(base_dir: str, index: int) -> str:
    """
    Create unique temporary filename.

    Args:
        base_dir: Base directory for temporary files
        index: Clip index for naming

    Returns:
        Full path to temporary file with unique identifier
    """
    unique_id = str(uuid.uuid4())[:8]
    return os.path.join(base_dir, f"clip_{index:03d}_{unique_id}.gif")


def create_grid_layout(clips: List[VideoFileClip], cols: int, rows: int, padding: int = 5) -> CompositeVideoClip:
    """
    Arrange clips into grid layout.

    Args:
        clips: List of video clips to arrange
        cols: Number of columns in grid
        rows: Number of rows in grid
        padding: Padding between clips in pixels

    Returns:
        grid layout of clips
    """
    # Get dimensions from first clip
    clip_width, clip_height = clips[0].size

    # Calculate total grid dimensions including padding
    total_width = (cols * clip_width) + ((cols - 1) * padding)
    total_height = (rows * clip_height) + ((rows - 1) * padding)

    grid = []
    for row in range(rows):
        start_idx = row * cols
        end_idx = start_idx + cols
        grid.append(clips[start_idx:end_idx])

    positioned_clips = []
    for row_idx, row_clips in enumerate(grid):
        for col_idx, clip in enumerate(row_clips):
            x_pos = col_idx * (clip_width + padding)
            y_pos = row_idx * (clip_height + padding)
            positioned_clips.append(clip.set_position((x_pos, y_pos)))

    return CompositeVideoClip(
            positioned_clips,
            size=(total_width, total_height),
            bg_color=(0, 0, 0)
        )


def pad_clips_to_grid_size(clips: List[VideoFileClip], target_size: int) -> List[VideoFileClip]:
    """
    Pad clips list to match grid requirements.

    Args:
        clips: List of video clips
        target_size: Required number of clips for grid

    Returns:
        Padded list of clips with transparent clips as needed

    Raises:
        ValueError: If clips list is empty
    """
    if not clips:
        raise ValueError("Cannot pad empty clips list")

    padded = clips.copy()
    if len(padded) > 0:
        transparent_clip = clips[0].fx(lambda clip: clip.set_opacity(0))
        while len(padded) < target_size:
            padded.append(transparent_clip)

    return padded
