"""
Data models and type definitions for animated video thumbnails.

All models are immutable (frozen dataclasses) following functional programming principles.
They represent pure data structures without behavior.
"""

from dataclasses import dataclass
from typing import Optional
import math

@dataclass(frozen=True)
class ProcessingConfig:
    """Configuration for video processing parameters."""
    max_workers: Optional[int]
    processing_fps: int
    processing_height: int
    enable_parallel: bool


@dataclass(frozen=True)
class CompressionConfig:
    """Configuration for GIF compression settings."""
    lossy_level: int
    optimization_level: int
    max_colors: int
    careful_optimization: bool


@dataclass(frozen=True)
class Config:
    """Main application configuration containing all settings."""
    video_path: str
    clip_duration: int
    interval: int
    fps: int
    cols: int
    rows: int
    grid_padding: int
    output_path: str
    compressed_output_path: str
    compression: CompressionConfig
    processing: ProcessingConfig
    include_metadata: bool = False


@dataclass(frozen=True)
class TimeStamp:
    """Represents a timestamp in seconds with formatting capabilities."""
    seconds: int

    def format(self) -> str:
        """Format timestamp as HH:MM:SS string."""
        h, rem = divmod(self.seconds, 3600)
        m, s = divmod(rem, 60)
        return f"{h:02}:{m:02}:{s:02}"


@dataclass(frozen=True)
class ClipMetadata:
    """Metadata for a video clip segment."""
    start_time: TimeStamp
    duration: int
    height: int
    index: int


@dataclass(frozen=True)
class ClipTask:
    """Task definition for parallel clip processing."""
    metadata: ClipMetadata
    video_path: str
    processing_fps: int
    temp_output_path: str


@dataclass(frozen=True)
class VideoMetadata:
    """Metadata for video track information."""
    codec: str
    width: int
    height: int
    aspect_ratio: str
    fps: float
    duration_seconds: float
    duration_formatted: str
    bitrate_kbps: Optional[int] = None


@dataclass(frozen=True)
class FileMetadata:
    """Metadata for file information."""
    filename: str
    file_size_bytes: int
    file_size_human: str
    full_path: str


@dataclass(frozen=True)
class AudioMetadata:
    """Metadata for audio track information."""
    codec: str
    sample_rate_hz: int
    channels: str
    bitrate_kbps: Optional[int] = None
    has_audio: bool = True


@dataclass(frozen=True)
class CompleteMetadata:
    """Complete metadata combining all video information."""
    file: FileMetadata
    video: VideoMetadata
    audio: Optional[AudioMetadata] = None

    def format_display_text(self) -> str:
        """Format metadata for display as compact multi-line string."""
        lines = [
            f"File: {self.file.filename}",
            f"Size: {self.file.file_size_bytes}B ({self.file.file_size_human}), Duration: {self.video.duration_formatted}",
            f"Video: {self.video.codec}, {self.video.width}x{self.video.height} ({self.video.aspect_ratio}), {self.video.fps:.2f} fps" +
            (f", {self.video.bitrate_kbps}kb/s" if self.video.bitrate_kbps else ""),
        ]

        # Add audio line if audio metadata is available
        if self.audio and self.audio.has_audio:
            audio_line = f"Audio: {self.audio.codec}, {self.audio.sample_rate_hz}Hz, {self.audio.channels}"
            if self.audio.bitrate_kbps:
                audio_line += f", {self.audio.bitrate_kbps}kb/s"
            lines.append(audio_line)

        return "\n".join(lines)


def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format."""
    if size_bytes == 0:
        return "0 B"

    size_names = ["B", "KiB", "MiB", "GiB", "TiB"]
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    size = round(size_bytes / p, 2)

    return f"{size} {size_names[i]}"


def format_duration_seconds(duration_seconds: float) -> str:
    """Format duration from seconds to HH:MM:SS format."""
    seconds = int(duration_seconds)
    hours, remainder = divmod(seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def calculate_aspect_ratio(width: int, height: int) -> str:
    """Calculate aspect ratio string from dimensions."""
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


def extract_metadata_information(video_path: str) -> CompleteMetadata:
    """
    Extract metadata from video file using pymediainfo.

    Args:
        video_path: Path to video file

    Returns:
        CompleteMetadata object with comprehensive video information

    Raises:
        Exception: If metadata extraction fails
    """
    try:
        from ..metadata.extraction import extract_complete_metadata
        return extract_complete_metadata(video_path)
    except ImportError:
        raise Exception("pymediainfo is required for metadata extraction. Install with: pip install pymediainfo")
