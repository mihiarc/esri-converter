#!/usr/bin/env python3
"""
Documentation development helper script.

This script provides convenient commands for working with the MkDocs documentation.
"""

import subprocess
import sys
import argparse
from pathlib import Path

def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed")
        print(f"Error: {e.stderr}")
        return False

def install_deps():
    """Install documentation dependencies."""
    cmd = 'uv pip install mkdocs mkdocs-material mkdocs-mermaid2-plugin "mkdocstrings[python]" mkdocs-gen-files mkdocs-literate-nav mkdocs-section-index'
    return run_command(cmd, "Installing documentation dependencies")

def serve_docs(host="127.0.0.1", port=8000):
    """Serve documentation locally."""
    cmd = f"mkdocs serve --dev-addr {host}:{port}"
    print(f"🚀 Starting documentation server at http://{host}:{port}")
    print("Press Ctrl+C to stop the server")
    try:
        subprocess.run(cmd, shell=True, check=True)
    except KeyboardInterrupt:
        print("\n👋 Documentation server stopped")

def build_docs():
    """Build static documentation."""
    return run_command("mkdocs build --strict", "Building documentation")

def clean_docs():
    """Clean build artifacts."""
    site_dir = Path("site")
    if site_dir.exists():
        import shutil
        shutil.rmtree(site_dir)
        print("🧹 Cleaned build artifacts")
    else:
        print("🧹 No build artifacts to clean")

def check_links():
    """Check for broken links in documentation."""
    # This would require additional tools like linkchecker
    print("🔍 Link checking not implemented yet")
    print("Consider using: pip install linkchecker && linkchecker http://localhost:8000")

def validate_docs():
    """Validate documentation structure and content."""
    print("🔍 Validating documentation...")
    
    # Check if all required files exist
    required_files = [
        "docs/index.md",
        "docs/getting-started/installation.md",
        "docs/getting-started/quickstart.md",
        "docs/user-guide/converting.md",
        "docs/development/contributing.md",
        "mkdocs.yml"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing required files:")
        for file_path in missing_files:
            print(f"  - {file_path}")
        return False
    
    # Try building docs to check for errors
    if build_docs():
        print("✅ Documentation validation passed")
        return True
    else:
        print("❌ Documentation validation failed")
        return False

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="ESRI Converter documentation development helper",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/docs.py serve           # Serve docs locally
  python scripts/docs.py build          # Build static docs
  python scripts/docs.py install        # Install dependencies
  python scripts/docs.py validate       # Validate docs structure
        """
    )
    
    parser.add_argument(
        "command",
        choices=["install", "serve", "build", "clean", "validate", "check-links"],
        help="Command to run"
    )
    
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host for serve command (default: 127.0.0.1)"
    )
    
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port for serve command (default: 8000)"
    )
    
    args = parser.parse_args()
    
    # Change to project root
    project_root = Path(__file__).parent.parent
    import os
    os.chdir(project_root)
    
    if args.command == "install":
        success = install_deps()
    elif args.command == "serve":
        serve_docs(args.host, args.port)
        success = True
    elif args.command == "build":
        success = build_docs()
    elif args.command == "clean":
        clean_docs()
        success = True
    elif args.command == "validate":
        success = validate_docs()
    elif args.command == "check-links":
        check_links()
        success = True
    else:
        parser.print_help()
        success = False
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 