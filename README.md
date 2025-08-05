# Wiki Engine

A Docker-based documentation system combining MkDocs and Word document generation.

## Quick Start

Assume your wiki is in `/your_wiki` folder.

> **Important:** It's crucial to mount that folder in the `/wiki` docker folder.

### Build the docker image

#### Cloning the repo

```bash
git clone https://github.com/genpat-it/wiki-engine
cd wiki-engine
docker build -t wiki-engine .
```

#### Using the GitHub Registry

```bash
docker pull ghcr.io/genpat-it/wiki-engine:latest
docker tag ghcr.io/genpat-it/wiki-engine wiki-engine
```

#### Windows Users

For Windows users, it is **recommended to use PowerShell** when running Docker commands. PowerShell provides a more consistent environment for managing Docker, especially when working with paths and volume mounts.

### Use mkdocs

```bash
docker run -it --rm -v /your_wiki:/wiki wiki-engine mkdocs build -f /wiki/mkdocs.yml --site-dir /wiki/target/mkdocs
```

Your mkdocs output will be available at `/your_wiki/target/mkdocs` folder.

### Build docx and html outputs

Run:
```bash
docker run -it --rm -u $(id -u):$(id -g) -v /your_wiki:/wiki wiki-engine build-docx
```

Your output will be available at `/your_wiki/target/docx` and  `/your_wiki/target/html` folders.

#### Advanced Usage

##### Specify a Custom Docs Directory

To use a different directory for your markdown files (instead of the default `docs`), add the `--docs-dir` option:

```bash
docker run -it --rm -u $(id -u):$(id -g) -v /your_wiki:/wiki wiki-engine build-docx --docs-dir /path/accessible/from/docker/image/docs
```

##### Set a Custom Index File

To use a specific file as your index (instead of the default `index.md`), use the `--index-file` option:

```bash
docker run -it --rm -u $(id -u):$(id -g) -v /your_wiki:/wiki wiki-engine build-docx --index-file home.md
```

> **Note:** The index file must be located at the root of the specified docs directory.

##### Use a Custom Word Template

To apply a custom Word template, provide the template path with the `--template` option:

```bash
# The template file must be accessible from within the Docker image
docker run -it --rm -u $(id -u):$(id -g) -v /your_wiki:/wiki wiki-engine build-docx --template /template/path/accessible/from/docker/image
```

### Build EFSA compatible docx

Run:
```bash
docker run -it --rm -u $(id -u):$(id -g) -v /your_wiki:/wiki wiki-engine build-docx --efsa 
```

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
  
## Prerequisites

- Docker
- Write permissions in the wiki directory