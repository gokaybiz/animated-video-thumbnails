"""
Processing functions for parallel video clip creation.

This module contains functions designed for multiprocessing,
including frame annotation and clip processing tasks.
"""

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy import VideoFileClip

from ..types.models import TimeStamp, ClipTask


def create_annotation_function(frame: np.ndarray, current_time_str: str, font: ImageFont.ImageFont) -> np.ndarray:
    """
    Named function for frame annotation (can be pickled for multiprocessing).

    Args:
        frame: Video frame as numpy array
        current_time_str: Formatted time string to display
        font: Font object for text rendering

    Returns:
        Annotated frame with timestamp overlay
    """
    annotated_frame = frame.copy()
    img = Image.fromarray(annotated_frame)
    draw = ImageDraw.Draw(img)

    # Draw timestamp background and text
    text_y = img.height - 25
    draw.rectangle([(5, text_y - 7), (65, img.height - 5)], fill=(0, 0, 0))
    draw.text((12, text_y), current_time_str, font=font, fill=(255, 255, 255))

    return np.array(img)


def process_single_clip(task: ClipTask) -> str:
    """
    Process a single clip and save as temporary file - designed for multiprocessing.

    Args:
        task: ClipTask containing all necessary processing information

    Returns:
        Path to the created temporary file
    """
    try:
        # Load video in this process
        video = VideoFileClip(task.video_path)
        font = ImageFont.load_default()

        # Create base clip
        base_clip = video.subclipped(
            task.metadata.start_time.seconds,
            task.metadata.start_time.seconds + task.metadata.duration
        ).resized(height=task.metadata.height).with_fps(task.processing_fps)

        # Create annotated clip using a custom function that avoids lambda
        def annotate_frame_with_time(get_frame, t):
            frame = get_frame(t)
            current_time = TimeStamp(int(task.metadata.start_time.seconds + t))
            return create_annotation_function(frame, current_time.format(), font)

        # Apply annotation without lambda
        annotated_clip = base_clip.transform(annotate_frame_with_time)

        # Export to temporary file
        annotated_clip.write_gif(task.temp_output_path, fps=task.processing_fps)

        # Clean up
        annotated_clip.close()
        base_clip.close()
        video.close()

        return task.temp_output_path

    except Exception as e:
        print(f"Error processing clip {task.metadata.index}: {e}")
        # Create a minimal black GIF as fallback
        try:
            video = VideoFileClip(task.video_path)
            black_clip = video.subclipped(0, task.metadata.duration).resized(
                height=task.metadata.height
            ).with_opacity(0.1)
            black_clip.write_gif(task.temp_output_path, fps=task.processing_fps)
            black_clip.close()
            video.close()
        except (OSError, IOError, Exception) as fallback_error:
            # If fallback clip creation also fails, we'll return the temp path anyway
            # This ensures the parallel processing doesn't hang
            print(f"Warning: Fallback clip creation also failed for clip {task.metadata.index}: {fallback_error}")
            pass
        return task.temp_output_path
