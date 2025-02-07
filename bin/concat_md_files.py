import os
import re
import shutil
import argparse

def replace_footnotes(content):
    content = re.sub(r'\{\{\s*footnote_ref\((\d+)\)\s*\}\}', r'[\1]', content)
    content = re.sub(r'\{\{\s*footnote_def\((\d+)\)\s*\}\}', r'[\1]', content)
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

def process_content(content):
    content = replace_footnotes(content)
    content = replace_youtube(content)
    content = replace_video(content)
    content = replace_image(content)
    content = replace_button(content)
    content = replace_list_contents(content)
    content = replace_macros(content)  # Ensure this runs last
    return content

def concatenate_md_files(input_dir, docs_dir, output_file):
    docs_dir = os.path.join(input_dir, docs_dir)
    templates_dir = os.path.join(input_dir, 'templates')
    
    with open(output_file, 'w') as outfile:
        # Process intro.md if it exists
        intro_file = os.path.join(templates_dir, 'intro.md')
        if os.path.exists(intro_file):
            with open(intro_file, 'r') as infile:
                content = process_content(infile.read())
                outfile.write(content + '\n\n')

        # Process index.md if it exists
        index_file = os.path.join(docs_dir, 'index.md')
        if os.path.exists(index_file):
            with open(index_file, 'r') as infile:
                content = process_content(infile.read())
                outfile.write(content + '\n\n')

        # Collect and process all markdown files in docs_dir (except index.md)
        md_files = []
        for root, _, files in os.walk(docs_dir):
            for file in files:
                if file.endswith('.md') and file != 'index.md':
                    md_files.append(os.path.join(root, file))

        md_files.sort()

        for md_file in md_files:
            with open(md_file, 'r') as infile:
                content = process_content(infile.read())
                outfile.write(content + '\n\n')

def copy_media_folder(input_dir, docs_dir, output_dir):
    docs_dir = os.path.join(input_dir, docs_dir)
    media_src = os.path.join(docs_dir, 'media')
    media_dst = os.path.join(output_dir, 'media')

    if os.path.exists(media_src) and os.path.isdir(media_src):  # Ensure it exists and is a directory
        shutil.copytree(media_src, media_dst, dirs_exist_ok=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--output-dir', default='/wiki/target/tmp', help='Output directory')
    parser.add_argument('--input-dir', default='/wiki', help='Input directory')
    parser.add_argument('--docs-dir', default='docs', help='Docs directory')
    args = parser.parse_args()
    
    os.makedirs(args.output_dir, exist_ok=True)
    output_file = os.path.join(args.output_dir, 'all_docs.md')
    
    concatenate_md_files(args.input_dir, args.docs_dir, output_file)
    copy_media_folder(args.input_dir, args.docs_dir, args.output_dir)
