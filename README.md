Here's an improved and polished version of your README:

---

# **Wiki Engine**

A lightweight Docker-based documentation system that combines **MkDocs** for website generation with tools to create Word documents from Markdown.

## **Quick Start**

### **Build the Docker Image**
First, build the Docker image for the Wiki Engine:
```bash
docker build -t wiki-engine .
```

### **Use MkDocs**
To generate a static website from your Markdown files, use the following command. Make sure to replace `/your_wiki` with the path to your wiki directory:
```bash
docker run -it --rm -u $(id -u):$(id -g) \
  -v /your_wiki:/wiki \
  wiki-engine mkdocs build -f /wiki/mkdocs.yml --site-dir /wiki/target/mkdocs
```

Your MkDocs-generated website will be available in the `target/mkdocs` folder.

### **Build DOCX and HTML Outputs**
To generate both Word documents and HTML files:
```bash
docker run -it --rm -u $(id -u):$(id -g) \
  -v /your_wiki:/wiki \
  wiki-engine build
```

## **Directory Structure**

Organize your wiki content in the following structure for best results:

```
/your_wiki/
├── docs/          # Markdown source files
├── fonts/         # Custom fonts for Word documents
├── templates/     # Word templates for styling
├── theme/         # Custom website themes
├── mkdocs.yml     # MkDocs configuration file
└── target/        # Output directory for builds
    ├── docx/      # Generated Word documents
    └── html/      # Generated static website
```

## **Features**

- **Dual Output**: Generates both a static website and Word documents from your Markdown files.
- **Customizable**:
  - Use your own fonts for Word documents.
  - Apply custom themes for the website.
- **Preserves User Permissions**: Maps UID/GID to ensure files match your local user.
- **Flexible Formats**:
  - Converts Markdown to **HTML** for websites.
  - Converts Markdown to **DOCX** using EFSA Word template styles.
- **Fast and Lightweight**: Docker-based setup simplifies dependencies and environment management.

## **Prerequisites**

To use Wiki Engine, ensure the following are installed on your system:
- **Docker**: To run the containerized engine.
- **Write Permissions**: The `/your_wiki` directory must allow read and write access.

## **Usage Notes**
- The `-u $(id -u):$(id -g)` flag ensures that generated files match the user and group of the host system.
- Mounting `/your_wiki` ensures your content is processed and outputs are stored in the correct location.

## **Contributing**

We welcome contributions! Please submit pull requests or file issues on our [GitHub repository](#).

## **License**

This project is licensed under the [MIT License](LICENSE).