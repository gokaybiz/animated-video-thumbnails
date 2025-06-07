#!/usr/bin/env python3
"""
CLI Demo Script for Animated Video Thumbnails

This script demonstrates all the CLI functionality available in the
animated video thumbnails application. It shows various commands,
options, and use cases.

Run this script to see examples of all CLI features.
"""

import os
import subprocess
import sys
from pathlib import Path


def run_command(cmd: str, description: str = "") -> None:
    """Run a CLI command and display the output."""
    print(f"\n{'=' * 60}")
    if description:
        print(f"🎯 {description}")
    print(f"📝 Command: {cmd}")
    print("-" * 60)

    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, cwd="."
        )

        if result.stdout:
            print(result.stdout)

        if result.stderr:
            print(f"⚠️  Error output: {result.stderr}")

        if result.returncode != 0:
            print(f"❌ Command failed with exit code: {result.returncode}")
        else:
            print("✅ Command completed successfully")

    except Exception as e:
        print(f"❌ Failed to run command: {e}")


def main():
    """Demonstrate all CLI functionality."""

    print("🎬 Animated Video Thumbnails - CLI Demo")
    print("=" * 60)
    print("This demo shows all available CLI commands and options.")

    # Check if video file exists
    video_file = "test_files/Big Buck Bunny 1080p 60FPS.mp4"
    if not os.path.exists(video_file):
        print(f"\n❌ Demo video file not found: {video_file}")
        print("Please ensure you have a video file in the test_files directory.")
        return

    print(f"\n📹 Using demo video: {video_file}")

    # 1. Show general help
    run_command(
        "python cli.py --help",
        "General CLI help - shows all available commands"
    )

    # 2. Show version information
    run_command(
        "python cli.py generate --help",
        "Detailed help for the generate command"
    )

    # 3. Get video information
    run_command(
        f'python cli.py info "{video_file}"',
        "Display basic video information"
    )

    # 4. Get video info with configuration suggestions
    run_command(
        f'python cli.py info "{video_file}" --suggest-config',
        "Display video info with suggested configurations"
    )

    # 5. Dry run with default settings
    run_command(
        f'python cli.py generate "{video_file}" --dry-run',
        "Dry run with default settings (shows what would be done)"
    )

    # 6. Dry run with fast preset
    run_command(
        f'python cli.py generate "{video_file}" --preset fast --dry-run',
        "Dry run with fast preset"
    )

    # 7. Dry run with custom grid
    run_command(
        f'python cli.py generate "{video_file}" --grid 2x3 --dry-run',
        "Dry run with custom 2x3 grid layout"
    )

    # 8. Dry run with custom parameters
    run_command(
        f'python cli.py generate "{video_file}" --clip-duration 1 --interval 30 --fps 15 --dry-run',
        "Dry run with custom timing parameters"
    )

    # 9. Dry run with processing options
    run_command(
        f'python cli.py generate "{video_file}" --workers 2 --height 150 --processing-fps 8 --dry-run',
        "Dry run with custom processing options"
    )

    # 10. Dry run with compression options
    run_command(
        f'python cli.py generate "{video_file}" --lossy 90 --colors 64 --optimization 2 --dry-run',
        "Dry run with custom compression settings"
    )

    # 11. Generate a quick preview (actually runs)
    run_command(
        f'python cli.py preview "{video_file}" --grid 2x2',
        "Generate quick 2x2 preview (ACTUAL PROCESSING)"
    )

    # 12. Show batch command help
    run_command(
        "python cli.py batch --help",
        "Help for batch processing multiple videos"
    )

    # 13. Dry run batch processing
    run_command(
        f'python cli.py batch "{video_file}" --preset fast --suffix "_demo" --dry-run',
        "Dry run batch processing with custom suffix"
    )

    # 14. Show preview command help
    run_command(
        "python cli.py preview --help",
        "Help for preview command"
    )

    # 15. Show info command help
    run_command(
        "python cli.py info --help",
        "Help for info command"
    )

    print(f"\n{'=' * 60}")
    print("🎉 CLI Demo Complete!")
    print("=" * 60)

    print("\n📋 Summary of CLI Features Demonstrated:")
    print("✅ General help and command-specific help")
    print("✅ Video information display")
    print("✅ Configuration suggestions")
    print("✅ Dry run mode (shows what would be done)")
    print("✅ Multiple presets (default, fast, quality)")
    print("✅ Custom grid layouts")
    print("✅ Custom timing parameters")
    print("✅ Custom processing options")
    print("✅ Custom compression settings")
    print("✅ Quick preview generation")
    print("✅ Batch processing options")

    print("\n💡 Key CLI Commands:")
    print("🔹 python cli.py generate video.mp4              # Basic generation")
    print("🔹 python cli.py generate video.mp4 --preset fast # Fast preset")
    print("🔹 python cli.py preview video.mp4               # Quick preview")
    print("🔹 python cli.py batch *.mp4                     # Batch processing")
    print("🔹 python cli.py info video.mp4                  # Video information")
    print("🔹 python cli.py COMMAND --help                  # Command help")

    print("\n🎯 Next Steps:")
    print("1. Try generating thumbnails with different presets")
    print("2. Experiment with custom grid layouts and timing")
    print("3. Use batch processing for multiple videos")
    print("4. Check generated files for quality and size")

    # List any generated files
    print("\n📄 Generated Files:")
    for file_path in Path(".").glob("*.gif"):
        if file_path.exists():
            size_mb = file_path.stat().st_size / (1024 * 1024)
            print(f"   📄 {file_path.name} ({size_mb:.2f} MB)")

    for file_path in Path("test_files").glob("*.gif"):
        if file_path.exists():
            size_mb = file_path.stat().st_size / (1024 * 1024)
            print(f"   📄 {file_path} ({size_mb:.2f} MB)")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Demo interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        sys.exit(1)
