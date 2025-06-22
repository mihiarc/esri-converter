# Performance Tips

This guide provides strategies to optimize ESRI Converter performance for your specific use case and hardware configuration.

## Understanding Performance Factors

### Key Variables

| Factor | Impact | Optimization Strategy |
|--------|--------|--------------------|
| **Dataset Size** | High | Use appropriate chunk sizes |
| **Available Memory** | High | Configure memory-efficient settings |
| **Storage Type** | Medium | Use SSD for better I/O performance |
| **CPU Cores** | Medium | Enable parallel processing |
| **Network Storage** | High | Process locally when possible |

### Performance Bottlenecks

1. **Memory Pressure**: Large chunks causing swapping
2. **I/O Limitations**: Slow disk reads/writes
3. **Schema Processing**: Complex field type inference
4. **Geometry Complexity**: Large or complex polygons

## Chunk Size Optimization

### Automatic Optimization

Let ESRI Converter choose optimal chunk sizes:

```python
from esri_converter import convert_gdb_to_parquet
import psutil

# Get available memory
available_gb = psutil.virtual_memory().available / (1024**3)

# Auto-calculate optimal chunk size
if available_gb > 16:
    chunk_size = 50000
elif available_gb > 8:
    chunk_size = 25000
elif available_gb > 4:
    chunk_size = 15000
else:
    chunk_size = 5000

result = convert_gdb_to_parquet(
    "dataset.gdb",
    "output.parquet",
    chunk_size=chunk_size
)
```

### Manual Tuning

#### For Memory-Constrained Systems

```bash
# Conservative settings for 4GB RAM systems
esri-converter convert large.gdb output.parquet \
    --chunk-size 5000 \
    --memory-efficient
```

#### For High-Memory Systems

```bash
# Aggressive settings for 32GB+ RAM systems
esri-converter convert large.gdb output.parquet \
    --chunk-size 100000 \
    --parallel-chunks 4
```

### Chunk Size Guidelines by Dataset

| Records | RAM Available | Recommended Chunk Size | Expected Performance |
|---------|---------------|----------------------|-------------------|
| < 100K | Any | 25,000 | Fast (< 1 min) |
| 100K - 500K | 8GB | 20,000 | Moderate (1-5 min) |
| 500K - 2M | 16GB | 15,000 | Slow (5-15 min) |
| 2M - 5M | 32GB | 10,000 | Very Slow (15-30 min) |
| > 5M | 64GB+ | 5,000 | Extended (30+ min) |

## Memory Management

### Monitor Memory Usage

```python
import psutil
from esri_converter import convert_gdb_to_parquet

def memory_aware_conversion(gdb_path: str, output_path: str):
    """Convert with dynamic memory monitoring."""
    
    initial_memory = psutil.virtual_memory().percent
    
    # Start with conservative chunk size
    chunk_size = 10000
    
    # Adjust based on available memory
    if initial_memory < 50:  # Less than 50% memory used
        chunk_size = 25000
    elif initial_memory < 30:  # Less than 30% memory used
        chunk_size = 50000
    
    print(f"Starting conversion with chunk size: {chunk_size}")
    print(f"Initial memory usage: {initial_memory:.1f}%")
    
    result = convert_gdb_to_parquet(
        gdb_path,
        output_path,
        chunk_size=chunk_size
    )
    
    final_memory = psutil.virtual_memory().percent
    print(f"Final memory usage: {final_memory:.1f}%")
    
    return result
```

### Memory-Efficient Processing

```python
# Enable all memory optimization features
result = convert_gdb_to_parquet(
    "huge_dataset.gdb",
    "output.parquet",
    chunk_size=5000,           # Small chunks
    streaming=True,            # Stream processing
    memory_efficient=True,     # Minimize memory footprint
    cleanup_temp_files=True,   # Clean up immediately
    lazy_loading=True          # Load data on demand
)
```

## I/O Optimization

### Storage Considerations

#### SSD vs HDD Performance

| Storage Type | Read Speed | Write Speed | Recommendation |
|-------------|------------|-------------|----------------|
| **NVMe SSD** | 3,500 MB/s | 3,000 MB/s | Optimal for large datasets |
| **SATA SSD** | 550 MB/s | 520 MB/s | Good for most use cases |
| **7200 RPM HDD** | 150 MB/s | 150 MB/s | Use smaller chunk sizes |
| **5400 RPM HDD** | 100 MB/s | 100 MB/s | Avoid if possible |

#### Network Storage

```python
# For network-attached storage, use local temp directory
import tempfile
import shutil

def network_optimized_conversion(gdb_path: str, network_output: str):
    """Optimize conversion for network storage."""
    
    with tempfile.TemporaryDirectory() as temp_dir:
        local_output = f"{temp_dir}/temp_output.parquet"
        
        # Convert to local storage first
        result = convert_gdb_to_parquet(
            gdb_path,
            local_output,
            chunk_size=15000
        )
        
        # Copy to network location
        shutil.move(local_output, network_output)
        
    return result
```

### Parallel I/O

```python
# Enable parallel chunk processing
result = convert_gdb_to_parquet(
    "dataset.gdb",
    "output.parquet",
    chunk_size=20000,
    parallel_processing=True,
    max_workers=4,              # Number of parallel workers
    io_threads=2                # Separate I/O threads
)
```

## CPU Optimization

### Multi-Core Processing

```python
import os
from esri_converter import convert_gdb_to_parquet

# Use all available CPU cores
cpu_count = os.cpu_count()
optimal_workers = min(cpu_count, 8)  # Cap at 8 workers

result = convert_gdb_to_parquet(
    "dataset.gdb",
    "output.parquet",
    chunk_size=25000,
    parallel_processing=True,
    max_workers=optimal_workers
)
```

### CPU-Intensive Workloads

```bash
# For geometry-heavy datasets
esri-converter convert complex_geometries.gdb output.parquet \
    --chunk-size 10000 \
    --geometry-processing-threads 4 \
    --optimize-for-cpu
```

## Schema Optimization

### Pre-Analysis for Better Performance

```python
from esri_converter import get_gdb_info, convert_gdb_to_parquet

def optimized_conversion_with_analysis(gdb_path: str, output_path: str):
    """Analyze first, then optimize conversion."""
    
    # Analyze the GDB structure
    info = get_gdb_info(gdb_path)
    
    # Determine optimal settings based on analysis
    total_records = info['total_records']
    field_count = len(info['fields'])
    
    # Adjust chunk size based on complexity
    if field_count > 200:  # Many fields
        chunk_size = 5000
    elif field_count > 100:
        chunk_size = 10000
    else:
        chunk_size = 25000
    
    # Adjust for record count
    if total_records > 5000000:  # 5M+ records
        chunk_size = min(chunk_size, 10000)
    
    print(f"Optimized settings: chunk_size={chunk_size}")
    
    return convert_gdb_to_parquet(
        gdb_path,
        output_path,
        chunk_size=chunk_size
    )
```

### Schema Consistency Optimization

```python
# Pre-define schema for better performance
result = convert_gdb_to_parquet(
    "dataset.gdb",
    "output.parquet",
    force_string_types=True,    # Skip type inference
    consistent_schema=True,     # Use first chunk schema for all
    validate_schema=False       # Skip validation for speed
)
```

## Benchmarking and Monitoring

### Performance Monitoring

```python
import time
import psutil
from esri_converter import convert_gdb_to_parquet

def benchmark_conversion(gdb_path: str, output_path: str, chunk_size: int):
    """Benchmark conversion performance."""
    
    # Initial system state
    start_time = time.time()
    start_memory = psutil.virtual_memory().percent
    start_cpu = psutil.cpu_percent()
    
    # Run conversion
    result = convert_gdb_to_parquet(
        gdb_path,
        output_path,
        chunk_size=chunk_size
    )
    
    # Final measurements
    end_time = time.time()
    end_memory = psutil.virtual_memory().percent
    peak_memory = max(start_memory, end_memory)
    
    # Calculate metrics
    elapsed = end_time - start_time
    records_per_second = result['total_records'] / elapsed
    
    benchmark_results = {
        'total_time': elapsed,
        'records_processed': result['total_records'],
        'records_per_second': records_per_second,
        'peak_memory_usage': peak_memory,
        'chunk_size': chunk_size,
        'chunks_processed': result.get('chunks_processed', 0)
    }
    
    return benchmark_results

# Run benchmarks with different chunk sizes
chunk_sizes = [5000, 10000, 25000, 50000]
results = []

for chunk_size in chunk_sizes:
    print(f"Benchmarking chunk size: {chunk_size}")
    benchmark = benchmark_conversion("test.gdb", f"output_{chunk_size}.parquet", chunk_size)
    results.append(benchmark)
    
# Find optimal chunk size
optimal = max(results, key=lambda x: x['records_per_second'])
print(f"Optimal chunk size: {optimal['chunk_size']} ({optimal['records_per_second']:.0f} records/sec)")
```

### Real-Time Monitoring

```python
import threading
import time
import psutil

def monitor_system_resources(duration: int = 300):
    """Monitor system resources during conversion."""
    
    metrics = {
        'cpu_usage': [],
        'memory_usage': [],
        'disk_io': [],
        'timestamps': []
    }
    
    def collect_metrics():
        start_time = time.time()
        while time.time() - start_time < duration:
            metrics['cpu_usage'].append(psutil.cpu_percent())
            metrics['memory_usage'].append(psutil.virtual_memory().percent)
            metrics['disk_io'].append(psutil.disk_io_counters().read_bytes)
            metrics['timestamps'].append(time.time())
            time.sleep(1)
    
    # Start monitoring in background
    monitor_thread = threading.Thread(target=collect_metrics)
    monitor_thread.daemon = True
    monitor_thread.start()
    
    return metrics

# Usage
metrics = monitor_system_resources(600)  # Monitor for 10 minutes
# Run your conversion here
result = convert_gdb_to_parquet("large.gdb", "output.parquet")
```

## Hardware-Specific Optimizations

### High-Memory Systems (32GB+)

```python
# Optimize for high-memory systems
result = convert_gdb_to_parquet(
    "dataset.gdb",
    "output.parquet",
    chunk_size=100000,          # Large chunks
    parallel_processing=True,
    max_workers=8,
    memory_buffer_size="8GB",   # Large memory buffer
    aggressive_caching=True
)
```

### Low-Memory Systems (4GB)

```python
# Optimize for memory-constrained systems
result = convert_gdb_to_parquet(
    "dataset.gdb",
    "output.parquet",
    chunk_size=2500,            # Very small chunks
    streaming=True,
    memory_efficient=True,
    cleanup_temp_files=True,
    minimal_logging=True        # Reduce memory overhead
)
```

### Cloud/Container Environments

```python
# Optimize for containerized environments
import os

# Detect container limits
memory_limit = os.environ.get('MEMORY_LIMIT', '4GB')
cpu_limit = int(os.environ.get('CPU_LIMIT', '2'))

chunk_size = 5000 if memory_limit == '4GB' else 15000
max_workers = min(cpu_limit, 4)

result = convert_gdb_to_parquet(
    "dataset.gdb",
    "output.parquet",
    chunk_size=chunk_size,
    max_workers=max_workers,
    container_optimized=True
)
```

## Performance Troubleshooting

### Common Performance Issues

#### Slow Processing

```python
# Diagnostic function for slow processing
def diagnose_performance(gdb_path: str):
    """Diagnose performance issues."""
    
    from esri_converter import get_gdb_info
    import psutil
    
    info = get_gdb_info(gdb_path)
    system_info = {
        'available_memory_gb': psutil.virtual_memory().available / (1024**3),
        'cpu_count': psutil.cpu_count(),
        'disk_type': 'SSD' if psutil.disk_io_counters().read_time < 100 else 'HDD'
    }
    
    # Identify potential issues
    issues = []
    recommendations = []
    
    if info['total_records'] > 1000000 and system_info['available_memory_gb'] < 8:
        issues.append("Large dataset with limited memory")
        recommendations.append("Use chunk_size=5000 or smaller")
    
    if len(info['fields']) > 200:
        issues.append("High field count may slow processing")
        recommendations.append("Consider selecting specific layers only")
    
    if system_info['disk_type'] == 'HDD':
        issues.append("HDD storage may limit I/O performance")
        recommendations.append("Use smaller chunk sizes (5000-10000)")
    
    return {
        'gdb_info': info,
        'system_info': system_info,
        'issues': issues,
        'recommendations': recommendations
    }
```

#### Memory Issues

```bash
# For out-of-memory errors
esri-converter convert large.gdb output.parquet \
    --chunk-size 2500 \
    --memory-efficient \
    --cleanup-temp-files \
    --minimal-caching
```

#### I/O Bottlenecks

```python
# For I/O-bound processing
result = convert_gdb_to_parquet(
    "dataset.gdb",
    "output.parquet",
    chunk_size=10000,
    io_optimization=True,
    buffer_size="1GB",
    async_io=True
)
```

## Best Practices Summary

1. **Start Small**: Begin with conservative chunk sizes and increase gradually
2. **Monitor Resources**: Watch CPU, memory, and disk usage during conversion
3. **Test Different Settings**: Benchmark various configurations for your data
4. **Use Local Storage**: Process on local drives when possible
5. **Consider Data Characteristics**: Adjust settings based on field count and geometry complexity
6. **Scale Appropriately**: Match resource allocation to dataset size
7. **Clean Up**: Enable temporary file cleanup for long-running processes

Following these performance optimization strategies should help you achieve the best possible conversion speeds for your specific hardware and dataset characteristics. 