# Scripts documentation

## Documentation for `concat_md_files.py`

This script concatenates Markdown files from a specified input directory into a single output file and copies a media folder if it exists. It also replaces custom footnote references and definitions with a simpler format.

### Functions

#### `replace_footnotes(content)`

Replaces custom footnote references and definitions in the content with a simpler format.

- **Parameters**: 
  - `content` (str): The content of a Markdown file.
- **Returns**: 
  - `str`: The content with footnote references and definitions replaced.

#### `replace_youtube(content)`

Removes the caption text from YouTube links if present, or leaves only the YouTube link if no caption text is present.

- **Parameters**: 
  - `content` (str): The content of a Markdown file.
- **Returns**: 
  - `str`: The content with YouTube links processed.

#### `replace_video(content)`

Removes the caption text from video links if present, or leaves only the video link if no caption text is present.

- **Parameters**: 
  - `content` (str): The content of a Markdown file.
- **Returns**: 
  - `str`: The content with video links processed.

#### `replace_image(content)`

Replaces image macros with the common Markdown syntax for images.

- **Parameters**: 
  - `content` (str): The content of a Markdown file.
- **Returns**: 
  - `str`: The content with image macros replaced.

#### `replace_macros(content)`

Removes all macros with or without parameters.

- **Parameters**: 
  - `content` (str): The content of a Markdown file.
- **Returns**: 
  - `str`: The content with all macros removed.

#### `concatenate_md_files(input_dir, output_file)`

Concatenates Markdown files from the `docs` directory within the specified input directory into a single output file. It also includes an optional `intro.md` file from the `templates` directory and replaces footnotes in the content.

- **Parameters**: 
  - `input_dir` (str): The input directory containing the `docs` and `templates` directories.
  - `output_file` (str): The path to the output file where the concatenated content will be written.

#### `copy_media_folder(input_dir, output_dir)`

Copies the `media` folder from the `docs` directory within the specified input directory to the specified output directory if it exists.

- **Parameters**: 
  - `input_dir` (str): The input directory containing the `docs` directory.
  - `output_dir` (str): The output directory where the `media` folder will be copied.

### Usage

The script can be run from the command line with the following arguments:

- `--output-dir`: The output directory where the concatenated Markdown file and media folder will be saved. Default is `/wiki/target/tmp`.
- `--input-dir`: The input directory containing the `docs` and `templates` directories. Default is `/wiki`.

#### Example Command

```sh
python concat_md_files.py --output-dir /path/to/output --input-dir /path/to/input
```

### Script Workflow

1. Parse command line arguments to get the input and output directories.
2. Create the output directory if it does not exist.
3. Concatenate Markdown files from the docs directory into a single output file:
  * Include intro.md from the templates directory if it exists.
  * Include index.md from the docs directory if it exists.
  * Include all other Markdown files from the docs directory, excluding index.md.
  * Replace custom macros in the content.
4. Copy the media folder from the docs directory to the output directory if it exists.