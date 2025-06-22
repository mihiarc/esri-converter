# ESRI Converter Examples

This directory contains example scripts demonstrating how to use the esri-converter package.

## 📁 Files

### `convert_sf_premium_nc.py`
Comprehensive example that converts the SF_Premium_NC.gdb file to GeoParquet format with:
- Detailed progress tracking
- Error handling
- GDB analysis before conversion
- Confirmation prompts for large datasets
- Detailed results reporting

### `simple_example.py`
Simple, minimal example showing basic usage of the API functions.

## 🚀 Usage

### Run the SF Premium NC Conversion

```bash
# From the root directory (where SF_Premium_NC.gdb is located)
python examples/convert_sf_premium_nc.py

# Or just get info about the GDB without converting
python examples/convert_sf_premium_nc.py --info
```

### Run the Simple Example

```bash
# From the root directory
python examples/simple_example.py
```

## 📋 Prerequisites

1. Make sure you have the esri-converter package installed or the source code available
2. Ensure the GDB files (like `SF_Premium_NC.gdb`) are in the root directory
3. Have the required dependencies installed:
   ```bash
   uv add polars fiona shapely pyarrow rich psutil tqdm
   ```

## 📊 Expected Output

The conversion will create a `geoparquet_output/` directory with:
- `SF_Premium_NC/` subdirectory
- Individual `.parquet` files for each layer
- Compressed, optimized geospatial data

Example output structure:
```
geoparquet_output/
└── SF_Premium_NC/
    ├── OrphanAssessments.parquet
    └── ParcelsWithAssessments.parquet
```

## ⚡ Performance Tips

- **Chunk Size**: Adjust the `chunk_size` parameter based on available memory
  - Small systems: 5,000 - 10,000
  - Medium systems: 15,000 (default)
  - Large systems: 25,000+

- **Memory**: The converter uses streaming processing, so it can handle files larger than available RAM

- **Storage**: Output files are typically 20-40% the size of the original GDB due to compression

## 🔧 Customization

You can modify the examples to:
- Change output directories
- Convert specific layers only
- Adjust chunk sizes
- Add custom logging
- Handle different GDB files

Example customization:
```python
result = convert_gdb_to_parquet(
    gdb_path="your_file.gdb",
    output_dir="custom_output/",
    layers=["specific_layer"],
    chunk_size=10000,
    log_file="custom.log"
)
``` 