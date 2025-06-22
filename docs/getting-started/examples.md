# Examples

This page provides practical examples for common ESRI Converter use cases. Each example includes both command-line and Python API approaches.

## Basic Conversion

### Single GDB File

=== "Command Line"
    ```bash
    esri-converter convert sample.gdb sample.parquet
    ```

=== "Python API"
    ```python
    from esri_converter import convert_gdb_to_parquet
    
    result = convert_gdb_to_parquet("sample.gdb", "sample.parquet")
    print(f"Converted {result['total_records']} records")
    ```

### With Custom Chunk Size

=== "Command Line"
    ```bash
    esri-converter convert large_dataset.gdb output.parquet --chunk-size 25000
    ```

=== "Python API"
    ```python
    result = convert_gdb_to_parquet(
        "large_dataset.gdb", 
        "output.parquet",
        chunk_size=25000
    )
    ```

## Layer Selection

### Convert Specific Layers

=== "Command Line"
    ```bash
    esri-converter convert municipal.gdb output.parquet \
        --layers Parcels Buildings Roads
    ```

=== "Python API"
    ```python
    result = convert_gdb_to_parquet(
        "municipal.gdb",
        "output.parquet", 
        layers=["Parcels", "Buildings", "Roads"]
    )
    ```

### Discover Available Layers

=== "Command Line"
    ```bash
    esri-converter info sample.gdb
    ```

=== "Python API"
    ```python
    from esri_converter import get_gdb_info
    
    info = get_gdb_info("sample.gdb")
    print("Available layers:")
    for layer in info['layers']:
        print(f"  - {layer['name']}: {layer['record_count']} records")
    ```

## Batch Processing

### Convert Multiple GDB Files

=== "Command Line"
    ```bash
    # Convert all GDB files in current directory
    esri-converter batch-convert *.gdb --output-dir ./converted/
    
    # Convert with custom settings
    esri-converter batch-convert *.gdb \
        --output-dir ./converted/ \
        --chunk-size 30000 \
        --parallel
    ```

=== "Python API"
    ```python
    from esri_converter import convert_multiple_gdbs
    import glob
    
    gdb_files = glob.glob("*.gdb")
    results = convert_multiple_gdbs(
        gdb_files,
        output_dir="./converted/",
        chunk_size=30000
    )
    
    for result in results:
        print(f"{result['gdb_name']}: {result['status']}")
    ```

### Directory Processing

=== "Python API"
    ```python
    from esri_converter import discover_gdb_files, convert_multiple_gdbs
    from pathlib import Path
    
    # Discover all GDB files recursively
    gdb_files = discover_gdb_files("./data/", recursive=True)
    print(f"Found {len(gdb_files)} GDB files")
    
    # Convert all discovered files
    results = convert_multiple_gdbs(
        gdb_files,
        output_dir="./converted/",
        chunk_size=20000
    )
    ```

## Advanced Usage

### Memory-Optimized Processing

For systems with limited memory:

=== "Command Line"
    ```bash
    esri-converter convert huge_dataset.gdb output.parquet \
        --chunk-size 5000 \
        --memory-limit 2GB
    ```

=== "Python API"
    ```python
    # Process very large files with minimal memory usage
    result = convert_gdb_to_parquet(
        "huge_dataset.gdb",
        "output.parquet",
        chunk_size=5000,
        streaming=True,
        memory_efficient=True
    )
    ```

### High-Performance Processing

For powerful machines:

=== "Command Line"
    ```bash
    esri-converter convert dataset.gdb output.parquet \
        --chunk-size 100000 \
        --parallel-chunks 4
    ```

=== "Python API"
    ```python
    # Maximize performance on powerful hardware
    result = convert_gdb_to_parquet(
        "dataset.gdb",
        "output.parquet", 
        chunk_size=100000,
        parallel_processing=True,
        max_workers=4
    )
    ```

## Integration Examples

### GeoPandas Workflow

```python
import geopandas as gpd
from esri_converter import convert_gdb_to_parquet

# Convert GDB to GeoParquet
convert_gdb_to_parquet("municipal.gdb", "municipal.parquet")

# Load with GeoPandas for analysis
gdf = gpd.read_parquet("municipal.parquet")

# Perform spatial analysis
buffered = gdf.buffer(100)  # 100-unit buffer
area_stats = gdf.groupby('zone_type')['area'].agg(['mean', 'sum'])

print(f"Loaded {len(gdf)} features")
print(area_stats)
```

### Polars High-Performance Analysis

```python
import polars as pl
from esri_converter import convert_gdb_to_parquet

# Convert and analyze with Polars
convert_gdb_to_parquet("sales_data.gdb", "sales_data.parquet")

# High-performance analysis
df = pl.read_parquet("sales_data.parquet")

# Fast aggregations
summary = (df
    .group_by("property_type")
    .agg([
        pl.col("sale_price").mean().alias("avg_price"),
        pl.col("sale_price").count().alias("total_sales"),
        pl.col("lot_size").median().alias("median_lot_size")
    ])
    .sort("avg_price", descending=True)
)

print(summary)
```

### DuckDB Spatial Queries

```python
import duckdb
from esri_converter import convert_gdb_to_parquet

# Convert GDB
convert_gdb_to_parquet("parcels.gdb", "parcels.parquet")

# Query with DuckDB
conn = duckdb.connect()

# Install spatial extension
conn.execute("INSTALL spatial; LOAD spatial;")

# Spatial queries on the converted data
result = conn.execute("""
    SELECT 
        zone_type,
        COUNT(*) as parcel_count,
        AVG(assessed_value) as avg_value,
        SUM(ST_Area(ST_GeomFromText(geometry_wkt))) as total_area
    FROM 'parcels.parquet'
    WHERE assessed_value > 100000
    GROUP BY zone_type
    ORDER BY avg_value DESC
""").fetchall()

for row in result:
    print(f"{row[0]}: {row[1]} parcels, avg ${row[2]:,.0f}")
```

## Real-World Scenarios

### Municipal Data Processing

```python
from esri_converter import convert_gdb_to_parquet
import polars as pl
from pathlib import Path

def process_municipal_data(gdb_path: str, output_dir: str):
    """Process municipal GDB files for analysis."""
    
    # Convert GDB to GeoParquet
    result = convert_gdb_to_parquet(
        gdb_path,
        f"{output_dir}/municipal.parquet",
        layers=["Parcels", "Buildings", "Zoning"],
        chunk_size=25000
    )
    
    # Load and process each layer
    parcels = pl.read_parquet(f"{output_dir}/parcels.parquet")
    buildings = pl.read_parquet(f"{output_dir}/buildings.parquet") 
    zoning = pl.read_parquet(f"{output_dir}/zoning.parquet")
    
    # Generate summary statistics
    parcel_summary = (parcels
        .group_by("zone_code")
        .agg([
            pl.col("assessed_value").mean().alias("avg_assessment"),
            pl.col("lot_area").sum().alias("total_area"),
            pl.count().alias("parcel_count")
        ])
    )
    
    return {
        'conversion_result': result,
        'parcel_summary': parcel_summary,
        'total_parcels': len(parcels),
        'total_buildings': len(buildings)
    }

# Usage
results = process_municipal_data("city_data.gdb", "./processed/")
print(f"Processed {results['total_parcels']} parcels and {results['total_buildings']} buildings")
```

### Environmental Data Pipeline

```python
from esri_converter import convert_multiple_gdbs, discover_gdb_files
import polars as pl
from datetime import datetime

def environmental_data_pipeline(data_dir: str):
    """Process environmental monitoring GDB files."""
    
    # Discover all environmental GDB files
    gdb_files = discover_gdb_files(data_dir, pattern="*environmental*.gdb")
    
    # Convert all files
    results = convert_multiple_gdbs(
        gdb_files,
        output_dir=f"{data_dir}/converted/",
        chunk_size=15000
    )
    
    # Combine all converted files for analysis
    all_data = []
    for result in results:
        if result['status'] == 'success':
            df = pl.read_parquet(result['output_path'])
            df = df.with_columns(
                pl.lit(result['gdb_name']).alias('source_file'),
                pl.lit(datetime.now()).alias('processed_date')
            )
            all_data.append(df)
    
    # Combine all data
    if all_data:
        combined = pl.concat(all_data)
        combined.write_parquet(f"{data_dir}/environmental_combined.parquet")
        
        return {
            'files_processed': len([r for r in results if r['status'] == 'success']),
            'total_records': len(combined),
            'date_range': (combined['sample_date'].min(), combined['sample_date'].max())
        }
    
    return {'files_processed': 0, 'total_records': 0}

# Usage
pipeline_results = environmental_data_pipeline("./environmental_data/")
print(f"Pipeline processed {pipeline_results['files_processed']} files")
```

### Data Quality Assessment

```python
from esri_converter import convert_gdb_to_parquet, get_gdb_info
import polars as pl

def assess_data_quality(gdb_path: str):
    """Assess data quality of GDB file before and after conversion."""
    
    # Get original GDB info
    original_info = get_gdb_info(gdb_path)
    
    # Convert to GeoParquet
    result = convert_gdb_to_parquet(gdb_path, "temp_output.parquet")
    
    # Load converted data for quality assessment
    df = pl.read_parquet("temp_output.parquet")
    
    # Quality metrics
    quality_report = {
        'original_records': original_info['total_records'],
        'converted_records': len(df),
        'data_integrity': len(df) == original_info['total_records'],
        'null_percentages': {},
        'geometry_validity': {}
    }
    
    # Check null percentages
    for col in df.columns:
        null_pct = (df[col].is_null().sum() / len(df)) * 100
        quality_report['null_percentages'][col] = null_pct
    
    # Check geometry validity (if geometry column exists)
    if 'geometry_wkt' in df.columns:
        valid_geoms = df.filter(pl.col('geometry_wkt').is_not_null()).height
        quality_report['geometry_validity'] = {
            'valid_geometries': valid_geoms,
            'invalid_geometries': len(df) - valid_geoms,
            'validity_percentage': (valid_geoms / len(df)) * 100
        }
    
    return quality_report

# Usage
quality = assess_data_quality("sample.gdb")
print(f"Data integrity: {'✅ PASSED' if quality['data_integrity'] else '❌ FAILED'}")
print(f"Geometry validity: {quality['geometry_validity']['validity_percentage']:.1f}%")
```

## Error Handling

### Robust Conversion with Retry Logic

```python
from esri_converter import convert_gdb_to_parquet
import time
import logging

def robust_convert(gdb_path: str, output_path: str, max_retries: int = 3):
    """Convert GDB with retry logic and error handling."""
    
    for attempt in range(max_retries):
        try:
            result = convert_gdb_to_parquet(
                gdb_path, 
                output_path,
                chunk_size=15000  # Conservative chunk size
            )
            
            if result['status'] == 'success':
                logging.info(f"Conversion successful on attempt {attempt + 1}")
                return result
                
        except MemoryError:
            logging.warning(f"Memory error on attempt {attempt + 1}, reducing chunk size")
            # Retry with smaller chunk size
            try:
                result = convert_gdb_to_parquet(
                    gdb_path, 
                    output_path,
                    chunk_size=5000  # Smaller chunks
                )
                return result
            except Exception as e:
                logging.error(f"Failed even with small chunks: {e}")
                
        except Exception as e:
            logging.error(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
            
    raise Exception(f"Failed to convert after {max_retries} attempts")

# Usage
try:
    result = robust_convert("problematic.gdb", "output.parquet")
    print("Conversion successful!")
except Exception as e:
    print(f"Conversion failed: {e}")
```

These examples demonstrate the flexibility and power of ESRI Converter across different use cases and integration scenarios. Choose the patterns that best fit your workflow and data processing needs. 