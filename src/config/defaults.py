"""
Default configuration factory functions for animated video thumbnails.

This module provides functions to create default configurations
following functional programming principles. All functions return
immutable configuration objects.
"""

from ..types.models import ProcessingConfig, CompressionConfig, Config


def create_default_processing_config() -> ProcessingConfig:
    """
    Create default processing configuration with performance optimizations.

    Returns:
        ProcessingConfig with optimized settings for parallel processing
    """
    return ProcessingConfig(
        max_workers=None,  # Auto-detect CPU cores
        processing_fps=10,
        processing_height=180,
        enable_parallel=True,
    )


def create_default_compression_config() -> CompressionConfig:
    """
    Create default compression configuration for optimal file size.

    Returns:
        CompressionConfig with balanced quality and compression settings
    """
    return CompressionConfig(
        lossy_level=70,
        optimization_level=3,
        max_colors=128,
        careful_optimization=True
    )


def create_default_config(
    video_path: str,
    output_path: str = "output.gif",
    compressed_output_path: str = "output_compressed.gif"
) -> Config:
    """
    Create default application configuration.

    Args:
        video_path: Path to source video file
        output_path: Path for initial GIF output (default: "output.gif")
        compressed_output_path: Path for compressed output (default: "output_compressed.gif")

    Returns:
        Complete Config object with default settings
    """
    return Config(
        video_path=video_path,
        clip_duration=2,  # 2 second clips
        interval=40,  # 40 second intervals
        fps=25,  # Final output fps
        cols=3,  # 3x5 grid layout
        rows=5,
        grid_padding=4,
        output_path=output_path,
        compressed_output_path=compressed_output_path,
        compression=create_default_compression_config(),
        processing=create_default_processing_config(),
        include_metadata=True
    )


def create_fast_config(
    video_path: str,
    output_path: str = "output_fast.gif",
    compressed_output_path: str = "output_fast_compressed.gif"
) -> Config:
    """
    Create configuration optimized for speed over quality.

    Args:
        video_path: Path to source video file
        output_path: Path for initial GIF output
        compressed_output_path: Path for compressed output

    Returns:
        Config object optimized for fast processing
    """
    fast_processing = ProcessingConfig(
        max_workers=None,
        processing_fps=10,
        processing_height=120,
        enable_parallel=True,
    )

    fast_compression = CompressionConfig(
        lossy_level=80,
        optimization_level=3,
        max_colors=128,
        careful_optimization=False
    )

    return Config(
        video_path=video_path,
        clip_duration=2,
        interval=40,
        fps=20,
        cols=3,
        rows=5,
        grid_padding=4,
        output_path=output_path,
        compressed_output_path=compressed_output_path,
        compression=fast_compression,
        processing=fast_processing,
        include_metadata=True
    )


def create_quality_config(
    video_path: str,
    output_path: str = "output_quality.gif",
    compressed_output_path: str = "output_quality_compressed.gif"
) -> Config:
    """
    Create configuration optimized for quality over speed.

    Args:
        video_path: Path to source video file
        output_path: Path for initial GIF output
        compressed_output_path: Path for compressed output

    Returns:
        Config object optimized for high quality output
    """
    quality_processing = ProcessingConfig(
        max_workers=None,
        processing_fps=15,  # Higher processing fps
        processing_height=240,  # Higher resolution
        enable_parallel=True,
    )

    quality_compression = CompressionConfig(
        lossy_level=50,  # Lower lossy compression
        optimization_level=3,  # Maximum optimization
        max_colors=256,  # More colors
        careful_optimization=True  # Enable careful optimization
    )

    return Config(
        video_path=video_path,
        clip_duration=3,
        interval=30,
        fps=30,
        cols=4,
        rows=6,
        grid_padding=5,
        output_path=output_path,
        compressed_output_path=compressed_output_path,
        compression=quality_compression,
        processing=quality_processing,
        include_metadata=True
    )
