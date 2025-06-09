"""
GIF IO operations for animated video thumbnails.

This module handles GIF export and compression operations.
All functions in this module have side effects (file I/O, subprocess execution).
"""

import os
import subprocess
from moviepy import CompositeVideoClip, VideoFileClip
from typing import cast
from ..types.models import CompressionConfig
from ..core.functions import build_gifsicle_command


def export_gif_optimized(clip: CompositeVideoClip, output_path: str, final_fps: int) -> None:
    """
    Export GIF with final quality settings.

    Args:
        clip: VideoFileClip to export
        output_path: Path for output GIF file
        final_fps: Final frames per second for output
    """
    print(f"Exporting GIF at final quality: {final_fps}fps...")

    # Resize to final dimensions and set final fps
    final_clip = cast(
        VideoFileClip,
        clip.with_fps(final_fps)
    )
    final_clip.write_gif(output_path, fps=final_fps)
    final_clip.close()


def compress_gif(input_path: str, output_path: str, config: CompressionConfig) -> None:
    """
    Compress GIF using gifsicle with lossy compression.

    Args:
        input_path: Path to input GIF file
        output_path: Path for compressed output GIF
        config: Compression configuration settings

    Raises:
        subprocess.CalledProcessError: If gifsicle command fails
        FileNotFoundError: If gifsicle is not installed
    """
    cmd = build_gifsicle_command(input_path, output_path, config)

    try:
        print("Compressing GIF with gifsicle...")
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("Compression completed.")

        # Show compression statistics
        original_size = os.path.getsize(input_path) / (1024 * 1024)
        compressed_size = os.path.getsize(output_path) / (1024 * 1024)
        compression_ratio = (1 - compressed_size / original_size) * 100

        print(f"Original size: {original_size:.2f} MB")
        print(f"Compressed size: {compressed_size:.2f} MB")
        print(f"Compression ratio: {compression_ratio:.1f}% reduction")

    except subprocess.CalledProcessError as e:
        print(f"Compression failed: {e}")
        raise
    except FileNotFoundError:
        print("gifsicle not found. Please install gifsicle.")
        raise
