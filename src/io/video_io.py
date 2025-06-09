"""
Video IO operations for animated video thumbnails.

This module handles video loading and clip creation with both sequential
and parallel processing capabilities. All functions in this module have
side effects (file I/O, process creation).
"""

import os
import tempfile
import time
import multiprocessing
from typing import List
from concurrent.futures import ProcessPoolExecutor, as_completed, wait
from moviepy import VideoFileClip
from PIL import ImageFont

from ..types.models import ClipMetadata, ClipTask, Config
from ..core.functions import create_temp_filename
from ..core.processing import process_single_clip, create_annotation_function


def load_video(path: str) -> VideoFileClip:
    """
    Load video file (IO operation).

    Args:
        path: Path to video file

    Returns:
        VideoFileClip object
    """
    return VideoFileClip(path)


def create_clips_parallel(video_path: str, metadatas: List[ClipMetadata],
                         config: Config) -> List[VideoFileClip]:
    """
    Create clips using parallel processing with temporary files.

    Args:
        video_path: Path to source video file
        metadatas: List of clip metadata for processing
        config: Application configuration

    Returns:
        List of processed VideoFileClip objects
    """
    if not config.processing.enable_parallel or len(metadatas) < 2:
        return create_clips_sequential(video_path, metadatas, config)

    max_workers = config.processing.max_workers or min(multiprocessing.cpu_count(), len(metadatas))

    print(f"Processing {len(metadatas)} clips using {max_workers} workers...")

    # Create temporary directory
    temp_dir = tempfile.mkdtemp(prefix="video_preview_")
    temp_files = []

    try:
        # Create tasks for each clip
        tasks = []
        for metadata in metadatas:
            temp_path = create_temp_filename(temp_dir, metadata.index)
            temp_files.append(temp_path)
            task = ClipTask(
                metadata=metadata,
                video_path=video_path,
                processing_fps=config.processing.processing_fps,
                temp_output_path=temp_path
            )
            tasks.append(task)

        # Process clips in parallel
        start_time = time.time()
        completed_files = []

        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            future_to_task = {
                executor.submit(process_single_clip, task): task
                for task in tasks
            }

            for future in as_completed(future_to_task):
                task = future_to_task[future]
                try:
                    result_path = future.result()
                    completed_files.append(result_path)

                    elapsed = time.time() - start_time
                    progress = (len(completed_files) / len(tasks)) * 100
                    print(f"Progress: {progress:.1f}% ({len(completed_files)}/{len(tasks)}) - {elapsed:.1f}s elapsed")

                except Exception as e:
                    print(f"Task {task.metadata.index} failed: {e}")
                    completed_files.append(task.temp_output_path)  # Include even if failed

            wait(future_to_task) # Ensure all tasks are completed

        # Load temporary files back as VideoFileClip objects
        print("Loading processed clips...")
        clips = []
        for temp_path in sorted(completed_files):
            if os.path.exists(temp_path):
                try:
                    clip = VideoFileClip(temp_path)
                    clips.append(clip)
                except Exception as e:
                    print(f"Failed to load {temp_path}: {e}")
                    clips.append(None)
            else:
                clips.append(None)

        # Filter out None values
        valid_clips = [clip for clip in clips if clip is not None]
        print(f"Successfully loaded {len(valid_clips)}/{len(metadatas)} clips")

        return valid_clips

    finally:
        # Clean up temporary files
        for temp_path in temp_files:
            if os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except (OSError, FileNotFoundError) as _:
                    # Ignore cleanup errors - file may already be removed
                    pass

        # Remove temporary directory
        try:
            os.rmdir(temp_dir)
        except (OSError, FileNotFoundError) as _:
            # Ignore cleanup errors - directory may not be empty or already removed
            pass


def create_clips_sequential(video_path: str, metadatas: List[ClipMetadata],
                           config: Config) -> List[VideoFileClip]:
    """
    Create clips sequentially (fallback).

    Args:
        video_path: Path to source video file
        metadatas: List of clip metadata for processing
        config: Application configuration

    Returns:
        List of processed VideoFileClip objects
    """
    print(f"Processing {len(metadatas)} clips sequentially...")

    video = load_video(video_path)
    font = ImageFont.load_default()
    clips = []

    start_time = time.time()
    for i, metadata in enumerate(metadatas):
        # Create base clip
        base_clip = video.subclipped(
            metadata.start_time.seconds,
            metadata.start_time.seconds + metadata.duration
        ).resized(height=metadata.height).with_fps(config.processing.processing_fps)

        # Create annotation function without lambda
        def annotate_frame_with_time(get_frame, t, start_time=metadata.start_time):
            frame = get_frame(t)
            from ..types.models import TimeStamp
            current_time = TimeStamp(int(start_time.seconds + t))
            return create_annotation_function(frame, current_time.format(), font)

        annotated_clip = base_clip.transform(annotate_frame_with_time)
        clips.append(annotated_clip)

        # Progress reporting
        if (i + 1) % 5 == 0 or i == len(metadatas) - 1:
            elapsed = time.time() - start_time
            progress = ((i + 1) / len(metadatas)) * 100
            print(f"Progress: {progress:.1f}% ({i + 1}/{len(metadatas)}) - {elapsed:.1f}s elapsed")

    video.close()
    return clips
