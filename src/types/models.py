"""
Data models and type definitions for animated video thumbnails.

All models are immutable (frozen dataclasses) following functional programming principles.
They represent pure data structures without behavior.
"""

from dataclasses import dataclass
from typing import  Optional


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
