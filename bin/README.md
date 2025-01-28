# Documentation for bin scripts

## main.py

The `main.py` file collect all macros available to be used inside Mkdocs file (docs, themes, configuration). Available macros:

### def button(text, link)

Generates HTML code for a button that opens a link in a new window.

#### Args

* `text (str)`: The text to display on the button.
* `link (str)`: The URL to open when the button is clicked.

#### Returns

```html
<button onclick="window.open(\'{link}\')">{text}</button>
```

#### How to use

To be used inside `.md` files with following syntax: 

```markdown
{{ button('label', 'url') }}
```

### def image(src, alt, caption=None)

Generates HTML code for an image with an optional caption.

#### Args

* `src (str)`: The source URL of the image.
* `alt (str)`: The alt text for the image.
* `caption (str, optional)`: The caption for the image. Defaults to None.

#### Returns

```html
<figure>
  <img src="{src}" alt="{alt}">
  <figcaption class="caption">{caption}</figcaption>
</figure>
```

#### How to use

To be used inside `.md` files with following syntax: 

```markdown
{{ image('.media/image.png', 'alternative text', 'caption text') }}
```

### def youtube(src, caption=None)

Generates HTML code to embed a YouTube video.

#### Args

* `src (str)`: The source URL of the YouTube video.
* `caption (str, optional)`: The caption for the video. Defaults to None.

#### Returns

```html
<div class="embedded-video">
  <iframe src="{src}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen="true"></iframe>
  <a href="{src}">{caption}</a> <!-- if caption exists -->
</div>
```

#### How to use

To be used inside `.md` files with following syntax: 

```markdown
{{ youtube('https://youtube/abcde', 'caption text') }}
```

The caption text will act as a fallback link to the video.

### def video(src, caption=None)

Generates HTML code to embed a video.

#### Args

* `src (str)`: The source URL of the video.
* `caption (str, optional)`: The caption for the video. Defaults to None.

#### Returns

```html
<div class="video-container">
  <video controls="" style="width: 100%">
    <source src="{src}" type="video/mp4">
  </video>
  <a href="{src}">{caption}</a> <!-- if caption exists -->
</div>
```

#### How to use

To be used inside `.md` files with following syntax: 

```markdown
{{ video('./media/video.mp4', 'caption text') }}
```

The caption text will act as a fallback link to the video.

## def footnote_ref(number)

Generates HTML code for a footnote reference, linked to a footnote definition.

#### Args

* `number (int)`: The footnote number.

#### Returns

```html
<sup id="ref-{number}"><a href="#footnote-{number}">[{number}]</a></sup>
```

#### How to use

To be used inside `.md` files with following syntax: 

```markdown
referenced text{{ footnote_ref(2) }}
```

## def footnote_def(number)

Generates HTML code for a footnote definition, linked to a footnote reference.

#### Args

* `number (int)`: The footnote number.

#### Returns

```html
<span class="footnote-number" id="footnote-{number}"">[{number}]</span>
```

#### How to use

To be used inside `.md` files with following syntax: 

```markdown
{{ footnote_def(2) }}: Note 2 definition text
```

## def get_media_url()

> **To be tested.**

Retrieves the media URL from the environment configuration.

#### Returns

str: The media URL.

#### How to use

To be used inside `.md` files with following syntax: 

```markdown
{{ video('{{ get_media_url() }}/video.mp4', 'caption text') }}
```

## def list_contents(url)

> **To be tested.**

Lists the contents of a given directory.

#### Args

* `directory (str)`: The directory to list the contents of.

#### Returns

```html
<!-- for each .md file -->
<div class="expandable-content">
  <div class="expandable-trigger"></div>
  <!-- markdown content -->
</div>
```

#### How to use

To be used inside `.md` files with following syntax:

```markdown
{{ list_contents(docs/directory) }}
```

### def get_keys(value)

Retrieves the keys of the __dict__ attribute of a page object in MkDocs.
        
#### Args

* `value (object)`: The page object to retrieve the keys from.
        
#### Returns:

* list: A list of keys from the page object's `__dict__` attribute.

#### How to use

To be used inside `.md` files with following syntax:

```markdown
---
title: My Page Title
description: This is a description of my page.
author: John Doe
date: 2023-10-01
tags:
  - example
  - mkdocs
---

**filter**
{{ page | get_keys }}
```