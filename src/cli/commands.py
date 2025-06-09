"""
CLI command handlers for animated video thumbnails.

This module contains the main command handlers that implement the CLI functionality.
Each command is a pure function that takes parsed arguments and executes the
corresponding operation using the core application modules.
"""

import os
import time
import glob
from pathlib import Path
from dataclasses import replace

from ..pipeline.main_pipeline import create_video_preview
from ..config.defaults import (
    create_default_config,
    create_fast_config,
    create_quality_config
)
from .parser import args_to_config, get_default_output_path
from .utils import (
    print_config_summary,
    format_duration,
    format_file_size,
    validate_video_file,
)


def cmd_generate(args) -> int:
    """
    Handle the generate command for creating animated thumbnails.

    Args:
        args: Parsed command-line arguments

    Returns:
        Exit code (0 for success, 1 for error)
    """
    try:
        # Convert CLI args to config
        config = args_to_config(args)

        # Set output path if not specified
        if not args.output:
            output_base = get_default_output_path(args.input)
            config = replace(config,
                output_path=output_base,
                compressed_output_path=output_base.replace('.gif', '_compressed.gif')
            )

        # Handle no-compress option
        if getattr(args, 'no_compress', False):
            config = replace(config, compressed_output_path=config.output_path)

        # Print configuration summary if verbose
        if getattr(args, 'verbose', False):
            print_config_summary(config)

        # Dry run mode
        if getattr(args, 'dry_run', False):
            print("🔍 Dry run mode - showing what would be done:")
            print_config_summary(config)
            print("\n✅ Dry run completed. Use without --dry-run to actually process.")
            return 0

        # Execute the pipeline
        print(f"🎬 Generating animated thumbnail from: {config.video_path}")
        start_time = time.time()

        create_video_preview(config)

        elapsed = time.time() - start_time
        print(f"\n✅ Success! Generated in {format_duration(elapsed)}")

        # Show output file info
        output_file = config.compressed_output_path
        if os.path.exists(output_file):
            size = format_file_size(os.path.getsize(output_file))
            print(f"📄 Output: {output_file} ({size})")

        return 0

    except KeyboardInterrupt:
        print("\n🛑 Operation cancelled by user")
        return 1
    except FileNotFoundError as e:
        print(f"❌ File not found: {e}")
        return 1
    except Exception as e:
        print(f"❌ Error: {e}")
        if getattr(args, 'verbose', False):
            import traceback
            traceback.print_exc()
        return 1


def cmd_preview(args) -> int:
    """
    Handle the preview command for quick thumbnail generation.

    Args:
        args: Parsed command-line arguments

    Returns:
        Exit code (0 for success, 1 for error)
    """
    try:
        # Create fast config for preview
        config = create_fast_config(args.input)

        # Set custom grid if specified
        if hasattr(args, 'grid') and args.grid:
            from .parser import _parse_grid
            cols, rows = _parse_grid(args.grid)
            config = replace(config, cols=cols, rows=rows)

        # Set output path
        if args.output:
            output_path = args.output
        else:
            output_path = get_default_output_path(args.input, "_preview")

        config = replace(config,
            output_path=output_path,
            compressed_output_path=output_path.replace('.gif', '_compressed.gif')
        )

        # Further optimize for speed
        config = replace(config,
            clip_duration=1,  # Very short clips
            interval=60,      # Large intervals
            fps=10            # Low fps
        )

        print(f"🚀 Generating quick preview from: {config.video_path}")
        print(f"📐 Grid: {config.cols}x{config.rows}")

        start_time = time.time()
        create_video_preview(config)
        elapsed = time.time() - start_time

        print(f"\n✅ Preview generated in {format_duration(elapsed)}")

        if os.path.exists(output_path):
            size = format_file_size(os.path.getsize(output_path))
            print(f"📄 Preview: {output_path} ({size})")

        return 0

    except KeyboardInterrupt:
        print("\n🛑 Operation cancelled by user")
        return 1
    except Exception as e:
        print(f"❌ Error generating preview: {e}")
        if getattr(args, 'verbose', False):
            import traceback
            traceback.print_exc()
        return 1


def cmd_batch(args) -> int:
    """
    Handle the batch command for processing multiple videos.

    Args:
        args: Parsed command-line arguments

    Returns:
        Exit code (0 for success, 1 for error)
    """
    try:
        # Expand glob patterns
        input_files = []
        for pattern in args.inputs:
            if '*' in pattern or '?' in pattern:
                matches = glob.glob(pattern)
                input_files.extend(matches)
            else:
                input_files.append(pattern)

        # Remove duplicates and sort
        input_files = sorted(set(input_files))

        # Filter for valid video files
        valid_files = []
        for file_path in input_files:
            if os.path.exists(file_path) and validate_video_file(file_path):
                valid_files.append(file_path)
            else:
                print(f"⚠️  Skipping invalid file: {file_path}")

        if not valid_files:
            print("❌ No valid video files found")
            return 1

        print(f"🎬 Processing {len(valid_files)} video files...")

        # Get preset config
        preset = getattr(args, 'preset', 'fast')
        config_func = {
            'fast': create_fast_config,
            'quality': create_quality_config,
            'default': create_default_config
        }.get(preset, create_fast_config)

        successful = 0
        failed = 0
        start_time = time.time()

        for i, input_file in enumerate(valid_files, 1):
            print(f"\n📹 [{i}/{len(valid_files)}] Processing: {os.path.basename(input_file)}")

            try:
                # Create config for this file
                config = config_func(input_file)

                # Set output path
                output_dir = getattr(args, 'output_dir', None)
                suffix = getattr(args, 'suffix', '_thumb')

                if output_dir:
                    output_path = os.path.join(
                        output_dir,
                        Path(input_file).stem + suffix + '.gif'
                    )
                else:
                    output_path = get_default_output_path(input_file, suffix)

                config = replace(config,
                    output_path=output_path,
                    compressed_output_path=output_path.replace('.gif', '_compressed.gif')
                )

                # Process the video
                create_video_preview(config)

                if os.path.exists(output_path):
                    size = format_file_size(os.path.getsize(output_path))
                    print(f"   ✅ Generated: {os.path.basename(output_path)} ({size})")
                    successful += 1
                else:
                    print("   ❌ Failed to create output file")
                    failed += 1

            except Exception as e:
                print(f"   ❌ Error: {e}")
                failed += 1

                if not getattr(args, 'continue_on_error', False):
                    print("🛑 Stopping batch processing due to error")
                    break

        elapsed = time.time() - start_time
        print(f"\n📊 Batch processing completed in {format_duration(elapsed)}")
        print(f"✅ Successful: {successful}")
        print(f"❌ Failed: {failed}")

        return 0 if failed == 0 else 1

    except KeyboardInterrupt:
        print("\n🛑 Batch processing cancelled by user")
        return 1
    except Exception as e:
        print(f"❌ Batch processing error: {e}")
        if getattr(args, 'verbose', False):
            import traceback
            traceback.print_exc()
        return 1


def cmd_info(args) -> int:
    """
    Handle the info command for showing video information.

    Args:
        args: Parsed command-line arguments

    Returns:
        Exit code (0 for success, 1 for error)
    """
    try:
        from ..io.video_io import load_video

        input_file = args.input

        if not os.path.exists(input_file):
            print(f"❌ File not found: {input_file}")
            return 1

        if not validate_video_file(input_file):
            print(f"❌ File does not appear to be a video: {input_file}")
            return 1

        print(f"📹 Video Information: {os.path.basename(input_file)}")
        print("=" * 50)

        # Load video and get info
        video = load_video(input_file)

        duration = video.duration
        fps = video.fps
        size = video.size

        video.close()

        # File information
        file_size = os.path.getsize(input_file)
        print(f"📄 File size: {format_file_size(file_size)}")
        print(f"⏱️  Duration: {format_duration(duration)}")
        print(f"🎞️  FPS: {fps:.2f}")
        print(f"📐 Resolution: {size[0]}x{size[1]}")

        # Calculate approximate clips for different intervals
        print("\n📊 Potential clips (2s duration):")
        for interval in [30, 60, 120]:
            num_clips = max(1, int(duration // interval))
            print(f"   Interval {interval}s: ~{num_clips} clips")

        # Suggest configuration if requested
        if getattr(args, 'suggest_config', False):
            print("\n💡 Suggested configurations:")

            # Quick preview
            quick_clips = min(6, max(1, int(duration // 120)))
            cols = 2 if quick_clips <= 4 else 3
            rows = (quick_clips + cols - 1) // cols
            print(f"   Quick preview: {cols}x{rows} grid, 120s intervals")

            # Detailed view
            detail_clips = min(15, max(6, int(duration // 60)))
            cols = 3 if detail_clips <= 9 else 4
            rows = (detail_clips + cols - 1) // cols
            print(f"   Detailed view: {cols}x{rows} grid, 60s intervals")

            # Comprehensive
            comp_clips = min(24, max(12, int(duration // 30)))
            cols = 4 if comp_clips <= 16 else 5
            rows = (comp_clips + cols - 1) // cols
            print(f"   Comprehensive: {cols}x{rows} grid, 30s intervals")

        return 0

    except Exception as e:
        print(f"❌ Error getting video info: {e}")
        if getattr(args, 'verbose', False):
            import traceback
            traceback.print_exc()
        return 1


def cmd_help(args) -> int:
    """
    Handle the help command or show general help.

    Args:
        args: Parsed command-line arguments

    Returns:
        Exit code (always 0)
    """
    from .parser import create_cli_parser

    parser = create_cli_parser()
    parser.print_help()
    return 0


def execute_command(args) -> int:
    """
    Execute the appropriate command based on parsed arguments.

    Args:
        args: Parsed command-line arguments

    Returns:
        Exit code from command execution
    """
    command_map = {
        'generate': cmd_generate,
        'preview': cmd_preview,
        'batch': cmd_batch,
        'info': cmd_info,
        'help': cmd_help,
    }

    command = getattr(args, 'command', 'help')

    if command not in command_map:
        print(f"❌ Unknown command: {command}")
        return 1

    return command_map[command](args)
