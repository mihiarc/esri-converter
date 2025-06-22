# Converting GDB Files

This guide covers everything you need to know about converting ESRI Geodatabase files to GeoParquet format using ESRI Converter.

## Understanding GDB Files

ESRI Geodatabase (GDB) files are proprietary geospatial data containers that can store:

- **Vector data**: Points, lines, polygons
- **Raster data**: Images, elevation models  
- **Attribute data**: Tables with spatial and non-spatial information
- **Relationships**: Spatial and attribute relationships between datasets
- **Metadata**: Coordinate systems, field definitions, etc.

## GeoParquet Benefits

Converting to GeoParquet provides several advantages:

| Aspect | GDB | GeoParquet |
|--------|-----|------------|
| **File Size** | Larger, proprietary compression | Smaller, efficient columnar storage |
| **Performance** | Good for ESRI tools | Excellent for analytical queries |
| **Compatibility** | ESRI ecosystem | Universal (Python, R, SQL, etc.) |
| **Cloud Native** | Limited support | Optimized for cloud storage |
| **Streaming** | Requires full load | Supports partial reads |

## Basic Conversion

### Single Layer Conversion

Convert a simple GDB file:

```bash
esri-converter convert sample.gdb output.parquet
```

This will:
1. Analyze the GDB structure
2. Convert all layers to separate Parquet files
3. Show progress with rich UI
4. Generate summary statistics

### Specific Layer Selection

Convert only specific layers:

```bash
esri-converter convert municipal.gdb output.parquet --layers Parcels Buildings
```

### Python API Approach

```python
from esri_converter import convert_gdb_to_parquet

result = convert_gdb_to_parquet(
    gdb_path="municipal.gdb",
    output_path="municipal.parquet",
    layers=["Parcels", "Buildings"],
    chunk_size=25000
)

print(f"Conversion completed: {result['status']}")
print(f"Records processed: {result['total_records']:,}")
```

## Advanced Options

### Chunk Size Optimization

The chunk size parameter controls memory usage and performance:

```bash
# Small chunks (low memory, slower)
esri-converter convert large.gdb output.parquet --chunk-size 5000

# Large chunks (high memory, faster)  
esri-converter convert large.gdb output.parquet --chunk-size 100000

# Auto-optimization based on available memory
esri-converter convert large.gdb output.parquet --chunk-size auto
```

#### Chunk Size Guidelines

| Dataset Size | Available RAM | Recommended Chunk Size |
|-------------|---------------|----------------------|
| < 100MB | Any | 50,000 |
| 100MB - 1GB | 4GB | 25,000 |
| 1GB - 5GB | 8GB | 15,000 |
| 5GB - 10GB | 16GB | 10,000 |
| > 10GB | 32GB+ | 5,000 |

### Schema Handling

ESRI Converter automatically handles schema inconsistencies:

- **Type normalization**: Converts all fields to strings for consistency
- **Missing fields**: Adds null values for missing columns
- **Field ordering**: Maintains consistent column order across chunks

### Geometry Processing

#### Coordinate Reference Systems

The converter preserves CRS information:

```python
# Check CRS information
from esri_converter import get_gdb_info

info = get_gdb_info("sample.gdb")
for layer in info['layers']:
    print(f"{layer['name']}: {layer['crs']}")
```

#### Geometry Formats

Geometries are stored as Well-Known Text (WKT):

```python
import polars as pl

df = pl.read_parquet("converted.parquet")
print(df.select("geometry_wkt").head())
```

## Performance Optimization

### Memory Management

For large datasets, optimize memory usage:

```python
result = convert_gdb_to_parquet(
    "huge_dataset.gdb",
    "output.parquet",
    chunk_size=5000,           # Small chunks
    streaming=True,            # Enable streaming mode
    memory_efficient=True      # Minimize memory footprint
)
```

### Parallel Processing

Enable parallel chunk processing:

```python
result = convert_gdb_to_parquet(
    "dataset.gdb",
    "output.parquet",
    chunk_size=25000,
    parallel_processing=True,
    max_workers=4
)
```

### Progress Monitoring

Monitor conversion progress:

```python
from esri_converter import EnhancedGDBConverter

converter = EnhancedGDBConverter()
result = converter.convert_gdb_enhanced(
    "large_dataset.gdb",
    chunk_size=20000
)
```

## Error Handling

### Common Issues and Solutions

#### Memory Errors

```bash
# Error: Cannot allocate memory
# Solution: Reduce chunk size
esri-converter convert large.gdb output.parquet --chunk-size 5000
```

#### Schema Mismatches

The converter automatically handles schema inconsistencies, but you can also:

```python
# Force string conversion for all fields
result = convert_gdb_to_parquet(
    "problematic.gdb",
    "output.parquet",
    force_string_types=True
)
```

#### Corrupted Geometries

```python
# Skip invalid geometries
result = convert_gdb_to_parquet(
    "dataset.gdb",
    "output.parquet",
    skip_invalid_geometries=True,
    validate_geometries=True
)
```

### Logging and Debugging

Enable detailed logging:

```python
import logging
from esri_converter import convert_gdb_to_parquet

# Configure logging
logging.basicConfig(level=logging.DEBUG)

result = convert_gdb_to_parquet(
    "debug_dataset.gdb",
    "output.parquet",
    verbose=True
)
```

## Quality Assurance

### Validation Workflow

```python
from esri_converter import convert_gdb_to_parquet, get_gdb_info
import polars as pl

def validate_conversion(gdb_path: str, output_path: str):
    """Validate conversion quality."""
    
    # Get original info
    original = get_gdb_info(gdb_path)
    
    # Convert
    result = convert_gdb_to_parquet(gdb_path, output_path)
    
    # Load converted data
    df = pl.read_parquet(output_path)
    
    # Validation checks
    checks = {
        'record_count_match': len(df) == original['total_records'],
        'no_null_geometries': df['geometry_wkt'].null_count() == 0,
        'valid_field_count': len(df.columns) >= len(original['fields'])
    }
    
    return checks

# Usage
validation = validate_conversion("sample.gdb", "sample.parquet")
print("Validation results:", validation)
```

### Data Integrity Checks

```python
def check_data_integrity(original_gdb: str, converted_parquet: str):
    """Comprehensive data integrity check."""
    
    import fiona
    import polars as pl
    
    # Count records in original
    with fiona.open(original_gdb) as src:
        original_count = len(src)
    
    # Count records in converted
    df = pl.read_parquet(converted_parquet)
    converted_count = len(df)
    
    # Check geometry validity
    valid_geoms = df.filter(
        pl.col('geometry_wkt').is_not_null() &
        (pl.col('geometry_wkt').str.len_chars() > 0)
    ).height
    
    return {
        'record_count_original': original_count,
        'record_count_converted': converted_count,
        'data_integrity': original_count == converted_count,
        'geometry_completeness': valid_geoms / converted_count * 100,
        'conversion_success_rate': converted_count / original_count * 100
    }
```

## Best Practices

### 1. Pre-Conversion Analysis

Always analyze your GDB first:

```bash
esri-converter info dataset.gdb
```

### 2. Test with Small Datasets

Start with a subset:

```python
# Convert first 1000 records for testing
result = convert_gdb_to_parquet(
    "large_dataset.gdb",
    "test_output.parquet",
    max_records=1000
)
```

### 3. Monitor System Resources

```python
import psutil
from esri_converter import convert_gdb_to_parquet

# Check available memory
available_memory = psutil.virtual_memory().available / (1024**3)  # GB
recommended_chunk_size = min(50000, int(available_memory * 5000))

result = convert_gdb_to_parquet(
    "dataset.gdb",
    "output.parquet",
    chunk_size=recommended_chunk_size
)
```

### 4. Backup Important Data

```bash
# Create backup before conversion
cp -r original.gdb original_backup.gdb
esri-converter convert original.gdb converted.parquet
```

### 5. Validate Results

Always validate your converted data:

```python
# Quick validation
df = pl.read_parquet("converted.parquet")
print(f"Records: {len(df):,}")
print(f"Columns: {len(df.columns)}")
print(f"Null geometries: {df['geometry_wkt'].null_count()}")
```

## Output Formats

### Single File Output

```bash
# All layers combined into one file
esri-converter convert dataset.gdb combined.parquet --combine-layers
```

### Separate Files per Layer

```bash
# Default: separate file per layer
esri-converter convert dataset.gdb --output-dir ./converted/
```

### Custom Naming

```python
result = convert_gdb_to_parquet(
    "dataset.gdb",
    output_dir="./custom_output/",
    naming_pattern="{layer_name}_{date}.parquet"
)
```

## Integration with Other Tools

### Loading in GeoPandas

```python
import geopandas as gpd

# Read converted GeoParquet
gdf = gpd.read_parquet("converted.parquet")
print(gdf.info())
```

### Querying with DuckDB

```python
import duckdb

conn = duckdb.connect()
conn.execute("INSTALL spatial; LOAD spatial;")

# Query the converted data
result = conn.execute("""
    SELECT COUNT(*) as feature_count,
           AVG(ST_Area(ST_GeomFromText(geometry_wkt))) as avg_area
    FROM 'converted.parquet'
    WHERE geometry_wkt IS NOT NULL
""").fetchone()

print(f"Features: {result[0]}, Average area: {result[1]:.2f}")
```

### Analysis with Polars

```python
import polars as pl

df = pl.read_parquet("converted.parquet")

# Fast aggregations
summary = (df
    .group_by("category")
    .agg([
        pl.count().alias("count"),
        pl.col("area").mean().alias("avg_area"),
        pl.col("area").sum().alias("total_area")
    ])
    .sort("count", descending=True)
)

print(summary)
```

This comprehensive guide should help you convert GDB files efficiently and handle various scenarios you might encounter. 