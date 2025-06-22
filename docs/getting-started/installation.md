# Installation

## Requirements

- **Python**: 3.8 or higher
- **Operating System**: Windows, macOS, or Linux
- **Memory**: 4GB RAM minimum (8GB+ recommended for large datasets)
- **Disk Space**: Sufficient space for input and output files

## Install from PyPI

The easiest way to install ESRI Converter is using pip:

```bash
pip install esri-converter
```

## Install from Source

For the latest development version:

```bash
# Clone the repository
git clone https://github.com/mihiarc/esri-converter.git
cd esri-converter

# Install in development mode
pip install -e .
```

## Using uv (Recommended)

For faster and more reliable dependency management:

```bash
# Install uv if you haven't already
pip install uv

# Install esri-converter
uv pip install esri-converter
```

## Verify Installation

Test your installation:

```bash
# Check version
esri-converter --version

# Run help
esri-converter --help
```

You should see output similar to:

```
ESRI Converter v0.1.0
Modern Python package for converting ESRI Geodatabase files to GeoParquet format
```

## Dependencies

ESRI Converter automatically installs these key dependencies:

### Core Dependencies
- **polars** (≥0.20.0) - High-performance DataFrame library
- **duckdb** (≥0.10.0) - Analytical database engine
- **fiona** (≥1.9.0) - Geospatial data I/O
- **pyarrow** (≥15.0.0) - Apache Arrow Python bindings
- **shapely** (≥2.0.0) - Geometric operations

### UI & Progress
- **rich** (≥13.0.0) - Beautiful terminal output
- **typer** (≥0.9.0) - CLI framework

### Utilities
- **psutil** - System monitoring
- **tqdm** - Progress bars (fallback)

## Optional Dependencies

For development and testing:

```bash
# Development dependencies
pip install esri-converter[dev]

# Testing dependencies  
pip install esri-converter[test]

# Documentation dependencies
pip install esri-converter[docs]

# All optional dependencies
pip install esri-converter[all]
```

## System-Specific Notes

### Windows

No additional setup required. GDAL binaries are included with Fiona.

### macOS

Install using Homebrew for better GDAL support:

```bash
# Install GDAL (optional but recommended)
brew install gdal

# Then install esri-converter
pip install esri-converter
```

### Linux (Ubuntu/Debian)

Install system dependencies:

```bash
# Install GDAL development libraries
sudo apt-get update
sudo apt-get install gdal-bin libgdal-dev

# Install esri-converter
pip install esri-converter
```

### Linux (CentOS/RHEL)

```bash
# Install GDAL
sudo yum install gdal gdal-devel

# Install esri-converter  
pip install esri-converter
```

## Docker Installation

Use the official Docker image:

```bash
# Pull the image
docker pull mihiarc/esri-converter:latest

# Run a conversion
docker run -v $(pwd):/data mihiarc/esri-converter:latest \
  convert /data/input.gdb /data/output.parquet
```

## Conda Installation

Install from conda-forge:

```bash
# Add conda-forge channel
conda config --add channels conda-forge

# Install esri-converter
conda install esri-converter
```

## Troubleshooting

### Common Issues

#### GDAL Not Found
```bash
# Error: GDAL library not found
# Solution: Install GDAL system packages (see OS-specific notes above)
```

#### Permission Errors
```bash
# Error: Permission denied
# Solution: Use --user flag or virtual environment
pip install --user esri-converter
```

#### Memory Issues
```bash
# Error: Memory allocation failed
# Solution: Reduce chunk size or increase system memory
esri-converter convert input.gdb output.parquet --chunk-size 10000
```

### Getting Help

If you encounter issues:

1. Check the [troubleshooting guide](../user-guide/troubleshooting.md)
2. Search [existing issues](https://github.com/mihiarc/esri-converter/issues)
3. Create a [new issue](https://github.com/mihiarc/esri-converter/issues/new) with:
   - Your operating system and Python version
   - Complete error message
   - Steps to reproduce the issue

## Next Steps

- [Quick Start Guide](quickstart.md) - Your first conversion
- [Examples](examples.md) - Common usage patterns
- [User Guide](../user-guide/converting.md) - Detailed workflows 