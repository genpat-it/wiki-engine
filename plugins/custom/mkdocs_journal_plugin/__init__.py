import os
import yaml
from datetime import datetime, date
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import File
from mkdocs.structure.pages import Page
from mkdocs.config import config_options
import requests

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
        build_date = datetime.now().isoformat()  # Build/check date

        def is_url_valid(url):
            try:
                response = requests.head(url, allow_redirects=True, timeout=5)
                if response.status_code == 405:  # Method Not Allowed, try GET
                    response = requests.get(url, allow_redirects=True, timeout=5)
                return response.status_code == 200
            except Exception:
                return False

        for file in files:
            for dir_name, dir_opts in directories.items():
                file_folder = file.src_path.split(os.sep)[0]
                if file_folder == dir_name and file.src_path.endswith('.md') and not file.src_path.endswith('index.md'):
                    with open(file.abs_src_path, 'r') as f:
                        content = f.read()
                        metadata, _ = self._split_front_matter(content)
                        if metadata:
                            # Convert all date/datetime fields in metadata to isoformat strings
                            for key, value in metadata.items():
                                if isinstance(value, (datetime, date)):
                                    metadata[key] = value.isoformat()

                            # Handle additional_metadata
                            additional_metadata = metadata.get('additional_metadata', {})
                            if isinstance(additional_metadata, dict):
                                link = additional_metadata.get('link')
                                if link:
                                    additional_metadata['link_valid'] = is_url_valid(link)
                                    additional_metadata['link_checked_at'] = build_date

                            # Fallback: use file creation date if no date in metadata
                            if 'date' in metadata and metadata['date']:
                                date_value = metadata['date']
                            else:
                                stat = os.stat(file.abs_src_path)
                                if hasattr(stat, 'st_birthtime'):
                                    creation_time = stat.st_birthtime
                                else:
                                    creation_time = stat.st_ctime
                                date_value = datetime.fromtimestamp(creation_time).date().isoformat()

                            journal_file = {
                                'src_path': file.src_path,
                                'base_url': base_url,
                                'context_path': os.path.dirname(file.src_path),
                                'title': metadata.get('title', 'Untitled'),
                                'date': date_value,
                                'description': metadata.get('description', None),
                                'terms': metadata.get('terms', []),
                                'thumbnail': metadata.get('thumbnail', None),
                                'category': metadata.get('category', None),
                                'additional_metadata': additional_metadata,
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