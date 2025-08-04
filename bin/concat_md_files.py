import os
import re
import shutil
import argparse

def has_media_folder(input_dir, docs_dir):
    media_path = os.path.join(input_dir, docs_dir, 'media')
    return os.path.isdir(media_path)

def replace_footnotes(content):
    # Replace footnote references with Pandoc-style references
    content = re.sub(r'\{\{\s*footnote_ref\((\d+)\)\s*\}\}', r'[^\1]', content)
    # Replace footnote definitions with Pandoc-style definitions (you may need to append the actual text after the colon)
    content = re.sub(r'\{\{\s*footnote_def\((\d+)\)\s*\}\}', r'[^\1]:', content)
    return content

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

def replace_button(content):
    content = re.sub(r"\{\{\s*button\(['\"]([^'\"]+)['\"](?:,\s*['\"]([^'\"]*)['\"])?\)\s*\}\}", '', content)
    return content

def replace_list_contents(content):
    content = re.sub(r"\{\{\s*list_contents\([^\)]*\)\s*\}\}", '', content)
    content = re.sub(r"\{\{\s*list_contents\(\)\s*\}\}", '', content)
    return content

def replace_macros(content):
    # Remove all macros only if they were not handled by previous functions
    content = re.sub(r"\{\{\s*\w+\([^\)]*\)\s*\}\}", '', content)
    return content

def replace_relative_media_links(content, md_file_path, docs_dir):
    allowed_exts = ('.mp4', '.png', '.jpg', '.jpeg', '.svg')
    folder = os.path.relpath(os.path.dirname(md_file_path), docs_dir)

    # Replace [alt](relative_path.ext) for allowed extensions
    def link_repl(match):
        alt_text = match.group(1)
        rel_path = match.group(2)
        if rel_path.startswith(('http://', 'https://', 'files/')):
            return match.group(0)
        if not rel_path.lower().endswith(allowed_exts):
            return match.group(0)
        rel_path_clean = rel_path[2:] if rel_path.startswith('./') else rel_path
        new_path = f'./files/{folder}/{rel_path_clean}' if folder != '.' else f'./files/{rel_path_clean}'
        return f'[{alt_text}]({new_path})'

    # Replace ![](relative_path.ext) for allowed extensions
    def img_repl(match):
        rel_path = match.group(1)
        if rel_path.startswith(('http://', 'https://', 'files/')):
            return match.group(0)
        if not rel_path.lower().endswith(allowed_exts):
            return match.group(0)
        rel_path_clean = rel_path[2:] if rel_path.startswith('./') else rel_path
        new_path = f'./files/{folder}/{rel_path_clean}' if folder != '.' else f'./files/{rel_path_clean}'
        return f'![]({new_path})'

    # [alt](relative_path.ext)
    content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', link_repl, content)
    # ![](relative_path.ext)
    content = re.sub(r'!\[\]\(([^)]+)\)', img_repl, content)
    return content

def process_content(content, md_file_path=None, docs_dir=None, skip_media_links=False):
    content = replace_footnotes(content)
    content = replace_youtube(content)
    content = replace_video(content)
    content = replace_image(content)
    content = replace_button(content)
    content = replace_list_contents(content)
    content = replace_macros(content)  # Ensure this runs last
    if md_file_path and docs_dir and not skip_media_links:
        content = replace_relative_media_links(content, md_file_path, docs_dir)
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
def concatenate_md_files(input_dir, docs_dir, output_file):
    docs_dir_full = os.path.join(input_dir, docs_dir)
    templates_dir = os.path.join(input_dir, 'templates')
    skip_media_links = has_media_folder(input_dir, docs_dir)

    with open(output_file, 'w') as outfile:
        intro_file = os.path.join(templates_dir, 'intro.md')
        if os.path.exists(intro_file):
            with open(intro_file, 'r') as infile:
                content = process_content(infile.read(), intro_file, docs_dir_full, skip_media_links)
                outfile.write(content + '\n\n')

        index_file = os.path.join(docs_dir_full, 'index.md')
        if os.path.exists(index_file):
            with open(index_file, 'r') as infile:
                content = process_content(infile.read(), index_file, docs_dir_full, skip_media_links)
                outfile.write(content + '\n\n')

        md_files = []
        for root, _, files in os.walk(docs_dir_full):
            for file in files:
                if file.endswith('.md') and file != 'index.md':
                    md_files.append(os.path.join(root, file))

        md_files.sort()

        for md_file in md_files:
            with open(md_file, 'r') as infile:
                content = process_content(infile.read(), md_file, docs_dir_full, skip_media_links)
                outfile.write(content + '\n\n')

""" def copy_media_folder(input_dir, docs_dir, output_dir):
    docs_dir = os.path.join(input_dir, docs_dir)
    media_src = os.path.join(docs_dir, 'media')
    media_dst = os.path.join(output_dir, 'media')

    if os.path.exists(media_src) and os.path.isdir(media_src):
        shutil.copytree(media_src, media_dst, dirs_exist_ok=True) """

""" def copy_media_to_docx_folder(tmp_output_dir, docx_output_dir):
    media_src = os.path.join(tmp_output_dir, 'media')
    media_dst = os.path.join(docx_output_dir, 'media')
    if os.path.exists(media_src) and os.path.isdir(media_src):
        shutil.copytree(media_src, media_dst, dirs_exist_ok=True) """

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--output-dir', default='/wiki/target/tmp', help='Output directory')
    parser.add_argument('--input-dir', default='/wiki', help='Input directory')
    parser.add_argument('--docs-dir', default='docs', help='Docs directory')
    parser.add_argument('--docx-dir', default='/wiki/target/docx', help='Docx output directory')
    args = parser.parse_args()
    
    os.makedirs(args.output_dir, exist_ok=True)
    output_file = os.path.join(args.output_dir, 'all_docs.md')

    # Only copy non-md files if media folder is NOT present
    if not has_media_folder(args.input_dir, args.docs_dir):
        for target_dir in ['/wiki/target/tmp/files', '/wiki/target/docx/files', '/wiki/target/html/files', '/wiki/target/md/files']:
            os.makedirs(target_dir, exist_ok=True)
            copy_non_md_files(args.input_dir, args.docs_dir, target_dir)

    if has_media_folder(args.input_dir, args.docs_dir):
        media_src = os.path.join(args.input_dir, args.docs_dir, 'media')
        for target_dir in [
            '/wiki/target/tmp/media',
            '/wiki/target/docx/media',
            '/wiki/target/html/media',
            '/wiki/target/md/media'
        ]:
            os.makedirs(os.path.dirname(target_dir), exist_ok=True)
            shutil.copytree(media_src, target_dir, dirs_exist_ok=True)

    concatenate_md_files(args.input_dir, args.docs_dir, output_file)
    # Save a debug copy in /wiki/target/md/all_docs.md
    debug_md_dir = '/wiki/target/md'
    os.makedirs(debug_md_dir, exist_ok=True)
    debug_md_file = os.path.join(debug_md_dir, 'all_docs.md')
    shutil.copy2(output_file, debug_md_file)
    # copy_media_folder(args.input_dir, args.docs_dir, args.output_dir)
    # copy_media_to_docx_folder(args.output_dir, args.docx_dir)
