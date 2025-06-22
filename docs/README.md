# ESRI Converter Documentation

This directory contains the complete documentation for the ESRI Converter project, built with MkDocs and Material theme.

## Documentation Structure

```
docs/
├── index.md                    # Homepage
├── getting-started/            # Getting started guides
│   ├── installation.md
│   ├── quickstart.md
│   └── examples.md
├── user-guide/                 # User guides
│   ├── converting.md
│   ├── cli.md
│   ├── batch.md
│   └── performance.md
├── development/                # Developer documentation
│   ├── contributing.md
│   ├── architecture.md
│   └── testing.md
├── changelog.md               # Version history
├── stylesheets/               # Custom CSS
│   └── extra.css
└── gen_ref_pages.py          # API reference generator
```

## Building Documentation

### Prerequisites

Install documentation dependencies:

```bash
uv pip install mkdocs mkdocs-material mkdocs-mermaid2-plugin "mkdocstrings[python]" mkdocs-gen-files mkdocs-literate-nav mkdocs-section-index
```

### Local Development

Serve documentation locally with hot reload:

```bash
mkdocs serve
```

The documentation will be available at http://127.0.0.1:8000

### Building Static Site

Build the static documentation:

```bash
mkdocs build
```

The built site will be in the `site/` directory.

## Contributing to Documentation

### Writing Guidelines

1. **Clear and Concise**: Write in simple, clear language
2. **Code Examples**: Include working code examples
3. **Screenshots**: Add screenshots for UI-related features
4. **Cross-references**: Link between related sections
5. **Testing**: Test all code examples before committing

### Markdown Features

The documentation supports:

- **Admonitions**: !!! note, !!! warning, !!! tip
- **Code Blocks**: With syntax highlighting
- **Mermaid Diagrams**: For flowcharts and diagrams
- **Tabbed Content**: === "Tab Name"
- **API Documentation**: Auto-generated from docstrings

### Adding New Pages

1. Create the markdown file in the appropriate directory
2. Add it to the `nav` section in `mkdocs.yml`
3. Test locally with `mkdocs serve`
4. Submit a pull request

### Style Guide

- Use sentence case for headings
- Include code examples for all features
- Add screenshots for visual features
- Use consistent terminology throughout
- Link to related sections

## Deployment

Documentation is automatically deployed to GitHub Pages when changes are pushed to the main branch via GitHub Actions workflow (`.github/workflows/docs.yml`).

## API Reference

API documentation is automatically generated from Python docstrings using mkdocstrings. The generation script is in `gen_ref_pages.py`.

## Feedback

For documentation feedback:
- Open an issue on GitHub
- Submit a pull request with improvements
- Discuss in GitHub Discussions 