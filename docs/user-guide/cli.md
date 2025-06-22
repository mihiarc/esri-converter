# Command Line Usage

ESRI Converter provides a comprehensive command-line interface for converting GDB files to GeoParquet format. This guide covers all available commands and options.

## Installation and Setup

First, ensure ESRI Converter is installed:

```bash
pip install esri-converter
```

Verify the installation:

```bash
esri-converter --version
```

## Basic Commands

### `convert` - Single File Conversion

Convert a single GDB file to GeoParquet:

```bash
esri-converter convert input.gdb output.parquet
```

#### Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--chunk-size` | `-c` | Records per processing chunk | 15000 |
| `--layers` | `-l` | Specific layers to convert | All layers |
| `--output-dir` | `-o` | Output directory | Current directory |
| `--verbose` | `-v` | Enable verbose logging | False |
| `--quiet` | `-q` | Suppress progress output | False |

#### Examples

```bash
# Basic conversion
esri-converter convert sample.gdb sample.parquet

# Custom chunk size for memory optimization
esri-converter convert large.gdb output.parquet --chunk-size 25000

# Convert specific layers only
esri-converter convert municipal.gdb output.parquet --layers Parcels Buildings

# Verbose output for debugging
esri-converter convert data.gdb output.parquet --verbose

# Output to specific directory
esri-converter convert data.gdb --output-dir ./converted/
```

### `batch-convert` - Multiple File Processing

Convert multiple GDB files in batch:

```bash
esri-converter batch-convert *.gdb --output-dir ./converted/
```

#### Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--output-dir` | `-o` | Output directory | `./converted/` |
| `--chunk-size` | `-c` | Records per chunk | 15000 |
| `--parallel` | `-p` | Enable parallel processing | False |
| `--max-workers` | `-w` | Maximum parallel workers | CPU count |
| `--continue-on-error` |  | Continue if one file fails | False |

#### Examples

```bash
# Convert all GDB files in current directory
esri-converter batch-convert *.gdb

# Parallel processing with custom workers
esri-converter batch-convert *.gdb --parallel --max-workers 4

# Continue processing even if some files fail
esri-converter batch-convert *.gdb --continue-on-error

# Custom output directory and chunk size
esri-converter batch-convert /data/*.gdb \
    --output-dir /output/ \
    --chunk-size 30000
```

### `info` - GDB Analysis

Analyze GDB file structure and metadata:

```bash
esri-converter info sample.gdb
```

#### Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--detailed` | `-d` | Show detailed layer information | False |
| `--json` | `-j` | Output in JSON format | False |
| `--layers` | `-l` | Analyze specific layers only | All layers |

#### Examples

```bash
# Basic information
esri-converter info municipal.gdb

# Detailed analysis
esri-converter info municipal.gdb --detailed

# JSON output for scripting
esri-converter info municipal.gdb --json

# Analyze specific layers
esri-converter info municipal.gdb --layers Parcels Buildings
```

#### Sample Output

```
📊 GDB Analysis: municipal.gdb
=====================================
📁 File Size: 2.3 GB
📋 Total Layers: 3
📊 Total Records: 1,250,000
🗓️  Last Modified: 2025-01-28 10:30:00

Layer Details:
┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
┃ Layer              ┃ Records      ┃ Geometry Type ┃ CRS           ┃
┡━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
│ Parcels            │ 850,000      │ MultiPolygon  │ EPSG:4326     │
│ Buildings          │ 350,000      │ Polygon       │ EPSG:4326     │
│ Roads              │ 50,000       │ LineString    │ EPSG:4326     │
└────────────────────┴──────────────┴───────────────┴───────────────┘
```

## Advanced Usage

### Memory Management

Control memory usage with chunk size optimization:

```bash
# For systems with limited memory (4GB)
esri-converter convert large.gdb output.parquet --chunk-size 5000

# For high-memory systems (32GB+)
esri-converter convert large.gdb output.parquet --chunk-size 100000

# Auto-optimize based on available memory
esri-converter convert large.gdb output.parquet --chunk-size auto
```

### Performance Optimization

```bash
# Maximum performance settings
esri-converter convert dataset.gdb output.parquet \
    --chunk-size 50000 \
    --parallel-chunks 4 \
    --optimize-performance

# Memory-efficient settings
esri-converter convert dataset.gdb output.parquet \
    --chunk-size 5000 \
    --memory-efficient \
    --cleanup-temp-files
```

### Error Handling

```bash
# Continue processing with error recovery
esri-converter convert problematic.gdb output.parquet \
    --continue-on-error \
    --retry-failed-chunks \
    --max-retries 3

# Skip invalid geometries
esri-converter convert dataset.gdb output.parquet \
    --skip-invalid-geometries \
    --validate-geometries
```

## Configuration Files

### Using Configuration Files

Create a configuration file for repeated use:

```yaml
# esri-converter.yaml
chunk_size: 25000
output_dir: "./converted/"
parallel: true
max_workers: 4
verbose: true
continue_on_error: true
```

Use the configuration:

```bash
esri-converter convert dataset.gdb --config esri-converter.yaml
```

### Environment Variables

Set default options via environment variables:

```bash
export ESRI_CONVERTER_CHUNK_SIZE=25000
export ESRI_CONVERTER_OUTPUT_DIR="./converted/"
export ESRI_CONVERTER_VERBOSE=true

esri-converter convert dataset.gdb output.parquet
```

## Scripting and Automation

### Bash Scripting

```bash
#!/bin/bash
# convert_all_gdbs.sh

# Set parameters
CHUNK_SIZE=25000
OUTPUT_DIR="./converted"
LOG_FILE="conversion.log"

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Process all GDB files
for gdb_file in *.gdb; do
    if [ -d "$gdb_file" ]; then
        echo "Processing $gdb_file..." | tee -a "$LOG_FILE"
        
        esri-converter convert "$gdb_file" \
            --output-dir "$OUTPUT_DIR" \
            --chunk-size "$CHUNK_SIZE" \
            --verbose 2>&1 | tee -a "$LOG_FILE"
        
        if [ $? -eq 0 ]; then
            echo "✅ Successfully converted $gdb_file" | tee -a "$LOG_FILE"
        else
            echo "❌ Failed to convert $gdb_file" | tee -a "$LOG_FILE"
        fi
    fi
done

echo "Conversion complete. Check $LOG_FILE for details."
```

### PowerShell Scripting

```powershell
# convert_all_gdbs.ps1

$ChunkSize = 25000
$OutputDir = ".\converted"
$LogFile = "conversion.log"

# Create output directory
New-Item -ItemType Directory -Force -Path $OutputDir

# Process all GDB files
Get-ChildItem -Directory -Filter "*.gdb" | ForEach-Object {
    $GdbFile = $_.Name
    Write-Host "Processing $GdbFile..." -ForegroundColor Yellow
    
    $Command = "esri-converter convert `"$GdbFile`" --output-dir `"$OutputDir`" --chunk-size $ChunkSize --verbose"
    
    try {
        Invoke-Expression $Command 2>&1 | Tee-Object -FilePath $LogFile -Append
        Write-Host "✅ Successfully converted $GdbFile" -ForegroundColor Green
    }
    catch {
        Write-Host "❌ Failed to convert $GdbFile" -ForegroundColor Red
        $_.Exception.Message | Tee-Object -FilePath $LogFile -Append
    }
}

Write-Host "Conversion complete. Check $LogFile for details."
```

## Integration with Other Tools

### Using with Make

```makefile
# Makefile for GDB conversion

CHUNK_SIZE = 25000
OUTPUT_DIR = ./converted
GDB_FILES = $(wildcard *.gdb)
PARQUET_FILES = $(patsubst %.gdb,$(OUTPUT_DIR)/%.parquet,$(GDB_FILES))

.PHONY: all clean info

all: $(PARQUET_FILES)

$(OUTPUT_DIR)/%.parquet: %.gdb
	@mkdir -p $(OUTPUT_DIR)
	esri-converter convert $< --output-dir $(OUTPUT_DIR) --chunk-size $(CHUNK_SIZE)

info:
	@for gdb in $(GDB_FILES); do \
		echo "Analyzing $$gdb..."; \
		esri-converter info $$gdb; \
	done

clean:
	rm -rf $(OUTPUT_DIR)
```

### Docker Usage

```bash
# Using Docker for isolated processing
docker run -v $(pwd):/data mihiarc/esri-converter:latest \
    convert /data/input.gdb /data/output.parquet --chunk-size 25000

# Batch processing with Docker
docker run -v $(pwd):/data mihiarc/esri-converter:latest \
    batch-convert /data/*.gdb --output-dir /data/converted/
```

## Monitoring and Logging

### Progress Monitoring

```bash
# Real-time progress with detailed output
esri-converter convert large.gdb output.parquet \
    --verbose \
    --progress-bar \
    --show-eta

# Log to file while showing progress
esri-converter convert large.gdb output.parquet \
    --verbose 2>&1 | tee conversion.log
```

### Performance Metrics

```bash
# Enable performance metrics
esri-converter convert dataset.gdb output.parquet \
    --benchmark \
    --memory-monitoring \
    --performance-report metrics.json
```

## Troubleshooting

### Common Issues and Solutions

#### Command Not Found

```bash
# Error: esri-converter: command not found
# Solution: Ensure package is installed and in PATH
pip install esri-converter
which esri-converter
```

#### Permission Errors

```bash
# Error: Permission denied
# Solution: Check file permissions or run with appropriate privileges
chmod +r input.gdb
sudo esri-converter convert input.gdb output.parquet
```

#### Memory Issues

```bash
# Error: Memory allocation failed
# Solution: Reduce chunk size
esri-converter convert large.gdb output.parquet --chunk-size 5000
```

#### Invalid GDB Files

```bash
# Error: Unable to open GDB file
# Solution: Verify file integrity and format
esri-converter info input.gdb --validate
```

### Debug Mode

Enable detailed debugging:

```bash
esri-converter convert problematic.gdb output.parquet \
    --debug \
    --log-level DEBUG \
    --save-debug-info debug_output/
```

## Getting Help

### Built-in Help

```bash
# General help
esri-converter --help

# Command-specific help
esri-converter convert --help
esri-converter batch-convert --help
esri-converter info --help
```

### Version Information

```bash
# Show version and build info
esri-converter --version --verbose

# Show dependencies
esri-converter --version --show-deps
```

This comprehensive CLI guide should help you effectively use ESRI Converter from the command line for all your GDB conversion needs. 