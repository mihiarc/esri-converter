# Testing Guide

This guide covers testing strategies and practices for ESRI Converter development.

## Test Structure

```
tests/
├── unit/                    # Fast, isolated tests
│   ├── test_api.py
│   ├── test_converter.py
│   └── test_utils.py
├── integration/             # Component interaction tests
│   ├── test_full_conversion.py
│   └── test_batch_processing.py
├── fixtures/                # Test data
│   ├── sample.gdb/
│   └── expected_outputs/
└── conftest.py             # Shared fixtures
```

## Running Tests

### Basic Test Execution

```bash
# Install test dependencies
uv pip install -e ".[test]"

# Run all tests
pytest

# Run specific test categories
pytest tests/unit/
pytest tests/integration/

# Run with coverage
pytest --cov=esri_converter --cov-report=html
```

### Test Configuration

```bash
# Run verbose tests
pytest -v

# Run specific test file
pytest tests/unit/test_converter.py

# Run specific test function
pytest tests/unit/test_converter.py::test_basic_conversion
```

## Writing Tests

### Unit Tests

```python
import pytest
from pathlib import Path
from esri_converter import convert_gdb_to_parquet

class TestGDBConverter:
    """Test suite for GDB conversion functionality."""
    
    def test_successful_conversion(self, sample_gdb_path, tmp_path):
        """Test successful GDB to Parquet conversion."""
        output_path = tmp_path / "output.parquet"
        
        result = convert_gdb_to_parquet(
            str(sample_gdb_path),
            str(output_path),
            chunk_size=1000
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
    
    @pytest.mark.parametrize("chunk_size", [100, 1000, 5000])
    def test_different_chunk_sizes(self, sample_gdb_path, tmp_path, chunk_size):
        """Test conversion with different chunk sizes."""
        output_path = tmp_path / f"output_{chunk_size}.parquet"
        
        result = convert_gdb_to_parquet(
            str(sample_gdb_path),
            str(output_path),
            chunk_size=chunk_size
        )
        
        assert result['status'] == 'success'
        assert result['chunk_size'] == chunk_size
```

### Integration Tests

```python
class TestFullConversion:
    """Integration tests for complete conversion workflows."""
    
    def test_multi_layer_conversion(self, multi_layer_gdb_path, tmp_path):
        """Test conversion of GDB with multiple layers."""
        output_dir = tmp_path / "converted"
        output_dir.mkdir()
        
        result = convert_gdb_to_parquet(
            str(multi_layer_gdb_path),
            output_dir=str(output_dir)
        )
        
        assert result['status'] == 'success'
        assert len(result['layers_converted']) > 1
        
        # Verify output files exist
        for layer_info in result['layers_converted']:
            layer_file = output_dir / f"{layer_info['name']}.parquet"
            assert layer_file.exists()
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
def multi_layer_gdb_path():
    """Provide path to multi-layer GDB file."""
    return Path(__file__).parent / "fixtures" / "multi_layer.gdb"
```

## Performance Testing

### Memory Usage Tests

```python
import psutil

class TestMemoryUsage:
    """Test memory usage during conversion."""
    
    def test_memory_bounded_conversion(self, large_gdb_path, tmp_path):
        """Test that memory usage stays within bounds."""
        process = psutil.Process()
        initial_memory = process.memory_info().rss
        
        result = convert_gdb_to_parquet(
            str(large_gdb_path),
            str(tmp_path / "output.parquet"),
            chunk_size=2000
        )
        
        final_memory = process.memory_info().rss
        memory_increase_mb = (final_memory - initial_memory) / 1024 / 1024
        
        assert result['status'] == 'success'
        assert memory_increase_mb < 1000  # Stay under 1GB increase
```

### Benchmarking

```python
def test_conversion_speed_benchmark(benchmark, sample_gdb_path, tmp_path):
    """Benchmark conversion speed."""
    output_path = tmp_path / "benchmark.parquet"
    
    result = benchmark(
        convert_gdb_to_parquet,
        str(sample_gdb_path),
        str(output_path),
        chunk_size=5000
    )
    
    assert result['status'] == 'success'
    
    # Performance assertions
    records_per_second = result['total_records'] / result['processing_time']
    assert records_per_second > 1000  # Minimum acceptable speed
```

## Test Data Management

### Creating Test Data

```python
def create_test_gdb(output_path: str, record_count: int = 1000):
    """Create a test GDB file with specified number of records."""
    import fiona
    from shapely.geometry import Point
    import random
    
    schema = {
        'geometry': 'Point',
        'properties': {
            'id': 'int',
            'name': 'str',
            'value': 'float'
        }
    }
    
    with fiona.open(
        output_path,
        'w',
        driver='OpenFileGDB',
        schema=schema,
        crs='EPSG:4326'
    ) as dst:
        for i in range(record_count):
            point = Point(random.uniform(-180, 180), random.uniform(-90, 90))
            
            feature = {
                'geometry': point.__geo_interface__,
                'properties': {
                    'id': i,
                    'name': f'Point_{i}',
                    'value': random.uniform(0, 100)
                }
            }
            dst.write(feature)
```

## Best Practices

### Test Naming

Use descriptive test names that explain the scenario:

```python
def test_should_convert_gdb_when_valid_input_provided():
    """Clear test names improve readability."""
    pass

def test_should_raise_error_when_gdb_file_not_found():
    """Use 'should_action_when_condition' pattern."""
    pass
```

### Assertions with Messages

```python
def test_conversion_result():
    result = convert_gdb_to_parquet("test.gdb", "output.parquet")
    
    assert result['status'] == 'success', f"Conversion failed: {result.get('error')}"
    assert result['total_records'] > 0, "No records were converted"
```

### Test Isolation

- Each test should be independent
- Use fixtures for setup and teardown
- Clean up temporary files
- Reset global state between tests

## Debugging Tests

```bash
# Run with verbose output
pytest -v -s

# Run single test with debugging
pytest -v -s tests/unit/test_converter.py::test_basic_conversion

# Drop into debugger on failure
pytest --pdb

# Generate coverage report
pytest --cov=esri_converter --cov-report=html
```

## Continuous Integration

Tests run automatically on GitHub Actions for:
- Multiple Python versions (3.8, 3.9, 3.10, 3.11)
- Multiple operating systems (Ubuntu, Windows, macOS)
- Coverage reporting and quality checks

This testing framework ensures code reliability and catches regressions early in development. 