# Wiki Engine

A Docker-based documentation system combining MkDocs and Word document generation.

## Quick Start

Assume your wiki is in `/your_wiki` folder.
It's important to mount that folder in the `/wiki` docker folder.

### Use mkdocs

```bash
docker run -it --rm -u $(id -u):$(id -g) -v /your_wiki:/wiki wiki-engine mkdocs build -f /wiki/mkdocs.yml --site-dir /wiki/target/mkdocs
```

Your mkdocs output will be available at `target/mkdocs` folder.

### Build docx and html outputs

Build:
```bash
docker build -t wiki-engine .
```

Run:
```bash
docker run -it --rm -u $(id -u):$(id -g) -v /your_wiki:/wiki wiki-engine build
```

Your output will be available at `target/docx` and  `target/html` folders.

## Directory Structure of your wiki

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