import os
import yaml
from datetime import datetime
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import File
from mkdocs.structure.pages import Page
from mkdocs.config import config_options

# Define a custom MkDocs plugin class
class JournalPlugin(BasePlugin):
    # Define the configuration scheme for the plugin
    config_scheme = (
        ('directory', config_options.Type(dict, default={'journal': {'items_per_page': 5}})),
    )

    # Hook that is called when files are collected
    def on_files(self, files, config):
        journal_files = []
        directories = self.config['directory']
        base_url = config.get('site_url', '').rstrip('/')

        for file in files:
            for dir_name, dir_opts in directories.items():
                file_folder = file.src_path.split(os.sep)[0]
                if file_folder == dir_name and file.src_path.endswith('.md') and not file.src_path.endswith('index.md'):
                    with open(file.abs_src_path, 'r') as f:
                        content = f.read()
                        metadata, _ = self._split_front_matter(content)
                        if metadata:
                            if 'date' in metadata and isinstance(metadata['date'], str):
                                metadata['date'] = datetime.strptime(metadata['date'], '%Y-%m-%d').date()
                            journal_file = {
                                'src_path': file.src_path,
                                'base_url': base_url,
                                'context_path': os.path.dirname(file.src_path),
                                'title': metadata.get('title', 'Untitled'),
                                'date': metadata.get('date', datetime.min.date()).isoformat(),
                                'thumbnail': metadata.get('thumbnail', None),
                                'page_number': None,
                                'directory': dir_name,
                                'items_per_page': dir_opts.get('items_per_page', 5)
                            }
                            journal_files.append(journal_file)
        # Sort and assign page numbers per directory
        for dir_name, dir_opts in directories.items():
            dir_files = [f for f in journal_files if f['directory'] == dir_name]
            dir_files.sort(key=lambda x: x['date'], reverse=True)
            items_per_page = dir_opts.get('items_per_page', 5)
            for i, file in enumerate(dir_files):
                file['page_number'] = (i // items_per_page) + 1

        config['extra']['journal_files'] = journal_files
        return files

    # Hook that is called when the context for a page is created
    def on_page_context(self, context, page, config, nav):
        current_directory = os.path.dirname(page.file.src_path)
        journal_files = [file for file in config['extra'].get('journal_files', []) if file['src_path'].startswith(current_directory)]
        # Get items_per_page for this directory
        directories = self.config['directory']
        items_per_page = None
        for dir_name, dir_opts in directories.items():
            if page.file.src_path.startswith(dir_name):
                items_per_page = dir_opts.get('items_per_page', 5)
                break
        context['journal_files'] = journal_files
        context['items_per_page'] = items_per_page
        return context

    # Helper method to split the front matter from the content
    def _split_front_matter(self, content):
        if content.startswith('---'):
            _, front_matter, content = content.split('---', 2)
            metadata = yaml.safe_load(front_matter)
            return metadata, content
        return None, content