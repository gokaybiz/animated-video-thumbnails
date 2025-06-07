# Animated Video Thumbnails

A functional programming approach to creating animated GIF thumbnails from video files. This project demonstrates clean architecture principles with immutable data structures, pure functions, and clear separation of concerns.

## Features

- 🚀 **Parallel Processing**: Multi-core video processing for faster thumbnail generation
- 🎯 **Functional Programming**: Pure functions, immutable data structures, and composable operations
- ⚙️ **Configurable Quality**: Multiple preset configurations for different use cases
- 🗜️ **Advanced Compression**: Lossy compression with gifsicle for optimal file sizes
- 📦 **Modular Architecture**: Clean separation of concerns across focused modules
- 🔧 **Type Safety**: Comprehensive type hints and immutable dataclasses

## Project Structure

```
animated-video-thumbnails/
├── src/                          # Main package source code
│   ├── __init__.py              # Package exports and public API
│   ├── types/                   # Immutable data models
│   │   ├── __init__.py
│   │   └── models.py            # All dataclasses and type definitions
│   ├── core/                    # Pure business logic
│   │   ├── __init__.py
│   │   ├── functions.py         # Deterministic utility functions
│   │   └── processing.py        # Parallel processing functions
│   ├── io/                      # Side effect operations
│   │   ├── __init__.py
│   │   ├── video_io.py         # Video loading and clip creation
│   │   └── gif_io.py           # GIF export and compression
│   ├── pipeline/                # Main orchestration
│   │   ├── __init__.py
│   │   └── main_pipeline.py    # Complete processing pipeline
│   ├── config/                  # Configuration management
│   │   ├── __init__.py
│   │   └── defaults.py         # Configuration factory functions
│   └── cli/                     # Command-line interface
│       ├── __init__.py
│       ├── parser.py           # CLI argument parsing
│       ├── commands.py         # Command handlers
│       └── utils.py            # CLI utilities
├── main.py                      # Entry point with examples
├── cli.py                       # Command-line interface entry point
├── example.py                   # Usage examples
├── cli_demo.py                  # CLI demonstration script
├── test_files/                  # Sample video files
└── README.md                    # This file
```

## Architecture Principles

### Module Organization
- **types/**: Data definitions
- **core/**: Business logic and algorithms
- **io/**: File I/O, external processes
- **pipeline/**: Orchestration and workflow
- **config/**: Configuration and presets

## Quick Start

### Prerequisites

```bash
# Install uv (modern Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install Python dependencies
uv sync

# Install gifsicle for compression
sudo apt-get install gifsicle  # Ubuntu/Debian
brew install gifsicle          # macOS
```

### Basic Usage

#### Command Line Interface (Recommended)

```bash
# Basic thumbnail generation
python cli.py generate video.mp4

# Quick preview (fast processing)
python cli.py preview video.mp4

# Get video information
python cli.py info video.mp4

# Batch process multiple videos
python cli.py batch *.mp4

# Use different presets
python cli.py generate video.mp4 --preset fast
python cli.py generate video.mp4 --preset quality

# Custom settings
python cli.py generate video.mp4 --grid 4x3 --fps 30 --lossy 60
```

#### Python API

```python
from src.config.defaults import create_default_config
from src.pipeline.main_pipeline import create_video_preview

# Create configuration
config = create_default_config(
    video_path="path/to/your/video.mp4",
    output_path="thumbnail.gif",
    compressed_output_path="thumbnail_compressed.gif"
)

# Generate animated thumbnail
create_video_preview(config)
```

### Configuration Options

#### Default Configuration (Balanced)
```python
config = create_default_config("video.mp4")
# 3x5 grid, 2s clips, 40s intervals, 25fps output
```

#### Fast Processing (Speed over Quality)
```python
config = create_fast_config("video.mp4")
# 2x3 grid, 1s clips, 60s intervals, 15fps output
# Lower resolution, aggressive compression
```

#### High Quality (Quality over Speed)
```python
config = create_quality_config("video.mp4")
# 4x6 grid, 3s clips, 30s intervals, 30fps output
# Higher resolution, minimal compression
```

## Configuration Reference

### ProcessingConfig
```python
@dataclass(frozen=True)
class ProcessingConfig:
    max_workers: Optional[int]        # CPU cores to use (None = auto-detect)
    processing_fps: int               # FPS during processing (lower = faster)
    processing_height: int            # Height in pixels during processing
    enable_parallel: bool             # Enable parallel processing
```

### CompressionConfig
```python
@dataclass(frozen=True)
class CompressionConfig:
    lossy_level: int                  # Lossy compression level (0-200)
    optimization_level: int           # Optimization level (1-3)
    max_colors: int                   # Maximum colors in palette
    careful_optimization: bool        # Enable careful optimization
```

### Main Config
```python
@dataclass(frozen=True)
class Config:
    video_path: str                   # Input video file path
    clip_duration: int                # Duration of each clip in seconds
    interval: int                     # Interval between clips in seconds
    fps: int                          # Final output FPS
    cols: int                         # Grid columns
    rows: int                         # Grid rows
    output_path: str                  # Initial GIF output path
    compressed_output_path: str       # Final compressed output path
    compression: CompressionConfig    # Compression settings
    processing: ProcessingConfig      # Processing settings
```

## Advanced Usage

### Custom Configuration
```python
from src.types.models import Config, ProcessingConfig, CompressionConfig

# Create custom configuration
custom_config = Config(
    video_path="my_video.mp4",
    clip_duration=3,
    interval=45,
    fps=20,
    cols=4,
    rows=4,
    output_path="custom.gif",
    compressed_output_path="custom_compressed.gif",
    compression=CompressionConfig(
        lossy_level=60,
        optimization_level=3,
        max_colors=256,
        careful_optimization=True
    ),
    processing=ProcessingConfig(
        max_workers=4,
        processing_fps=12,
        processing_height=200,
        enable_parallel=True
    )
)

create_video_preview(custom_config)
```

### Using Individual Components
```python
from src.core.functions import generate_timestamps
from src.io.video_io import load_video
from src.types.models import TimeStamp

# Load video and generate timestamps
video = load_video("video.mp4")
timestamps = generate_timestamps(
    video_duration=video.duration,
    clip_duration=2,
    interval=30,
    max_clips=15
)
video.close()

# Work with timestamps
for ts in timestamps:
    print(f"Clip at: {ts.format()}")
```

## Command Line Interface

The CLI provides a user-friendly interface for all functionality:

### Available Commands

#### Generate Command
Create animated thumbnails with full customization:

```bash
python cli.py generate video.mp4 [OPTIONS]

Options:
  -o, --output PATH          Output file path
  --preset {default,fast,quality}  Configuration preset
  --grid COLSxROWS          Grid layout (e.g., 3x5, 4x3)
  --clip-duration SECONDS   Duration of each clip
  --interval SECONDS        Interval between clips
  --fps FPS                 Final output frames per second
  --workers N               Number of parallel workers
  --no-parallel             Disable parallel processing
  --height PIXELS           Processing height
  --lossy LEVEL             Compression level (0-200)
  --colors N                Maximum colors (2-256)
  --dry-run                 Show what would be done
```

#### Preview Command
Generate quick previews for fast feedback:

```bash
python cli.py preview video.mp4 [OPTIONS]

Options:
  -o, --output PATH         Output preview file
  --grid COLSxROWS         Preview grid layout (default: 2x2)
```

#### Batch Command
Process multiple videos with the same settings:

```bash
python cli.py batch video1.mp4 video2.mp4 *.mp4 [OPTIONS]

Options:
  --preset {default,fast,quality}  Configuration preset
  --output-dir DIR         Output directory
  --suffix SUFFIX          File suffix (default: _thumb)
  --continue-on-error      Continue if one file fails
  --dry-run               Show what would be done
```

#### Info Command
Display video information and suggestions:

```bash
python cli.py info video.mp4 [OPTIONS]

Options:
  --suggest-config         Show suggested configurations
```

### CLI Examples

```bash
# Get help for any command
python cli.py generate --help
python cli.py batch --help

# Basic generation with different presets
python cli.py generate video.mp4                    # Default preset
python cli.py generate video.mp4 --preset fast      # Fast processing
python cli.py generate video.mp4 --preset quality   # High quality

# Custom grid layouts
python cli.py generate video.mp4 --grid 2x3         # 2 columns, 3 rows
python cli.py generate video.mp4 --grid 5x4         # 5 columns, 4 rows

# Custom timing
python cli.py generate video.mp4 --clip-duration 3 --interval 45 --fps 30

# Custom processing options
python cli.py generate video.mp4 --workers 2 --height 200 --no-parallel

# Custom compression
python cli.py generate video.mp4 --lossy 80 --colors 64 --optimization 2

# Preview workflows
python cli.py preview video.mp4                     # Quick 2x2 preview
python cli.py preview video.mp4 --grid 3x2          # Custom preview grid

# Batch processing
python cli.py batch *.mp4 --preset fast             # Fast batch processing
python cli.py batch videos/*.mp4 --output-dir thumbs --suffix _thumbnail

# Information and planning
python cli.py info video.mp4                        # Basic video info
python cli.py info video.mp4 --suggest-config       # Get suggestions

# Dry run (planning mode)
python cli.py generate video.mp4 --dry-run          # See what would happen
python cli.py batch *.mp4 --dry-run                 # Plan batch operation
```

## Performance Optimization

### Parallel Processing
- Automatically detects CPU cores for optimal worker count
- Processes multiple clips simultaneously using multiprocessing
- Falls back to sequential processing for small clip counts

### Memory Management
- Temporary files for parallel processing reduce memory usage
- Automatic cleanup of temporary files and video objects
- Configurable processing resolution for memory efficiency

### Compression
- Two-stage compression: MoviePy + gifsicle
- Lossy compression significantly reduces file size
- Configurable quality vs. size trade-offs

## Examples

### Generate Quick Preview
```python
# Fast preview for quick feedback
config = create_fast_config(
    "long_video.mp4",
    "preview.gif",
    "preview_compressed.gif"
)
create_video_preview(config)
```

### High-Quality Archive
```python
# High-quality version for archival
config = create_quality_config(
    "important_video.mp4",
    "archive.gif",
    "archive_compressed.gif"
)
create_video_preview(config)
```

### Custom Grid Layout
```python
# Create wide thumbnail strip
config = create_default_config("video.mp4")
config = config._replace(cols=6, rows=2)  # 6x2 grid
create_video_preview(config)
```

## Installation and Dependencies

### Python Dependencies
```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install all dependencies
uv sync

# Or install specific packages
uv add moviepy pillow
```

### System Dependencies
```bash
# Ubuntu/Debian
sudo apt-get install gifsicle

# macOS
brew install gifsicle

# Windows
# Download from https://www.lcdf.org/gifsicle/
```

### Dependencies Overview
- **moviepy**: Video processing and clip manipulation
- **Pillow**: Image processing and frame annotation
- **gifsicle**: GIF optimization and compression (external binary)

## Error Handling

The application includes comprehensive error handling:
- Graceful fallback to sequential processing if parallel fails
- Automatic creation of placeholder clips for failed processing
- Clear error messages for common issues (missing files, gifsicle not installed)
- Progress reporting during long operations

## Contributing

This project follows functional programming principles:
1. Keep functions pure when possible
2. Use immutable data structures
3. Separate side effects from business logic
4. Write comprehensive type hints
5. Document function contracts clearly

## CLI Quick Reference

```bash
# Most Common Commands
python cli.py generate video.mp4                    # Basic generation
python cli.py preview video.mp4                     # Quick preview
python cli.py info video.mp4 --suggest-config       # Get recommendations

# Preset Workflows
python cli.py generate video.mp4 --preset fast      # Speed optimized
python cli.py generate video.mp4 --preset quality   # Quality optimized

# Custom Configurations
python cli.py generate video.mp4 --grid 3x4 --fps 25 --lossy 70
python cli.py batch *.mp4 --preset fast --output-dir thumbnails

# Planning and Testing
python cli.py generate video.mp4 --dry-run          # See configuration
python cli.py info video.mp4                        # Video information
```

## Getting Started

1. **Install dependencies**:
   ```bash
   # Install uv (if not already installed)
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # Install Python dependencies
   uv sync
   
   # Install system dependencies
   sudo apt-get install gifsicle  # or brew install gifsicle
   ```

2. **Get video information**:
   ```bash
   python cli.py info your_video.mp4 --suggest-config
   ```

3. **Generate a quick preview**:
   ```bash
   python cli.py preview your_video.mp4
   ```

4. **Create final thumbnail**:
   ```bash
   python cli.py generate your_video.mp4 --preset quality
   ```

## License

MIT License - See LICENSE file for details.
