import os
import re
import shutil
import argparse

def replace_footnotes(content):
    content = re.sub(r'\{\{\s*footnote_ref\((\d+)\)\s*\}\}', r'[\1]', content)
    content = re.sub(r'\{\{\s*footnote_def\((\d+)\)\s*\}\}', r'[\1]', content)
    return content

def replace_youtube(content):
    # Replace YouTube macros with caption text
    content = re.sub(r"\{\{\s*youtube\(['\"]([^'\"]*)['\"],\s*['\"]([^'\"]*)['\"]\)\s*\}\}", r'[\2](\1)', content)
    # Replace YouTube macros without caption text
    content = re.sub(r"\{\{\s*youtube\(['\"]([^'\"]*)['\"]\)\s*\}\}", r'[video](\1)', content)
    return content

def replace_video(content):
    # Replace video macros with caption text
    content = re.sub(r"\{\{\s*video\(['\"]([^'\"]*)['\"],\s*['\"]([^'\"]*)['\"]\)\s*\}\}", r'[\2](\1)', content)
    # Replace video macros without caption text
    content = re.sub(r"\{\{\s*video\(['\"]([^'\"]*)['\"]\)\s*\}\}", r'[video](\1)', content)
    return content

def replace_image(content):
    # Replace image with caption and alternative text
    content = re.sub(r"\{\{\s*image\(['\"]([^'\"]*)['\"],\s*['\"][^'\"]*['\"],\s*['\"][^'\"]*['\"]\)\s*\}\}", r'![](\1)', content)
    # Replace image with alternative text only
    content = re.sub(r"\{\{\s*image\(['\"]([^'\"]*)['\"],\s*['\"][^'\"]*['\"]\)\s*\}\}", r'![](\1)', content)
    # Replace image with no additional text
    content = re.sub(r"\{\{\s*image\(['\"]([^'\"]*)['\"]\)\s*\}\}", r'![](\1)', content)
    return content

def replace_button(content):
    # Remove the button label and URL, handling optional spaces and parameters
    content = re.sub(r"\{\{\s*button\(['\"]([^'\"]*)['\"](?:,\s*['\"]([^'\"]*)['\"])?\)\s*\}\}", '', content)
    return content

def replace_list_contents(content):
    # Remove the list_contents with a directory
    content = re.sub(r"\{\{\s*list_contents\([^\)]*\)\s*\}\}", '', content)
    # Remove the list_contents with no parameters
    content = re.sub(r"\{\{\s*list_contents\(\)\s*\}\}", '', content)
    return content

def replace_macros(content):
    # Remove all macros with or without parameters
    content = re.sub(r"\{\{\s*\w+\([^\)]*\)\s*\}\}", '', content)
    return content

def concatenate_md_files(input_dir, docs_dir, output_file):
    docs_dir = os.path.join(input_dir, docs_dir)
    templates_dir = os.path.join(input_dir, 'templates')
    
    with open(output_file, 'w') as outfile:
       intro_file = os.path.join(templates_dir, 'intro.md')
       if os.path.exists(intro_file):
           with open(intro_file, 'r') as infile:
               content = replace_footnotes(infile.read())
               outfile.write(content + '\n\n')

       index_file = os.path.join(docs_dir, 'index.md')
       if os.path.exists(index_file):
           with open(index_file, 'r') as infile:
               content = replace_footnotes(infile.read())
               outfile.write(content + '\n\n')

       md_files = []
       for root, _, files in os.walk(docs_dir):
           for file in files:
               if file.endswith('.md') and file != 'index.md':
                   md_files.append(os.path.join(root, file))

       md_files.sort()

       for md_file in md_files:
           with open(md_file, 'r') as infile:
               content = replace_footnotes(infile.read())
               outfile.write(content + '\n\n')

def copy_media_folder(input_dir, docs_dir, output_dir):
    docs_dir = os.path.join(input_dir, docs_dir)
    media_src = os.path.join(docs_dir, 'media')
    media_dst = os.path.join(output_dir, 'media')
    if os.path.exists(media_src):
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