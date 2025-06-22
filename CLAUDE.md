# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ESRI Converter is a modern Python package for converting ESRI Geodatabase (GDB) files to OGC-compliant GeoParquet format. Built for 2025 with performance and developer experience in mind, using GeoPandas, Polars, Rich, PyArrow, Fiona, and Shapely. The package now produces valid GeoParquet files that can be read by all standard geospatial tools.

## Key Commands

### Development Setup
```bash
# Create and activate virtual environment
uv venv
source .venv/bin/activate

# Install in development mode
uv pip install -e ".[dev]"    # Development dependencies
uv pip install -e ".[all]"    # All optional dependencies
```

### Code Quality
```bash
# Format code
uv run black esri_converter/

# Lint code
uv run ruff check esri_converter/

# Type check
uv run mypy esri_converter/

# Run tests (when implemented)
uv run pytest
uv run pytest --cov=esri_converter
```

### Documentation
```bash
# Install docs dependencies
python scripts/docs.py install

# Serve docs locally (http://127.0.0.1:8000)
python scripts/docs.py serve

# Build documentation
python scripts/docs.py build
```

### Publishing
```bash
# Full test publish workflow
python scripts/publish.py full-test

# Full live publish workflow (requires PYPI_LIVE_TOKEN)
python scripts/publish.py full-live
```

## Architecture Overview

### Module Structure
```
esri_converter/
├── __init__.py                  # Public API exports
├── api.py                      # High-level conversion functions
├── exceptions.py               # Custom exception hierarchy
├── converters/                 # Core conversion engines
│   └── geoparquet_converter.py # GeoParquetConverter (OGC-compliant output)
└── utils/              
    ├── formats.py              # Format information and recommendations
    └── validation.py           # Input validation functions
```

### Core API Functions
- `convert_gdb_to_parquet()` - Single GDB conversion with detailed metrics
- `convert_multiple_gdbs()` - Batch conversion with aggregate results
- `discover_gdb_files()` - Find GDB files in directories
- `get_gdb_info()` - Non-destructive GDB inspection

### Key Design Patterns
1. **Streaming Architecture**: Chunk-based processing for large datasets (default: 15,000 records/chunk)
2. **Rich UI Integration**: Beautiful console output with progress bars, tables, and trees
3. **Comprehensive Error Handling**: Custom exception hierarchy with context preservation
4. **Lazy Evaluation**: Uses Polars for memory-efficient operations

### Exception Hierarchy
```
ESRIConverterError
├── UnsupportedFormatError
├── ValidationError
├── ConversionError
│   ├── SchemaError
│   └── MemoryError
└── FileAccessError
```

## Development Notes

1. **Python Version**: Requires Python 3.10+
2. **Package Manager**: Always use `uv` for Python operations
3. **Testing**: Currently no unit tests - test scripts exist but formal test suite needs implementation
4. **Type Safety**: Project uses strict mypy configuration
5. **Code Style**: Ruff for linting and formatting with 100-character line length
6. **Main Converter**: `GeoParquetConverter` (aliased as `GDBConverter` for compatibility)
7. **Default Output**: Creates "geoparquet_output" directory if not specified

## Important Considerations

- The CLI is commented out in v0.1.0 - focus is on Python API
- GDAL warnings are suppressed for cleaner output
- Schema normalization handles inconsistent field types across chunks
- Memory-efficient processing adapts based on dataset characteristics
- Rich console output provides detailed progress and performance metrics
- **GeoParquet Compliance**: All output files are OGC GeoParquet v1.0.0 compliant
- **GeoPandas Dependency**: Required for proper GeoParquet output with WKB geometry storage
- **Geometry Storage**: Uses WKB (Well-Known Binary) format for optimal performance