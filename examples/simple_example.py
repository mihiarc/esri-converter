#!/usr/bin/env python3
"""
Simple Example: Basic usage of esri-converter

This script shows the simplest way to use the esri-converter package.
"""

import sys
import argparse
from pathlib import Path

# Add the parent directory to the path so we can import esri_converter
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import the main API functions
from esri_converter import convert_gdb_to_parquet, get_gdb_info


def simple_conversion(gdb_file, output_dir=None, chunk_size=15000):
    """Simple conversion example."""
    
    print(f"🗺️  Converting {gdb_file} to GeoParquet...")
    
    try:
        # Convert the GDB file
        result = convert_gdb_to_parquet(
            gdb_path=gdb_file,
            output_dir=output_dir,
            chunk_size=chunk_size
        )
        
        # Print results
        if result['success']:
            print(f"✅ Success! Converted {result['total_records']:,} records")
            print(f"📁 Output: {result['output_dir']}")
            print(f"💾 Size: {result['output_size_mb']:.1f} MB")
        else:
            print("❌ Conversion failed")
            
    except Exception as e:
        print(f"❌ Error: {e}")


def get_info_example(gdb_file):
    """Example of getting GDB information."""
    
    print(f"📊 Getting info for {gdb_file}...")
    
    try:
        info = get_gdb_info(gdb_file)
        
        print(f"📋 Layers: {info['total_layers']}")
        print(f"📊 Records: {info['total_records']:,}")
        
        for layer in info['layers']:
            print(f"  • {layer['name']}: {layer['record_count']:,} records")
            
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    print("🚀 ESRI Converter - Simple Examples")
    print("=" * 40)
    
    # Example 1: Get GDB info
    print("\n1️⃣  Getting GDB Information:")
    get_info_example()
    
    # Example 2: Convert GDB
    print("\n2️⃣  Converting GDB:")
    simple_conversion()
    
    print("\n✨ Done!") 