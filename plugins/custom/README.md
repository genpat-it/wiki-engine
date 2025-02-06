# Custom plugins documentation

## Journal Plugin (mkdocs_journal_plugin)

The `JournalPlugin` is a custom MkDocs plugin that allows you to create a journal section in your documentation. It supports pagination and metadata extraction from Markdown files.

### Configuration

To configure the `JournalPlugin`, add it to the `plugins` section of your `mkdocs.yml` file with the following options:

```yaml
plugins:
  - journal_plugin:
      directory: 'journal'
      items_per_page: 4
```

#### Options

* `directory`: The directory inside `docs` that contains the journal entries. Default is `journal`.
* `items_per_page`: The number of articles listed on each page. Default is `5`.

### Usage

Place your journal entries in the specified directory (e.g., `docs/journal`). Each entry should be a Markdown file with optional front matter for metadata.

**Example Journal Entry**
```yaml
---
title: "My Journal Entry"
date: "2023-10-01"
thumbnail: "path/to/thumbnail.jpg"
---

This is the content of my journal entry.
```

The plugin will automatically collect and paginate the journal entries (sorted by date in descending order) based on the configuration.

The entries are made available as a JSON-like parameter in the `config.items_per_page`. For example, you can access it in a theme like this:

```html
{% if journal_files %}
  <div id="journal-files-json">
    {{ journal_files | tojson }}
  </div>
{% endif %}

<script>
  const journalFilesNode = document.querySelector('#journal-files-json');
  // Retrieves data
  const journalFiles = journalFilesNode ? JSON.parse(journalFilesNode.innerHTML) : undefined;
</script>
```

## List Subfolders Plugin (mkdocs_list_subfolders_plugin)

The `ListSubfoldersPlugin` is a custom MkDocs plugin that lists subcategories starting from subfolders contained by a defined directory.

### Configuration

To configure the `ListSubfoldersPlugin`, add it to the `plugins` section of your `mkdocs.yml` file with the following options:

```yaml
plugins:
  - list_subfolders_plugin:
      folder_path: 'journal'
```

#### Options

* `folder_path`: The directory inside `docs` that contains the subfolders to be listed. Default is `journal`.

### Usage

Place your subfolders in the specified directory (e.g., `docs/journal`). Each subfolder will be listed as a subcategory in your documentation.

**Example Directory Structure:**

```
docs/
  journal/
    category1/
      file1.md
    category2/
      file2.md
```

The subcategories list are made available as a `config.subfolder_paths` parameter. For example, you can access it in a theme like this:

```html
{% if subfolder_paths %}
  <div id="journal-categories">
    {{ subfolder_paths }}
  </div>
{% endif %}

<script>
  const categoriesNode = document.querySelector('#journal-categories');
  // Retrieves data
  const journalCategories = categoriesNode ? JSON.parse(categoriesNode.innerHTML.replace(/'/g, '"')) : undefined;
</script>
```