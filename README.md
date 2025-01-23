# Wiki Engine

A Docker-based documentation system combining MkDocs and Word document generation.

## Quick Start

Build:
```bash
docker build -t wiki-engine .
```

Run:
```bash
docker run -it --rm -u $(id -u):$(id -g) \
  -v /your_wiki:/wiki \
  wiki-engine build
```

## Directory Structure
```
/your_wiki/
├── docs/          # Markdown files
├── fonts/         # Custom fonts
├── templates/     # Word templates
├── theme/         # Website theme
├── mkdocs.yml     # MkDocs configuration
└── target/        # Build output
    ├── docx/      # Generated Word documents
    └── html/      # Generated website
```

## Features

- Generates both website and Word documentation
- Supports custom fonts and themes
- Preserves user permissions with proper UID/GID mapping
- Converts markdown to HTML and DOCX formats
- Uses EFSA Word template styles

## Prerequisites

- Docker
- Write permissions in the wiki directory