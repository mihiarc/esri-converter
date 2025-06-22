#!/usr/bin/env python3
"""
Example: Convert SF_Premium_NC.gdb to GeoParquet

This script demonstrates how to use the esri-converter package to convert
a large ESRI File Geodatabase to GeoParquet format with proper error handling
and progress tracking.
"""

import sys
import argparse
from pathlib import Path
import time

# Add the parent directory to the path so we can import esri_converter
sys.path.insert(0, str(Path(__file__).parent.parent))

from esri_converter.api import (
    convert_gdb_to_parquet,
    get_gdb_info,
    discover_gdb_files
)
from esri_converter.exceptions import (
    ValidationError,
    ConversionError,
    ESRIConverterError
)


def main(gdb_path=None, output_dir=None, chunk_size=15000):
    """Main conversion function with comprehensive error handling."""
    
    print("🗺️  ESRI Converter - GDB to Parquet Example")
    print("=" * 50)
    
    # Use provided path or default
    if gdb_path is None:
        gdb_path = Path("SF_Premium_NC.gdb")
    else:
        gdb_path = Path(gdb_path)
    
    # Use provided output directory or default
    if output_dir is None:
        output_dir = "geoparquet_output"
    
    # Show configuration
    print(f"📁 Input GDB: {gdb_path}")
    print(f"📂 Output Dir: {output_dir}")
    print(f"📦 Chunk Size: {chunk_size:,}")
    
    # Check if the GDB file exists
    if not gdb_path.exists():
        print(f"❌ Error: GDB file not found: {gdb_path}")
        print(f"   Make sure {gdb_path.name} exists in the specified location.")
        return 1
    
    try:
        # Step 1: Get information about the GDB
        print("\n📊 Analyzing GDB file...")
        info = get_gdb_info(gdb_path)
        
        print(f"✅ GDB Analysis Complete:")
        print(f"   📁 File: {info['gdb_path']}")
        print(f"   📋 Layers: {info['total_layers']}")
        print(f"   📊 Total Records: {info['total_records']:,}")
        
        # Show layer details
        print(f"\n📋 Layer Details:")
        for layer in info['layers']:
            print(f"   • {layer['name']}: {layer['record_count']:,} records ({layer['geometry_type']})")
        
        # Step 2: Estimate processing time
        estimated_time = info['total_records'] / 15000  # Rough estimate at 15K records/sec
        print(f"\n⏱️  Estimated processing time: {estimated_time:.1f} seconds")
        
        # Step 3: Ask for confirmation for large datasets
        if info['total_records'] > 1000000:
            print(f"\n⚠️  Large dataset detected ({info['total_records']:,} records)")
            response = input("   Continue with conversion? (y/N): ")
            if response.lower() != 'y':
                print("   Conversion cancelled.")
                return 0
        
        # Step 4: Perform the conversion
        print(f"\n🚀 Starting conversion...")
        start_time = time.time()
        
        result = convert_gdb_to_parquet(
            gdb_path=gdb_path,
            output_dir=output_dir,
            chunk_size=chunk_size,
            show_progress=True,
            log_file="conversion.log"
        )
        
        # Step 5: Display results
        elapsed_time = time.time() - start_time
        
        if result['success']:
            print(f"\n🎉 Conversion Successful!")
            print(f"   ✅ Layers converted: {len(result['layers_converted'])}")
            print(f"   📊 Total records: {result['total_records']:,}")
            print(f"   ⏱️  Processing time: {result['total_time']:.2f} seconds")
            print(f"   ⚡ Processing rate: {result['processing_rate']:,.0f} records/sec")
            print(f"   💾 Output size: {result['output_size_mb']:.1f} MB")
            print(f"   📁 Output directory: {result['output_dir']}")
            
            # Show individual layer results
            print(f"\n📋 Layer Results:")
            for layer in result['layers_converted']:
                output_file = Path(layer['output_file'])
                file_size = output_file.stat().st_size / (1024 * 1024) if output_file.exists() else 0
                print(f"   • {layer['layer']}: {layer['record_count']:,} records → {file_size:.1f} MB")
            
            # Show failed layers if any
            if result['layers_failed']:
                print(f"\n❌ Failed Layers:")
                for layer in result['layers_failed']:
                    print(f"   • {layer}")
        else:
            print(f"\n❌ Conversion Failed!")
            if result['layers_failed']:
                print(f"   Failed layers: {result['layers_failed']}")
        
        # Step 6: Show output file structure
        output_dir = Path(result['output_dir'])
        if output_dir.exists():
            print(f"\n📂 Output Files:")
            for parquet_file in sorted(output_dir.glob("*.parquet")):
                size_mb = parquet_file.stat().st_size / (1024 * 1024)
                print(f"   📄 {parquet_file.name} ({size_mb:.1f} MB)")
        
        return 0 if result['success'] else 1
        
    except ValidationError as e:
        print(f"\n❌ Validation Error: {e}")
        print("   Please check your input parameters.")
        return 1
        
    except ConversionError as e:
        print(f"\n❌ Conversion Error: {e}")
        if hasattr(e, 'source_file'):
            print(f"   Source file: {e.source_file}")
        if hasattr(e, 'layer_name'):
            print(f"   Layer: {e.layer_name}")
        return 1
        
    except ESRIConverterError as e:
        print(f"\n❌ ESRI Converter Error: {e}")
        return 1
        
    except Exception as e:
        print(f"\n💥 Unexpected Error: {e}")
        print("   Please check the logs for more details.")
        return 1


def quick_info(gdb_path=None):
    """Quick function to just show GDB information without converting."""
    
    if gdb_path is None:
        gdb_path = Path("SF_Premium_NC.gdb")
    else:
        gdb_path = Path(gdb_path)
    
    if not gdb_path.exists():
        print(f"❌ GDB file not found: {gdb_path}")
        return
    
    try:
        info = get_gdb_info(gdb_path)
        
        print(f"📊 GDB Information:")
        print(f"   File: {info['gdb_path']}")
        print(f"   Layers: {info['total_layers']}")
        print(f"   Total Records: {info['total_records']:,}")
        
        for layer in info['layers']:
            bounds_str = ""
            if layer.get('bounds'):
                bounds = layer['bounds']
                bounds_str = f" | Bounds: ({bounds[0]:.2f}, {bounds[1]:.2f}, {bounds[2]:.2f}, {bounds[3]:.2f})"
            
            print(f"   • {layer['name']}: {layer['record_count']:,} {layer['geometry_type']} | {layer['field_count']} fields | CRS: {layer['crs']}{bounds_str}")
            
    except Exception as e:
        print(f"❌ Error getting GDB info: {e}")


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Convert ESRI File Geodatabase (GDB) to GeoParquet format",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert SF_Premium_NC.gdb with default settings
  python convert_sf_premium_nc.py
  
  # Convert a different GDB file
  python convert_sf_premium_nc.py -i "MyData.gdb"
  
  # Convert with custom output directory and chunk size
  python convert_sf_premium_nc.py -i "data.gdb" -o "my_output" -c 10000
  
  # Just get information about a GDB file
  python convert_sf_premium_nc.py -i "data.gdb" --info
        """
    )
    
    parser.add_argument(
        "-i", "--input",
        type=str,
        default="SF_Premium_NC.gdb",
        help="Input GDB file path (default: SF_Premium_NC.gdb)"
    )
    
    parser.add_argument(
        "-o", "--output",
        type=str,
        default="geoparquet_output",
        help="Output directory path (default: geoparquet_output)"
    )
    
    parser.add_argument(
        "-c", "--chunk-size",
        type=int,
        default=15000,
        help="Chunk size for processing records (default: 15000)"
    )
    
    parser.add_argument(
        "--info",
        action="store_true",
        help="Show GDB information without converting"
    )
    
    return parser.parse_args()


if __name__ == "__main__":
    # Parse command line arguments
    args = parse_arguments()
    
    # Validate chunk size
    if args.chunk_size <= 0:
        print("❌ Error: Chunk size must be positive")
        sys.exit(1)
    
    if args.chunk_size > 100000:
        print("⚠️  Warning: Very large chunk size may cause memory issues")
        response = input("Continue? (y/N): ")
        if response.lower() != 'y':
            print("Cancelled.")
            sys.exit(0)
    
    # Run the appropriate function
    if args.info:
        quick_info(args.input)
    else:
        exit_code = main(
            gdb_path=args.input,
            output_dir=args.output,
            chunk_size=args.chunk_size
        )
        sys.exit(exit_code) 