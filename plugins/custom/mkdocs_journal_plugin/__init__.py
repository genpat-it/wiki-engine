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
        ('directory', config_options.Type(str, default='journal')),
        ('items_per_page', config_options.Type(int, default=5)),
    )

    # Hook that is called when files are collected
    def on_files(self, files, config):
        journal_files = []
        directory = self.config['directory']
        items_per_page = self.config['items_per_page']
        base_url = config.get('site_url', '').rstrip('/')

        # Iterate over all files in the MkDocs project
        for file in files:
            # Check if the file is in the specified directory, is a Markdown file, and is not 'index.md'
            if file.src_path.startswith(directory) and file.src_path.endswith('.md') and not file.src_path.endswith('index.md'):
                # Read the file content
                with open(file.abs_src_path, 'r') as f:
                    content = f.read()
                    # Split the front matter from the content
                    metadata, _ = self._split_front_matter(content)
                    if metadata:
                        # Parse the date if it exists in the metadata
                        if 'date' in metadata and isinstance(metadata['date'], str):
                            metadata['date'] = datetime.strptime(metadata['date'], '%Y-%m-%d').date()
                        # Create a dictionary with the necessary information
                        journal_file = {
                            'src_path': file.src_path,
                            'base_url': base_url,
                            'context_path': os.path.dirname(file.src_path),
                            'title': metadata.get('title', 'Untitled'),
                            'date': metadata.get('date', datetime.min.date()).isoformat(),
                            'thumbnail': metadata.get('thumbnail', None),
                            'page_number': None  # Placeholder for page number
                        }
                        journal_files.append(journal_file)

        # Sort the journal files by date in descending order
        journal_files.sort(key=lambda x: x['date'], reverse=True)

        # Add page information to each journal file
        for i, file in enumerate(journal_files):
            file['page_number'] = (i // items_per_page) + 1

        # Store the sorted journal files in the config for later use
        config['extra']['journal_files'] = journal_files
        return files

    # Hook that is called when the context for a page is created
    def on_page_context(self, context, page, config, nav):
        current_directory = os.path.dirname(page.file.src_path)
        items_per_page = self.config['items_per_page']
        # Filter the journal files to include only those in the current directory
        journal_files = [file for file in config['extra'].get('journal_files', []) if file['src_path'].startswith(current_directory)]
        # Add the filtered journal files to the page context
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