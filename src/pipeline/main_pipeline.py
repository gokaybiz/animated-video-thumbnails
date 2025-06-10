"""
Main pipeline for animated video thumbnails.

This module contains the main orchestration function that coordinates
all processing steps to create animated video thumbnails from video files.
"""

import os
import time

from ..types.models import Config, extract_metadata_information
from ..core.functions import (
    generate_timestamps,
    create_processing_metadata,
    create_grid_layout,
    pad_clips_to_grid_size,
    combine_metadata_with_grid,
)
from ..io.video_io import load_video, create_clips_parallel
from ..io.gif_io import export_gif_optimized, compress_gif


def create_video_thumbnails(config: Config) -> None:
    """
    Optimized main pipeline with parallel processing.

    This function orchestrates the entire process of creating animated
    video thumbnails from a source video file. It follows these steps:

    1. Load video metadata
    2. Generate timestamps for clips
    3. Create processing metadata
    4. Process clips (parallel or sequential)
    5. Arrange clips in grid layout
    6. Export final GIF
    7. Compress the output

    Args:
        config: Complete configuration object with all settings

    Raises:
        ValueError: If no clips were successfully created
        Various IO exceptions from underlying operations
    """
    overall_start = time.time()

    # Load video to get metadata
    print("Loading video metadata...")
    video = load_video(config.video_path)
    video_duration = video.duration

    # Extract metadata if needed
    metadata = None
    if config.include_metadata:
        metadata = extract_metadata_information(config.video_path)

    video.close()

    # Generate timestamps and metadata
    timestamps = generate_timestamps(
        video_duration,
        config.clip_duration,
        config.interval,
        config.cols * config.rows
    )

    metadatas = create_processing_metadata(timestamps, config)
    print(f"Generated {len(metadatas)} clips to process")

    # Create clips (parallel or sequential)
    clip_start = time.time()
    clips = create_clips_parallel(config.video_path, metadatas, config)
    clip_time = time.time() - clip_start
    print(f"Clip processing completed in {clip_time:.1f}s")

    if not clips:
        raise ValueError("No clips were successfully created")

    # Pad and arrange
    print("Arranging grid layout...")
    padded_clips = pad_clips_to_grid_size(clips, config.cols * config.rows)
    grid_clip = create_grid_layout(padded_clips, config.cols, config.rows, config.grid_padding)

    # Optionally combine with metadata header
    final_clip = grid_clip
    if config.include_metadata and metadata:
        print("Adding metadata header...")
        final_clip = combine_metadata_with_grid(metadata, grid_clip)

    # Create grid and export
    export_gif_optimized(final_clip, config.output_path, config.fps)

    # Clean up clips
    for clip in clips:
        if clip:
            clip.close()

    if final_clip is not grid_clip:
        final_clip.close()
    grid_clip.close()

    # Compress the GIF
    print("Starting final compression...")
    compress_gif(config.output_path, config.compressed_output_path, config.compression)

    # Clean up and report
    if os.path.exists(config.compressed_output_path):
        os.remove(config.output_path)
        print(f"Removed original file: {config.output_path}")

    total_time = time.time() - overall_start
    print(f"\nCompleted! Total processing time: {total_time:.1f}s")
    print(f"Final output: {config.compressed_output_path}")
