#!/usr/bin/env python3
"""
Publishing script for esri-converter package.

This script handles building and uploading the package to PyPI (test and live).
It uses environment variables for secure credential management.
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def run_command(cmd, check=True):
    """Run a shell command and return the result."""
    print(f"🔧 Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    
    if check and result.returncode != 0:
        print(f"❌ Command failed with exit code {result.returncode}")
        sys.exit(1)
    
    return result

def clean_build():
    """Clean previous build artifacts."""
    print("🧹 Cleaning build artifacts...")
    
    # Remove build directories
    for dir_name in ['build', 'dist', '*.egg-info']:
        run_command(f"rm -rf {dir_name}", check=False)
    
    # Remove __pycache__ directories
    run_command("find . -type d -name '__pycache__' -exec rm -rf {} +", check=False)
    
    print("✅ Build artifacts cleaned")

def build_package():
    """Build the package."""
    print("📦 Building package...")
    
    # Build the package (dependencies should already be installed)
    run_command("uv run python -m build")
    
    print("✅ Package built successfully")

def check_package():
    """Check the built package."""
    print("🔍 Checking package...")
    
    # Check with twine
    run_command("uv run python -m twine check dist/*")
    
    print("✅ Package check passed")

def publish_to_test():
    """Publish to TestPyPI."""
    print("🚀 Publishing to TestPyPI...")
    
    # Get credentials from environment
    token = os.getenv('PYPI_TEST_TOKEN')
    if not token:
        print("❌ PYPI_TEST_TOKEN not found in environment variables")
        print("   Please set your TestPyPI token in .env file")
        sys.exit(1)
    
    # Upload to TestPyPI
    run_command(f"uv run python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/* -u __token__ -p {token}")
    
    print("✅ Published to TestPyPI successfully")
    print("🔗 Check your package at: https://test.pypi.org/project/esri-converter/")

def publish_to_live():
    """Publish to live PyPI."""
    print("🚀 Publishing to PyPI (LIVE)...")
    
    # Get credentials from environment
    token = os.getenv('PYPI_LIVE_TOKEN')
    if not token:
        print("❌ PYPI_LIVE_TOKEN not found in environment variables")
        print("   Please set your PyPI token in .env file")
        sys.exit(1)
    
    # Confirmation for live publishing
    package_name = os.getenv('PACKAGE_NAME', 'esri-converter')
    package_version = os.getenv('PACKAGE_VERSION', '1.0.0')
    
    print(f"⚠️  About to publish {package_name} v{package_version} to LIVE PyPI")
    response = input("   Are you absolutely sure? (type 'YES' to confirm): ")
    
    if response != 'YES':
        print("❌ Publishing cancelled")
        sys.exit(0)
    
    # Upload to PyPI
    run_command(f"uv run python -m twine upload dist/* -u __token__ -p {token}")
    
    print("✅ Published to PyPI successfully")
    print(f"🔗 Check your package at: https://pypi.org/project/{package_name}/")

def install_test():
    """Test installation from TestPyPI."""
    print("🧪 Testing installation from TestPyPI...")
    
    package_name = os.getenv('PACKAGE_NAME', 'esri-converter')
    
    # Try to install from TestPyPI
    run_command(f"uv add --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ {package_name}")
    
    print("✅ Test installation successful")

def main():
    """Main publishing workflow."""
    parser = argparse.ArgumentParser(description="Publish esri-converter package")
    parser.add_argument('action', choices=['clean', 'build', 'check', 'test', 'live', 'install-test', 'full-test', 'full-live'], 
                       help='Action to perform')
    
    args = parser.parse_args()
    
    # Check if .env file exists
    if not Path('.env').exists():
        print("⚠️  No .env file found. Please create one from env.template")
        print("   cp env.template .env")
        print("   # Then edit .env with your actual API tokens")
        if args.action in ['test', 'live', 'full-test', 'full-live']:
            sys.exit(1)
    
    print("🚀 ESRI Converter Publishing Script")
    print("=" * 50)
    
    if args.action == 'clean':
        clean_build()
    
    elif args.action == 'build':
        build_package()
    
    elif args.action == 'check':
        check_package()
    
    elif args.action == 'test':
        publish_to_test()
    
    elif args.action == 'live':
        publish_to_live()
    
    elif args.action == 'install-test':
        install_test()
    
    elif args.action == 'full-test':
        clean_build()
        build_package()
        check_package()
        publish_to_test()
        print("\n🎉 Full test publishing workflow completed!")
        print("   You can now test install with: python scripts/publish.py install-test")
    
    elif args.action == 'full-live':
        clean_build()
        build_package()
        check_package()
        publish_to_live()
        print("\n🎉 Full live publishing workflow completed!")
        print(f"   Your package is now available at: https://pypi.org/project/{os.getenv('PACKAGE_NAME', 'esri-converter')}/")

if __name__ == "__main__":
    main() 