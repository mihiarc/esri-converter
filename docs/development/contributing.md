# Contributing

We welcome contributions to ESRI Converter! This guide will help you get started with contributing code, documentation, or bug reports.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- uv (recommended) or pip
- Basic knowledge of geospatial data formats

### Development Setup

1. **Fork and Clone**

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/esri-converter.git
cd esri-converter
```

2. **Set Up Development Environment**

```bash
# Create virtual environment with uv (recommended)
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install development dependencies
uv pip install -e ".[dev,test,docs]"
```

3. **Verify Installation**

```bash
# Run tests to ensure everything works
pytest

# Check code style
ruff check .

# Build documentation
mkdocs build
```

## Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Changes

- Write code following our style guidelines
- Add tests for new functionality
- Update documentation as needed
- Follow commit message conventions

### 3. Test Your Changes

```bash
# Run all tests
pytest

# Run specific test files
pytest tests/test_converter.py

# Run with coverage
pytest --cov=esri_converter --cov-report=html

# Test with different Python versions (if available)
tox
```

### 4. Check Code Quality

```bash
# Format code
ruff format .

# Check for linting issues
ruff check .

# Type checking
mypy esri_converter/

# Check documentation
mkdocs build --strict
```

### 5. Commit and Push

```bash
git add .
git commit -m "feat: add new feature description"
git push origin feature/your-feature-name
```

### 6. Create Pull Request

- Open a pull request on GitHub
- Fill out the PR template
- Wait for review and address feedback

## Code Style Guidelines

### Python Style

We follow PEP 8 with some modifications:

```python
# Good: Clear, descriptive names
def convert_gdb_to_parquet(gdb_path: str, output_path: str) -> Dict[str, Any]:
    """Convert GDB file to GeoParquet format."""
    pass

# Good: Type hints
from typing import List, Dict, Optional, Union
from pathlib import Path

def process_chunks(
    chunks: List[Dict[str, Any]], 
    output_dir: Path,
    chunk_size: Optional[int] = None
) -> Dict[str, Union[int, str]]:
    """Process data chunks with optional chunk size."""
    pass

# Good: Docstrings
def validate_gdb_file(gdb_path: str) -> bool:
    """
    Validate that the GDB file exists and is readable.
    
    Args:
        gdb_path: Path to the GDB file
        
    Returns:
        True if valid, False otherwise
        
    Raises:
        FileNotFoundError: If GDB file doesn't exist
    """
    pass
```

### Documentation Style

Use Google-style docstrings:

```python
def convert_layer(layer_name: str, chunk_size: int = 15000) -> Dict[str, Any]:
    """
    Convert a single layer from GDB to Parquet.
    
    Args:
        layer_name: Name of the layer to convert
        chunk_size: Number of records to process at once
        
    Returns:
        Dictionary containing conversion results with keys:
        - status: 'success' or 'failed'
        - records_processed: Number of records converted
        - processing_time: Time taken in seconds
        
    Raises:
        LayerNotFoundError: If the specified layer doesn't exist
        ConversionError: If conversion fails
        
    Example:
        >>> result = convert_layer("Parcels", chunk_size=25000)
        >>> print(f"Processed {result['records_processed']} records")
    """
    pass
```

## Testing Guidelines

### Test Structure

```
tests/
├── unit/
│   ├── test_converter.py
│   ├── test_utils.py
│   └── test_api.py
├── integration/
│   ├── test_full_conversion.py
│   └── test_batch_processing.py
├── fixtures/
│   ├── sample.gdb/
│   └── expected_outputs/
└── conftest.py
```

### Writing Tests

```python
import pytest
from pathlib import Path
from esri_converter import convert_gdb_to_parquet

class TestGDBConverter:
    """Test suite for GDB conversion functionality."""
    
    def test_basic_conversion(self, sample_gdb_path, tmp_path):
        """Test basic GDB to Parquet conversion."""
        output_path = tmp_path / "output.parquet"
        
        result = convert_gdb_to_parquet(
            str(sample_gdb_path),
            str(output_path)
        )
        
        assert result['status'] == 'success'
        assert result['total_records'] > 0
        assert output_path.exists()
    
    def test_invalid_gdb_path(self):
        """Test handling of invalid GDB paths."""
        with pytest.raises(FileNotFoundError):
            convert_gdb_to_parquet(
                "nonexistent.gdb",
                "output.parquet"
            )
    
    @pytest.mark.parametrize("chunk_size", [1000, 5000, 15000])
    def test_different_chunk_sizes(self, sample_gdb_path, tmp_path, chunk_size):
        """Test conversion with different chunk sizes."""
        output_path = tmp_path / f"output_{chunk_size}.parquet"
        
        result = convert_gdb_to_parquet(
            str(sample_gdb_path),
            str(output_path),
            chunk_size=chunk_size
        )
        
        assert result['status'] == 'success'
```

### Test Fixtures

```python
# conftest.py
import pytest
from pathlib import Path

@pytest.fixture
def sample_gdb_path():
    """Provide path to sample GDB file for testing."""
    return Path(__file__).parent / "fixtures" / "sample.gdb"

@pytest.fixture
def large_gdb_path():
    """Provide path to large GDB file for performance testing."""
    return Path(__file__).parent / "fixtures" / "large_sample.gdb"
```

## Documentation Contributions

### Building Documentation

```bash
# Install documentation dependencies
uv pip install -e ".[docs]"

# Serve documentation locally
mkdocs serve

# Build static documentation
mkdocs build
```

### Writing Documentation

- Use clear, concise language
- Include code examples
- Add diagrams where helpful
- Test all code examples

## Performance Considerations

### Benchmarking

When making performance-related changes:

```python
import time
import psutil
from esri_converter import convert_gdb_to_parquet

def benchmark_conversion(gdb_path: str, chunk_size: int):
    """Benchmark conversion performance."""
    start_time = time.time()
    start_memory = psutil.virtual_memory().percent
    
    result = convert_gdb_to_parquet(
        gdb_path,
        "benchmark_output.parquet",
        chunk_size=chunk_size
    )
    
    end_time = time.time()
    end_memory = psutil.virtual_memory().percent
    
    return {
        'processing_time': end_time - start_time,
        'records_per_second': result['total_records'] / (end_time - start_time),
        'peak_memory_usage': max(start_memory, end_memory),
        'chunk_size': chunk_size
    }
```

### Memory Profiling

```bash
# Install memory profiler
pip install memory-profiler

# Profile memory usage
python -m memory_profiler examples/convert_sf_premium_nc.py
```

## Issue Guidelines

### Bug Reports

When reporting bugs, include:

1. **Environment Information**
   - Operating system and version
   - Python version
   - ESRI Converter version
   - GDAL version

2. **Reproduction Steps**
   - Minimal code example
   - Sample data (if possible)
   - Expected vs actual behavior

3. **Error Information**
   - Complete error traceback
   - Log files (if available)

### Feature Requests

For feature requests, provide:

1. **Use Case**: Why is this feature needed?
2. **Proposed Solution**: How should it work?
3. **Alternatives**: What alternatives have you considered?
4. **Implementation Ideas**: Any thoughts on implementation?

## Release Process

### Version Numbering

We follow [Semantic Versioning](https://semver.org/):

- **MAJOR**: Incompatible API changes
- **MINOR**: Backwards-compatible functionality additions
- **PATCH**: Backwards-compatible bug fixes

### Release Checklist

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Run full test suite
4. Build and test documentation
5. Create release PR
6. Tag release after merge
7. Publish to PyPI

## Code Review Process

### For Contributors

- Keep PRs focused and reasonably sized
- Write clear commit messages
- Respond to feedback promptly
- Update tests and documentation

### For Reviewers

- Be constructive and helpful
- Test changes locally when possible
- Check for performance implications
- Verify documentation updates

## Getting Help

### Development Questions

- **GitHub Discussions**: For general development questions
- **GitHub Issues**: For bug reports and feature requests
- **Code Review**: For feedback on implementation approaches

### Communication

- Be respectful and inclusive
- Follow the code of conduct
- Help newcomers get started
- Share knowledge and best practices

## Recognition

Contributors will be recognized in:

- `CONTRIBUTORS.md` file
- Release notes
- Documentation acknowledgments

Thank you for contributing to ESRI Converter! 🚀 