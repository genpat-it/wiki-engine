import os
import re
import shutil
import argparse

def has_media_folder(input_dir, docs_dir):
    media_path = os.path.join(input_dir, docs_dir, 'media')
    return os.path.isdir(media_path)

def replace_youtube(content):
    content = re.sub(r"\{\{\s*youtube\(['\"]([^'\"]+)['\"]\s*,\s*['\"]([^'\"]+)['\"]\)\s*\}\}", r'[\2](\1)', content)
    content = re.sub(r"\{\{\s*youtube\(['\"]([^'\"]+)['\"]\)\s*\}\}", r'[\1](\1)', content)
    return content

def replace_video(content):
    content = re.sub(r"\{\{\s*video\(['\"]([^'\"]+)['\"]\s*,\s*['\"]([^'\"]+)['\"]\)\s*\}\}", r'[\2](\1)', content)
    content = re.sub(r"\{\{\s*video\(['\"]([^'\"]+)['\"]\)\s*\}\}", r'[video](\1)', content)
    return content

def replace_image(content):
    # Matches image macros with any number of parameters and captures only the address
    content = re.sub(r"\{\{\s*image\(['\"]([^'\"]+)['\"](?:,\s*['\"][^'\"]*['\"])*\s*\)\s*\}\}", r'![](\1)', content)
    return content

def replace_relative_res_links(content, md_file_path, docs_dir):
    # Allow all extensions except .md
    def is_allowed_ext(path):
      # Allow internal anchor links (e.g., #section)
      if path.startswith('#'):
          return False
      # Remove fragment before checking extension
      path_no_fragment = path.split('#', 1)[0]
      ext = os.path.splitext(path_no_fragment)[1].lower()
      return ext != '.md'

    folder = os.path.relpath(os.path.dirname(md_file_path), docs_dir)

    def link_repl(match):
        alt_text = match.group(1)
        rel_path = match.group(2)
        if rel_path.startswith(('http://', 'https://', 'res/', '.res/')):
            return match.group(0)
        if not is_allowed_ext(rel_path):
            return match.group(0)
        rel_path_clean = rel_path[2:] if rel_path.startswith('./') else rel_path
        new_path = f'./res/{folder}/{rel_path_clean}' if folder != '.' else f'./res/{rel_path_clean}'
        return f'[{alt_text}]({new_path})'

    def img_repl(match):
        rel_path = match.group(1)
        if rel_path.startswith(('http://', 'https://', 'res/', '.res/')):
            return match.group(0)
        if not is_allowed_ext(rel_path):
            return match.group(0)
        rel_path_clean = rel_path[2:] if rel_path.startswith('./') else rel_path
        new_path = f'./res/{folder}/{rel_path_clean}' if folder != '.' else f'./res/{rel_path_clean}'
        return f'![]({new_path})'

    # [alt](relative_path.ext)
    content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', link_repl, content)
    # ![](relative_path.ext)
    content = re.sub(r'!\[\]\(([^)]+)\)', img_repl, content)
    return content

def extract_first_h1_title(md_path):
    """Extract the first H1 (# ...) title, skipping YAML front matter."""
    with open(md_path, encoding='utf-8') as f:
        in_yaml = False
        for line in f:
            if line.strip() == "---":
                in_yaml = not in_yaml
                continue
            if in_yaml:
                continue
            m = re.match(r'#\s+(.+)', line)
            if m:
                return m.group(1).strip()
    return None

def get_md_titles(docs_dir):
    md_titles = {}
    for root, _, files in os.walk(docs_dir):
        for file in files:
            if file.endswith('.md'):
                path = os.path.join(root, file)
                rel_path = os.path.relpath(path, docs_dir)
                title = extract_first_h1_title(path)
                if title:
                    anchor = '#' + re.sub(r'[^a-zA-Z0-9]+', '-', title).lower().strip('-')
                    md_titles[rel_path] = anchor
    return md_titles

def replace_md_links(content, md_file_path, docs_dir, md_titles):
    """
    Replace [text](some.md) with [text](#anchor) if anchor is found.
    For [text](some.md#fragment), replace with [text](#fragment).
    """
    folder = os.path.relpath(os.path.dirname(md_file_path), docs_dir)
    def repl(match):
        alt_text = match.group(1)
        rel_path = match.group(2)
        # If the link contains a fragment (i.e., #), use only the fragment as anchor
        if '.md#' in rel_path:
            fragment = rel_path.split('#', 1)[1]
            return f'[{alt_text}](#{fragment})'
        # Otherwise, replace as before
        rel_path_norm = os.path.normpath(os.path.join(folder, rel_path))
        if rel_path.endswith('.md') and rel_path_norm in md_titles:
            return f'[{alt_text}]({md_titles[rel_path_norm]})'
        return match.group(0)
    return re.sub(r'\[([^\]]+)\]\(([^)]+)\)', repl, content)

def process_content(content, md_file_path=None, docs_dir=None, skip_media_links=False, md_titles=None):
    content = replace_youtube(content)
    content = replace_video(content)
    content = replace_image(content)
    if md_file_path and docs_dir and not skip_media_links:
        content = replace_relative_res_links(content, md_file_path, docs_dir)
    if md_titles is not None and md_file_path and docs_dir:
        content = replace_md_links(content, md_file_path, docs_dir, md_titles)
    return content

def copy_non_md_files(input_dir, docs_dir, target_files_dir):
    docs_dir = os.path.join(input_dir, docs_dir)
    for root, _, files in os.walk(docs_dir):
        for file in files:
            if not file.endswith('.md'):
                src_file = os.path.join(root, file)
                # Get relative path to docs_dir
                rel_path = os.path.relpath(src_file, docs_dir)
                dst_file = os.path.join(target_files_dir, rel_path)
                os.makedirs(os.path.dirname(dst_file), exist_ok=True)
                shutil.copy2(src_file, dst_file)

# In concatenate_md_files, pass md_file_path and docs_dir to process_content:
def concatenate_md_files(input_dir, docs_dir, output_file, index_file='index.md'):
    docs_dir_full = os.path.join(input_dir, docs_dir)
    templates_dir = os.path.join(input_dir, 'templates')
    skip_media_links = has_media_folder(input_dir, docs_dir)
    md_titles = get_md_titles(docs_dir_full)  # <-- Build mapping here

    with open(output_file, 'w') as outfile:
        intro_file = os.path.join(templates_dir, 'intro.md')
        if os.path.exists(intro_file):
            with open(intro_file, 'r') as infile:
                content = process_content(infile.read(), intro_file, docs_dir_full, skip_media_links, md_titles)
                outfile.write(content + '\n\n')

        index_file_path = os.path.join(docs_dir_full, index_file)
        if os.path.exists(index_file_path):
            with open(index_file_path, 'r') as infile:
                content = process_content(infile.read(), index_file_path, docs_dir_full, skip_media_links, md_titles)
                outfile.write(content + '\n\n')

        md_files = []
        for root, _, files in os.walk(docs_dir_full):
            for file in files:
                if file.endswith('.md') and file != index_file:
                    md_files.append(os.path.join(root, file))

        md_files.sort()

        for md_file in md_files:
            with open(md_file, 'r') as infile:
                content = process_content(infile.read(), md_file, docs_dir_full, skip_media_links, md_titles)
                outfile.write(content + '\n\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--output-dir', default='/wiki/target/tmp', help='Output directory')
    parser.add_argument('--input-dir', default='/wiki', help='Input directory')
    parser.add_argument('--docs-dir', default='docs', help='Docs directory')
    parser.add_argument('--index-file', default='index.md', help='Index file name')
    parser.add_argument('--docx-dir', default='/wiki/target/docx', help='Docx output directory')
    args = parser.parse_args()
    
    os.makedirs(args.output_dir, exist_ok=True)
    output_file = os.path.join(args.output_dir, 'index.md')

    # Only copy non-md files if media folder is NOT present
    if not has_media_folder(args.input_dir, args.docs_dir):
        for target_dir in [
            '/wiki/target/md_for_mkdocs/docs/res'
        ]:
            os.makedirs(target_dir, exist_ok=True)
            copy_non_md_files(args.input_dir, args.docs_dir, target_dir)

    if has_media_folder(args.input_dir, args.docs_dir):
        media_src = os.path.join(args.input_dir, args.docs_dir, 'media')
        for target_dir in [
            '/wiki/target/md_for_mkdocs/docs/media'
        ]:
            os.makedirs(os.path.dirname(target_dir), exist_ok=True)
            shutil.copytree(media_src, target_dir, dirs_exist_ok=True)

    concatenate_md_files(args.input_dir, args.docs_dir, output_file, args.index_file)
    # Save a debug copy in /wiki/target/md/index.md
    debug_md_dir = '/wiki/target/md_for_mkdocs/docs'
    os.makedirs(debug_md_dir, exist_ok=True)
    debug_md_file = os.path.join(debug_md_dir, 'index.md')
    shutil.copy2(output_file, debug_md_file)
    # copy_media_folder(args.input_dir, args.docs_dir, args.output_dir)
    # copy_media_to_docx_folder(args.output_dir, args.docx_dir)
