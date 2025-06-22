# Batch Processing

This guide covers efficient batch processing of multiple GDB files using ESRI Converter's batch capabilities.

## Overview

Batch processing allows you to convert multiple GDB files simultaneously, with features like:

- **Parallel Processing**: Convert multiple files at once
- **Error Recovery**: Continue processing even if some files fail
- **Progress Tracking**: Monitor overall batch progress
- **Resource Management**: Optimize memory and CPU usage across files

## Basic Batch Conversion

### Command Line

```bash
# Convert all GDB files in current directory
esri-converter batch-convert *.gdb --output-dir ./converted/

# Convert with custom settings
esri-converter batch-convert *.gdb \
    --output-dir ./converted/ \
    --chunk-size 25000 \
    --parallel \
    --max-workers 4
```

### Python API

```python
from esri_converter import convert_multiple_gdbs
import glob

# Find all GDB files
gdb_files = glob.glob("*.gdb")

# Convert with batch processing
results = convert_multiple_gdbs(
    gdb_files,
    output_dir="./converted/",
    chunk_size=25000,
    parallel=True,
    max_workers=4
)

# Process results
for result in results:
    if result['status'] == 'success':
        print(f"✅ {result['gdb_name']}: {result['total_records']} records")
    else:
        print(f"❌ {result['gdb_name']}: {result['error']}")
```

## Advanced Features

### Automatic Discovery

```python
from esri_converter import discover_gdb_files, convert_multiple_gdbs

# Discover GDB files recursively
gdb_files = discover_gdb_files(
    search_dir="./data/",
    recursive=True,
    pattern="*municipal*.gdb"
)

print(f"Found {len(gdb_files)} GDB files")

# Convert all discovered files
results = convert_multiple_gdbs(
    gdb_files,
    output_dir="./converted/",
    chunk_size=20000
)
```

### Error Handling

```python
# Continue processing even if some files fail
results = convert_multiple_gdbs(
    gdb_files,
    output_dir="./converted/",
    continue_on_error=True,
    retry_failed=True,
    max_retries=3
)

# Separate successful and failed conversions
successful = [r for r in results if r['status'] == 'success']
failed = [r for r in results if r['status'] == 'failed']

print(f"Successful: {len(successful)}, Failed: {len(failed)}")
```

## Performance Optimization

### Memory-Aware Processing

```python
import os
import psutil

# Determine optimal worker count
cpu_count = os.cpu_count()
available_memory_gb = psutil.virtual_memory().available / (1024**3)

# Calculate optimal workers based on resources
if available_memory_gb >= 32:
    max_workers = min(cpu_count, 8)
    chunk_size = 50000
elif available_memory_gb >= 16:
    max_workers = min(cpu_count, 4)
    chunk_size = 25000
else:
    max_workers = min(cpu_count, 2)
    chunk_size = 15000

results = convert_multiple_gdbs(
    gdb_files,
    output_dir="./converted/",
    parallel=True,
    max_workers=max_workers,
    chunk_size=chunk_size
)
```

### Progress Monitoring

```python
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

def batch_convert_with_progress(gdb_files, output_dir):
    """Batch convert with detailed progress tracking."""
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        refresh_per_second=1
    ) as progress:
        
        # Create overall progress task
        overall_task = progress.add_task(
            f"Converting {len(gdb_files)} GDB files...", 
            total=len(gdb_files)
        )
        
        results = []
        
        for i, gdb_file in enumerate(gdb_files):
            # Update current file
            progress.update(
                overall_task, 
                description=f"Converting {Path(gdb_file).name} ({i+1}/{len(gdb_files)})"
            )
            
            try:
                result = convert_gdb_to_parquet(
                    gdb_file,
                    f"{output_dir}/{Path(gdb_file).stem}.parquet",
                    chunk_size=20000
                )
                results.append(result)
                
            except Exception as e:
                results.append({
                    'gdb_path': gdb_file,
                    'status': 'failed',
                    'error': str(e)
                })
            
            # Update progress
            progress.update(overall_task, advance=1)
        
    return results
```

## Automation and Scheduling

### Automated Pipeline

```python
#!/usr/bin/env python3
"""Automated GDB processing pipeline"""

import os
import time
import shutil
from pathlib import Path
from esri_converter import discover_gdb_files, convert_multiple_gdbs

def process_directory(input_dir, output_dir, processed_dir):
    """Process all GDB files in input directory."""
    
    # Discover new GDB files
    gdb_files = discover_gdb_files(input_dir, recursive=False)
    
    if not gdb_files:
        print("No GDB files found for processing")
        return
    
    print(f"Found {len(gdb_files)} GDB files to process")
    
    # Convert files
    results = convert_multiple_gdbs(
        gdb_files,
        output_dir=output_dir,
        chunk_size=25000,
        parallel=True,
        max_workers=4,
        continue_on_error=True
    )
    
    # Move processed files
    for result in results:
        if result['status'] == 'success':
            source_path = Path(result['gdb_path'])
            dest_path = Path(processed_dir) / source_path.name
            shutil.move(str(source_path), str(dest_path))
    
    # Log summary
    successful = len([r for r in results if r['status'] == 'success'])
    failed = len([r for r in results if r['status'] == 'failed'])
    print(f"Processing complete: {successful} successful, {failed} failed")

# Main loop
while True:
    process_directory("/data/incoming", "/data/converted", "/data/processed")
    time.sleep(300)  # Check every 5 minutes
```

## Best Practices

1. **Start Small**: Test with a few files before processing large batches
2. **Monitor Resources**: Watch CPU and memory usage during batch processing
3. **Use Error Recovery**: Enable continue-on-error for large batches
4. **Validate Results**: Check output files after batch processing
5. **Plan Resources**: Calculate optimal worker count based on available memory

This batch processing guide provides the foundation for efficiently converting multiple GDB files at scale. 