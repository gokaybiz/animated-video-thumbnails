#!/usr/bin/env python3
"""
Animated Video Thumbnails - Main Entry Point

A functional programming approach to creating animated GIF thumbnails from video files.
This script demonstrates how to use the modular animated video thumbnails package.

Usage:
    python main.py

Features:
    - Parallel processing for faster clip creation
    - Configurable quality and compression settings
    - Functional programming with immutable data structures
    - Clean separation of concerns across modules

Requirements:
    - moviepy
    - Pillow
    - gifsicle (for compression)
"""

from src.config.defaults import (
    create_fast_config,
)
from src.pipeline.main_pipeline import create_video_preview


def main() -> None:
    """
    Main entry point for animated video thumbnail generation.

    This function demonstrates different configuration options
    and runs the video preview generation pipeline.
    """
    # Example video path - update this to your video file
    video_path = "test_files/Big Buck Bunny 1080p 60FPS.mp4"


    # Fast processing
    config = create_fast_config(
        video_path=video_path,
        output_path="Big Buck Bunny_fast.gif",
        compressed_output_path="Big Buck Bunny_fast_compressed.gif"
    )


    print("Starting animated video thumbnail generation...")
    print(f"Input: {config.video_path}")
    print(f"Output: {config.compressed_output_path}")
    print(f"Grid: {config.cols}x{config.rows} with padding {config.grid_padding}px")
    print(f"Clip duration: {config.clip_duration}s")
    print(f"Interval: {config.interval}s")
    print(f"Final FPS: {config.fps}")
    print(f"Parallel processing: {config.processing.enable_parallel}")
    print("-" * 50)

    try:
        # Run the main pipeline
        create_video_preview(config)

        print("-" * 50)
        print("Success! Animated thumbnail created successfully.")

    except FileNotFoundError as e:
        print(f"❌ Error: File not found - {e}")
        print("Please check that the video file exists and gifsicle is installed.")

    except Exception as e:
        print(f"❌ Error during processing: {e}")
        print("Please check the error message above for details.")


if __name__ == "__main__":
    main()
