"""
Metadata extraction functions for video files using pymediainfo.

This module provides pure functions for extracting comprehensive metadata
from video files using the pymediainfo library, which provides accurate
and detailed media information. All functions follow functional programming principles.
"""

import os
import math
from typing import Optional, Dict, Any
from pymediainfo import MediaInfo

from ..types.models import FileMetadata, VideoMetadata, AudioMetadata, CompleteMetadata


def extract_file_metadata(file_path: str) -> FileMetadata:
    """
    Extract file-level metadata from video file.

    Args:
        file_path: Path to video file

    Returns:
        FileMetadata object with file information

    Raises:
        FileNotFoundError: If file doesn't exist
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Video file not found: {file_path}")

    file_size_bytes = os.path.getsize(file_path)
    filename = os.path.basename(file_path)

    return FileMetadata(
        filename=filename,
        file_size_bytes=file_size_bytes,
        file_size_human=format_file_size(file_size_bytes),
        full_path=os.path.abspath(file_path)
    )


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format.

    Args:
        size_bytes: File size in bytes

    Returns:
        Human-readable file size string (e.g., "333.37 MiB")
    """
    if size_bytes == 0:
        return "0 B"

    size_names = ["B", "KiB", "MiB", "GiB", "TiB"]
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    size = round(size_bytes / p, 2)

    return f"{size} {size_names[i]}"


def format_duration_ms(duration_ms: Optional[float]) -> str:
    """
    Format duration from milliseconds to HH:MM:SS format.

    Args:
        duration_ms: Duration in milliseconds

    Returns:
        Formatted duration string
    """
    if duration_ms is None:
        return "00:00:00"

    seconds = int(duration_ms / 1000)
    hours, remainder = divmod(seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def calculate_aspect_ratio(width: int, height: int) -> str:
    """
    Calculate aspect ratio string from dimensions.

    Args:
        width: Video width in pixels
        height: Video height in pixels

    Returns:
        Aspect ratio string (e.g., "16:9")
    """
    def gcd(a: int, b: int) -> int:
        while b:
            a, b = b, a % b
        return a

    if width == 0 or height == 0:
        return "Unknown"

    ratio_gcd = gcd(width, height)
    ratio_w = width // ratio_gcd
    ratio_h = height // ratio_gcd

    return f"{ratio_w}:{ratio_h}"


def extract_video_track_metadata(media_info: MediaInfo) -> VideoMetadata:
    """
    Extract video metadata from MediaInfo object.

    Args:
        media_info: MediaInfo object from pymediainfo

    Returns:
        VideoMetadata object with video properties
    """
    # Find video track
    video_track = None
    for track in media_info.tracks:
        if track.track_type == 'Video':
            video_track = track
            break

    if video_track is None:
        # Fallback values if no video track found
        return VideoMetadata(
            codec="Unknown",
            width=0,
            height=0,
            aspect_ratio="Unknown",
            fps=0.0,
            duration_seconds=0.0,
            duration_formatted="00:00:00"
        )

    # Extract video properties with safe conversions
    width = int(video_track.width or 0)
    height = int(video_track.height or 0)

    # Handle frame rate - can be a string like "25.000" or None
    fps = 0.0
    if video_track.frame_rate:
        try:
            fps = float(video_track.frame_rate)
        except (ValueError, TypeError):
            fps = 0.0

    # Handle duration
    duration_ms = float(video_track.duration or 0)
    duration_seconds = duration_ms / 1000 if duration_ms else 0.0

    # Get codec information with profile
    codec = video_track.format or "Unknown"
    format_profile = video_track.format_profile
    if format_profile and codec != "Unknown":
        codec = f"{codec} ({format_profile})"

    # Get bitrate (convert from bps to kbps)
    bitrate_kbps = None
    if video_track.bit_rate:
        try:
            bitrate_kbps = int(float(video_track.bit_rate) / 1000)
        except (ValueError, TypeError):
            bitrate_kbps = None

    return VideoMetadata(
        codec=codec,
        width=width,
        height=height,
        aspect_ratio=calculate_aspect_ratio(width, height),
        fps=fps,
        duration_seconds=duration_seconds,
        duration_formatted=format_duration_ms(duration_ms),
        bitrate_kbps=bitrate_kbps
    )


def get_general_track_info(media_info: MediaInfo) -> Dict[str, Any]:
    """
    Extract general track information for fallback data.

    Args:
        media_info: MediaInfo object from pymediainfo

    Returns:
        Dictionary with general track information
    """
    general_track = None
    for track in media_info.tracks:
        if track.track_type == 'General':
            general_track = track
            break

    if general_track is None:
        return {}

    info = {}

    # Duration from general track (sometimes more accurate)
    if general_track.duration:
        try:
            info['duration_ms'] = float(general_track.duration)
        except (ValueError, TypeError):
            pass

    # Overall bitrate
    if general_track.overall_bit_rate:
        try:
            info['overall_bitrate_kbps'] = int(float(general_track.overall_bit_rate) / 1000)
        except (ValueError, TypeError):
            pass

    # Format name
    if general_track.format:
        info['format_name'] = str(general_track.format)

    # Encoding library
    if general_track.encoded_library_name:
        info['encoding_library'] = str(general_track.encoded_library_name)

    return info


def extract_complete_metadata(file_path: str) -> CompleteMetadata:
    """
    Extract complete metadata from video file using pymediainfo.

    Args:
        file_path: Path to video file

    Returns:
        CompleteMetadata object with all video information

    Raises:
        FileNotFoundError: If file doesn't exist
        Exception: If video cannot be analyzed
    """
    # Extract file metadata
    file_metadata = extract_file_metadata(file_path)

    try:
        # Parse media file with pymediainfo
        media_info = MediaInfo.parse(file_path)

        if not media_info.tracks:
            raise Exception("No media tracks found in file")

        # Extract video metadata
        video_metadata = extract_video_track_metadata(media_info)

        # Extract audio metadata
        audio_metadata = extract_audio_metadata(media_info)

        # Get general track info for potential fallbacks
        general_info = get_general_track_info(media_info)

        # Use general track duration if video track duration is missing/zero
        if video_metadata.duration_seconds == 0.0 and 'duration_ms' in general_info:
            duration_ms = general_info['duration_ms']
            duration_seconds = duration_ms / 1000

            # Create updated video metadata with corrected duration
            video_metadata = VideoMetadata(
                codec=video_metadata.codec,
                width=video_metadata.width,
                height=video_metadata.height,
                aspect_ratio=video_metadata.aspect_ratio,
                fps=video_metadata.fps,
                duration_seconds=duration_seconds,
                duration_formatted=format_duration_ms(duration_ms),
                bitrate_kbps=video_metadata.bitrate_kbps or general_info.get('overall_bitrate_kbps')
            )

        return CompleteMetadata(
            file=file_metadata,
            video=video_metadata,
            audio=audio_metadata if audio_metadata.has_audio else None
        )

    except Exception as e:
        raise Exception(f"Failed to extract metadata from {file_path}: {e}")


def validate_media_file(file_path: str) -> bool:
    """
    Validate if a file can be analyzed by pymediainfo.

    Args:
        file_path: Path to media file

    Returns:
        True if file can be analyzed, False otherwise
    """
    try:
        if not os.path.exists(file_path):
            return False

        media_info = MediaInfo.parse(file_path)
        # Check if we have at least one track
        return len(media_info.tracks) > 0

    except Exception:
        return False


def extract_audio_metadata(media_info: MediaInfo) -> AudioMetadata:
    """
    Extract audio metadata from MediaInfo object.

    Args:
        media_info: MediaInfo object from pymediainfo

    Returns:
        AudioMetadata object with audio properties
    """
    audio_track = None
    for track in media_info.tracks:
        if track.track_type == 'Audio':
            audio_track = track
            break

    if audio_track is None:
        return AudioMetadata(
            codec="None",
            sample_rate_hz=0,
            channels="none",
            bitrate_kbps=None,
            has_audio=False
        )

    # Audio codec
    codec = str(audio_track.format or "Unknown")
    if audio_track.format_profile:
        codec = f"{codec} ({audio_track.format_profile})"

    # Channels
    channels = "unknown"
    if audio_track.channel_s:
        try:
            num_channels = int(audio_track.channel_s)
            if num_channels == 1:
                channels = "mono"
            elif num_channels == 2:
                channels = "stereo"
            elif num_channels == 6:
                channels = "5.1"
            elif num_channels == 8:
                channels = "7.1"
            else:
                channels = f"{num_channels} channels"
        except (ValueError, TypeError):
            channels = "unknown"
    elif audio_track.channel_layout:
        channels = str(audio_track.channel_layout).lower()

    # Sample rate
    sample_rate_hz = 0
    if audio_track.sampling_rate:
        try:
            sample_rate_hz = int(float(audio_track.sampling_rate))
        except (ValueError, TypeError):
            sample_rate_hz = 0

    # Bitrate
    bitrate_kbps = None
    if audio_track.bit_rate:
        try:
            bitrate_kbps = int(float(audio_track.bit_rate) / 1000)
        except (ValueError, TypeError):
            bitrate_kbps = None

    return AudioMetadata(
        codec=codec,
        sample_rate_hz=sample_rate_hz,
        channels=channels,
        bitrate_kbps=bitrate_kbps,
        has_audio=True
    )


def extract_audio_info(media_info: MediaInfo) -> Dict[str, Any]:
    """
    Extract basic audio information from MediaInfo object (legacy function).

    Args:
        media_info: MediaInfo object from pymediainfo

    Returns:
        Dictionary with audio information
    """
    audio_metadata = extract_audio_metadata(media_info)

    if not audio_metadata.has_audio:
        return {'has_audio': False}

    return {
        'has_audio': True,
        'codec': audio_metadata.codec,
        'channels': audio_metadata.channels,
        'sample_rate_hz': audio_metadata.sample_rate_hz,
        'bitrate_kbps': audio_metadata.bitrate_kbps
    }
