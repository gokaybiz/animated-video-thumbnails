#!/usr/bin/env python3
"""
Example usage patterns for animated video thumbnails.

This script demonstrates various ways to use the modular animated video
thumbnails package with different configurations and use cases.
"""

import os
from src.config.defaults import (
    create_default_config,
    create_fast_config,
    create_quality_config
)
from dataclasses import replace
from src.pipeline.main_pipeline import create_video_preview
from src.types.models import Config, ProcessingConfig, CompressionConfig


def example_basic_usage():
    """Demonstrate basic usage with default configuration."""
    print("=== Basic Usage Example ===")

    video_path = "test_files/Big Buck Bunny 1080p 60FPS.mp4"

    if not os.path.exists(video_path):
        print(f"⚠️  Video file not found: {video_path}")
        print("Please add a video file to test_files/ directory")
        return

    # Simple default configuration
    config = create_default_config(
        video_path=video_path,
        output_path="example_basic.gif",
        compressed_output_path="example_basic_compressed.gif"
    )

    print(f"Processing: {config.video_path}")
    print(f"Grid size: {config.cols}x{config.rows}")
    print(f"Output: {config.compressed_output_path}")

    try:
        create_video_preview(config)
        print("✓ Basic example completed successfully!")
    except Exception as e:
        print(f"❌ Error in basic example: {e}")


def example_fast_processing():
    """Demonstrate fast processing for quick previews."""
    print("\n=== Fast Processing Example ===")

    video_path = "test_files/Big Buck Bunny 1080p 60FPS.mp4"

    if not os.path.exists(video_path):
        print(f"⚠️  Video file not found: {video_path}")
        return

    # Fast configuration for quick feedback
    config = create_fast_config(
        video_path=video_path,
        output_path="example_fast.gif",
        compressed_output_path="example_fast_compressed.gif"
    )

    print("Fast processing configuration:")
    print(f"- Grid: {config.cols}x{config.rows}")
    print(f"- Clip duration: {config.clip_duration}s")
    print(f"- Interval: {config.interval}s")
    print(f"- Processing height: {config.processing.processing_height}px")
    print(f"- Final FPS: {config.fps}")

    try:
        create_video_preview(config)
        print("✅ Fast processing example completed!")
    except Exception as e:
        print(f"❌ Error in fast example: {e}")


def example_high_quality():
    """Demonstrate high-quality processing."""
    print("\n=== High Quality Example ===")

    video_path = "test_files/Big Buck Bunny 1080p 60FPS.mp4"

    if not os.path.exists(video_path):
        print(f"⚠️  Video file not found: {video_path}")
        return

    # Quality configuration for best results
    config = create_quality_config(
        video_path=video_path,
        output_path="example_quality.gif",
        compressed_output_path="example_quality_compressed.gif"
    )

    print("High quality configuration:")
    print(f"- Grid: {config.cols}x{config.rows}")
    print(f"- Clip duration: {config.clip_duration}s")
    print(f"- Processing height: {config.processing.processing_height}px")
    print(f"- Colors: {config.compression.max_colors}")
    print(f"- Lossy level: {config.compression.lossy_level}")

    try:
        create_video_preview(config)
        print("✓ High quality example completed!")
    except Exception as e:
        print(f"❌ Error in quality example: {e}")


def example_custom_configuration():
    """Demonstrate custom configuration creation."""
    print("\n=== Custom Configuration Example ===")

    video_path = "test_files/Big Buck Bunny 1080p 60FPS.mp4"

    if not os.path.exists(video_path):
        print(f"⚠️  Video file not found: {video_path}")
        return

    # Create completely custom configuration
    custom_processing = ProcessingConfig(
        max_workers=2,  # Limit to 2 workers
        processing_fps=8,  # Low processing fps
        processing_height=160,  # Small height
        enable_parallel=True
    )

    custom_compression = CompressionConfig(
        lossy_level=80,  # High compression
        optimization_level=3,  # Max optimization
        max_colors=64,  # Few colors
        careful_optimization=False  # Skip careful mode for speed
    )

    custom_config = Config(
        video_path=video_path,
        clip_duration=1,  # Very short clips
        interval=120,  # Large intervals
        fps=12,  # Low final fps
        cols=2,  # Small grid
        rows=2,
        output_path="example_custom.gif",
        compressed_output_path="example_custom_compressed.gif",
        compression=custom_compression,
        processing=custom_processing
    )

    print("Custom configuration:")
    print(f"- Tiny grid: {custom_config.cols}x{custom_config.rows}")
    print(f"- Short clips: {custom_config.clip_duration}s")
    print(f"- Large intervals: {custom_config.interval}s")
    print(f"- Limited workers: {custom_config.processing.max_workers}")
    print(f"- High compression: {custom_config.compression.lossy_level}")

    try:
        create_video_preview(custom_config)
        print("✓ Custom configuration example completed!")
    except Exception as e:
        print(f"❌ Error in custom example: {e}")


def example_functional_composition():
    """Demonstrate using individual components functionally."""
    print("\n=== Functional Composition Example ===")

    video_path = "test_files/Big Buck Bunny 1080p 60FPS.mp4"

    if not os.path.exists(video_path):
        print(f"⚠️  Video file not found: {video_path}")
        return

    # Import individual components
    from src.core.functions import generate_timestamps
    from src.io.video_io import load_video

    try:
        # Load video to get duration
        video = load_video(video_path)
        duration = video.duration
        video.close()

        # Generate timestamps functionally
        timestamps = generate_timestamps(
            video_duration=duration,
            clip_duration=3,
            interval=60,
            max_clips=9  # 3x3 grid
        )

        print(f"Generated {len(timestamps)} timestamps:")
        for i, ts in enumerate(timestamps[:5]):  # Show first 5
            print(f"  {i+1}. {ts.format()}")
        if len(timestamps) > 5:
            print(f"... and {len(timestamps) - 5} more")

        # Now create full config and process
        config = create_default_config(video_path)
        config = replace(config,
            cols=3, rows=3,  # Use 3x3 grid
            output_path="example_functional.gif",
            compressed_output_path="example_functional_compressed.gif"
        )

        create_video_preview(config)
        print("✅ Functional composition example completed!")

    except Exception as e:
        print(f"❌ Error in functional example: {e}")


def example_error_handling():
    """Demonstrate error handling and edge cases."""
    print("\n=== Error Handling Example ===")

    # Try with non-existent file
    try:
        config = create_default_config(
            video_path="non_existent_video.mp4",
            output_path="error_test.gif",
            compressed_output_path="error_test_compressed.gif"
        )
        create_video_preview(config)
    except FileNotFoundError:
        print("✅ Correctly handled missing video file")
    except Exception as e:
        print(f"⚠️  Unexpected error: {e}")

    # Try with invalid configuration
    try:
        from src.types.models import Config, ProcessingConfig, CompressionConfig

        invalid_config = Config(
            video_path="test_files/Big Buck Bunny 1080p 60FPS.mp4",
            clip_duration=0,  # Invalid duration
            interval=10,
            fps=30,
            cols=0,  # Invalid grid
            rows=0,
            output_path="invalid.gif",
            compressed_output_path="invalid_compressed.gif",
            compression=CompressionConfig(
                lossy_level=200,  # Very high compression
                optimization_level=3,
                max_colors=8,  # Very few colors
                careful_optimization=False
            ),
            processing=ProcessingConfig(
                max_workers=1,
                processing_fps=1,  # Very low fps
                processing_height=50,  # Very small
                enable_parallel=False
            )
        )

        if os.path.exists(invalid_config.video_path):
            create_video_preview(invalid_config)
            print("⚠️  Processed despite questionable configuration")
        else:
            print("⚠️  Cannot test invalid config - video file missing")

    except Exception as e:
        print(f"✅ Correctly handled invalid configuration: {e}")


def main():
    """Run all examples in sequence."""
    print("🎬 Animated Video Thumbnails - Examples")
    print("=" * 50)

    # Check if we have any video files
    test_dir = "test_files"
    if not os.path.exists(test_dir):
        print(f"⚠️  Test directory '{test_dir}' not found.")
        print("Creating test_files directory...")
        os.makedirs(test_dir, exist_ok=True)
        print("Please add video files to test_files/ to run examples.")
        return

    # Run examples
    example_basic_usage()
    example_fast_processing()
    example_high_quality()
    example_custom_configuration()
    example_functional_composition()
    example_error_handling()

    print("\n" + "=" * 50)
    print("🎉 All examples completed!")
    print("\nGenerated files:")
    for filename in [
        "example_basic_compressed.gif",
        "example_fast_compressed.gif",
        "example_quality_compressed.gif",
        "example_custom_compressed.gif",
        "example_functional_compressed.gif"
    ]:
        if os.path.exists(filename):
            size_mb = os.path.getsize(filename) / (1024 * 1024)
            print(f"  📄 {filename} ({size_mb:.2f} MB)")


if __name__ == "__main__":
    main()
