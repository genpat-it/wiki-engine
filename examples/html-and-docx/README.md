# EFSA WGS System, User manual

## Quick Start Guide

### Pull the wiki-engine

```
docker pull ghcr.io/genpat-it/wiki-engine:latest
docker tag ghcr.io/genpat-it/wiki-engine wiki-engine
```

### Build mkdocs

```
docker run -it --rm -u $(id -u):$(id -g) -v $(pwd):/wiki wiki-engine mkdocs build -f /wiki/mkdocs.yml --site-dir /wiki/target/mkdocs
```

The output of MkDocs will be available in the `/your_wiki/target/mkdocs` folder.

### Build docx

```
docker run -it --rm -u $(id -u):$(id -g) -v $(pwd):/wiki wiki-engine build
```

The generated `docx` output will be located in the `/your_wiki/target/docx`.

## Prerequisites

- Docker
- Write permissions in the wiki directory
- [Getting started with MkDocs](https://www.mkdocs.org/getting-started/#getting-started-with-mkdocs)

## Directory Structure of your wiki

```
/your_wiki/
├── docs/          # Markdown files
    ├── media/     # Media files
├── fonts/         # Custom fonts
├── templates/     # Word templates
├── theme/         # Website theme
├── mkdocs.yml     # MkDocs configuration
└── target/        # Build output
    ├── docx/      # Generated Word documents
    └── html/      # Generated website
```

### docs

The `docs` folder contains the `.md` files necessary for building both the docx and the `mkdocs`. The `index.md` file is required and represents the entry page of the site and simultaneously the first topic shown in the `docx`.

In this specific use case, an explicit navigation menu is not used, so the order of presentation of the topics is given by the name of the `.md` files (ascending alphabetical order). In any case, the `wiki-engine` to build the docx, recursively scans the folder concatenating the files it finds inside according to the name order.

> **Please note** if a `media` folder exists, the `wiki-engine` will copy it as is. If not, the `wiki-engine` will parse the `docs` folder to collect video and image resources and make them available to build docx

### fonts

The `fonts` folder contains fonts we want to use to build `pdf` from mkdocs. Fonts file should be in `.ttf` format.

### templates

The `templates` folder contains resources needed to build `docx`:

* `intro.md`, optional, contains contents for the first page of the document, the file name cannot be changed.
* `template.docx`, optional, is the word template to apply to the `docx`, the file name cannot be changed.

### theme

The `theme` folder is optional, it contains the theme to be used for the site layout. It is referenced by the `mkdocs.yml` configuration file of `mkdocs`.

For more information on using `mkdocs` themes, you can refer to the [official documentation](https://www.mkdocs.org/getting-started/#theming-our-documentation).

### mkdocs.yml

`mkdocs` configuration file, mandatory.

### target

The `target` folder hosts output generated files.

## Writing docs

Before starting writing or edit docs, please have a look to Mkdocs user guide on how [writing your docs](https://www.mkdocs.org/user-guide/writing-your-docs/).

### Title and toc

> The **h1** is reserved only for the page title

The contents menu (on the right), will index only heading of second level and optionally third level, by changing `toc_depth: "2"` in `toc_depth: "2-3"` inside `.yml` configuration file:

`## Title` and or optionally `### Title`

### Notes and highlights

By using the blockquote notation, the theme will highlight the box with a light background.

```
> **N.B.**
>
> Lorem ipsum
```

### Use image title as caption

If you need to use a caption for images, you can use the markdown image title sintax:

`![](./media/image.png "image title")`

> *Please note:* you should always use the `/` symbol to indicate the file name as a path otherwise mkdocs does not will recognize the sintax.

Alternatvely see [macros](#macros) section on how to add images.

### Use icons inline

To use icons inline inside the contents, please add the alt attribute `inline-icon`

```
![inline-icon](./media/image.png)
```

### Use diagram as images

To use diagram inside the contents as images, please add the alt attribute `diagram` to avoid box shadow.

```
![diagram](./media/image.png)
```

### Highlight code

To highlight the code, add the proper programming language definition:

~~~
```python
def fn():
    pass
```
~~~

or

```
~~~python
def fn():
    pass
~~~
```

## Macros

Following macros extend markdown basic syntax, just add them inside your `.md` files.

### Add footnotes

* **Footnote reference:** `{{ footnote_ref(n) }}`, for instance `Agreement{{ footnote_ref(2) }}`
* **Footnote definition:** `{{ footnote_def(n) }}`, for instance `{{ footnote_def(2) }}: Note 2 text`

> **IMPORTANT**
> macros plugin looks for `{}`, please use html notation to use curly braces in docs `&#123;`

### Add videos

#### File

```
{{ video('./media/your-video.mp4', 'caption') }}
```

#### Youtube

```
{{ youtube('https://www.youtube-nocookie.com/embed/EngW7tLk6R8?rel=0&wmode=transparent&autoplay=0', 'caption') }}
```

## Features

- Generates both website and Word documentation
- Supports custom fonts and themes
- Preserves user permissions with proper UID/GID mapping
- Converts markdown to HTML and DOCX formats

## Tips

To see changes in real time while writing your docs, you can use the following command in the terminal:

```
docker run -it --rm -u $(id -u):$(id -g) -v $(pwd):/wiki -p 8001:8000 wiki-engine mkdocs serve -f /wiki/mkdocs.yml --dev-addr=0.0.0.0:8000
```

Open following address to the browser `http://0.0.0.0:8001/efsa_wgs_system_wiki/`

> **Please note:** The port to open depends on the `-p 8001:8000` parameter. In this case, you should use `http://0.0.0.0:8001/`

## Resources

* [Wiki Engine](https://github.com/genpat-it/wiki-engine)
* [MkDocs](https://www.mkdocs.org/)
* [Pandoc](https://pandoc.org/)
