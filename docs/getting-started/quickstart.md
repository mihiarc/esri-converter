# Quick Start

Get up and running with ESRI Converter in just 5 minutes! This guide will walk you through your first GDB to GeoParquet conversion.

## Step 1: Installation

First, install the package:

```bash
pip install esri-converter
```

## Step 2: Verify Installation

Check that everything is working:

```bash
esri-converter --version
```

## Step 3: Your First Conversion

### Using the Command Line

Convert a single GDB file:

```bash
esri-converter convert input.gdb output.parquet
```

### Using Python API

```python
from esri_converter import convert_gdb_to_parquet

# Convert with default settings
result = convert_gdb_to_parquet("input.gdb", "output.parquet")
print(f"Converted {result['total_records']} records")
```

## Step 4: Monitor Progress

ESRI Converter provides beautiful progress tracking:

```
🗺️  ESRI Converter - GDB to Parquet
==================================================
📁 Input GDB: sample.gdb
📂 Output: sample.parquet
📊 Analyzing GDB file...

╔════════════════════════ Enhanced Converter ═══════════════════════════╗
║  🗺️  GDB to GeoParquet Converter                                        ║
║  Modern Large-Scale Geospatial Data Processing                          ║
╚═════════════════════════════════════════════════════════════════════════╝

Processing Layer 1/2
  Layer: Parcels
┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
┃ Property      ┃ Value         ┃
┡━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
│ Records       │ 1,250,000     │
│ Geometry Type │ MultiPolygon  │
│ CRS           │ EPSG:4326     │
│ Fields        │ 156           │
└───────────────┴───────────────┘

Converting Parcels ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:02:15
```

## Step 5: Explore Your Data

The output GeoParquet file can be used with many tools:

### With GeoPandas
```python
import geopandas as gpd

# Read the converted file
gdf = gpd.read_parquet("output.parquet")
print(f"Loaded {len(gdf)} features")
print(gdf.head())
```

### With Polars
```python
import polars as pl

# Read with Polars for high performance
df = pl.read_parquet("output.parquet")
print(f"Shape: {df.shape}")
print(df.head())
```

### With DuckDB
```python
import duckdb

# Query directly from file
conn = duckdb.connect()
result = conn.execute("""
    SELECT COUNT(*) as total_features 
    FROM 'output.parquet'
""").fetchone()
print(f"Total features: {result[0]}")
```

## Common Options

### Chunk Size
For large files, adjust the chunk size:

```bash
# Smaller chunks for limited memory
esri-converter convert input.gdb output.parquet --chunk-size 10000

# Larger chunks for better performance
esri-converter convert input.gdb output.parquet --chunk-size 50000
```

### Specific Layers
Convert only specific layers:

```bash
esri-converter convert input.gdb output.parquet --layers Parcels Buildings
```

### Batch Processing
Convert multiple GDB files:

```bash
esri-converter batch-convert *.gdb --output-dir ./converted/
```

## Performance Tips

!!! tip "Memory Optimization"
    For large datasets (>1GB), use smaller chunk sizes:
    ```bash
    esri-converter convert large.gdb output.parquet --chunk-size 15000
    ```

!!! tip "Speed Optimization"
    For faster processing on powerful machines:
    ```bash
    esri-converter convert input.gdb output.parquet --chunk-size 100000
    ```

## What's Happening Under the Hood?

When you run a conversion, ESRI Converter:

1. **Analyzes** the GDB file structure and layers
2. **Discovers** geometry types and field schemas
3. **Streams** data in configurable chunks
4. **Normalizes** schemas across chunks
5. **Combines** chunks into the final GeoParquet file

## Troubleshooting

### File Not Found
```bash
# Error: [Errno 2] No such file or directory: 'input.gdb'
# Solution: Check the file path
ls -la *.gdb
```

### Memory Issues
```bash
# Error: Cannot allocate memory
# Solution: Reduce chunk size
esri-converter convert input.gdb output.parquet --chunk-size 5000
```

### Large Files Taking Too Long
```bash
# Solution: Increase chunk size for better performance
esri-converter convert input.gdb output.parquet --chunk-size 50000
```

## Next Steps

Now that you've completed your first conversion, explore more advanced features:

- **[Examples](examples.md)** - Common usage patterns and workflows
- **[User Guide](../user-guide/converting.md)** - Detailed conversion options
- **[Performance Tips](../user-guide/performance.md)** - Optimize for your use case
- ****API Reference** - Complete function documentation (available in code docstrings)** - Complete API documentation

## Real-World Example

Here's a complete example converting a large municipal dataset:

```python
from esri_converter import convert_gdb_to_parquet
import time

# Convert a large municipal GDB file
start_time = time.time()

result = convert_gdb_to_parquet(
    gdb_path="municipal_data.gdb",
    output_path="municipal_data.parquet",
    chunk_size=25000,
    layers=["Parcels", "Buildings", "Roads"]
)

elapsed = time.time() - start_time

print(f"""
Conversion Complete! 
├── Total Records: {result['total_records']:,}
├── Layers Converted: {len(result['layers_converted'])}
├── Processing Time: {elapsed:.2f} seconds
├── Output Size: {result['output_size_mb']:.2f} MB
└── Processing Rate: {result['total_records']/elapsed:,.0f} records/second
""")
```

Ready to convert your own data? Let's go! 🚀 