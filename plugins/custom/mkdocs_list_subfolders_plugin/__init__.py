import os
from mkdocs.plugins import BasePlugin
from mkdocs.config import config_options

class ListSubfoldersPlugin(BasePlugin):
    # Define the configuration scheme for the plugin
    config_scheme = (
        ('folder_paths', config_options.Type((str, list), default='journal')),
    )

    def on_config(self, config):
        # Accept either a string or a list for folder_paths
        folder_paths = self.config.get('folder_paths', 'journal')
        if isinstance(folder_paths, str):
            folder_paths = [folder_paths]

        all_subfolder_paths = []
        for folder in folder_paths:
            folder_path = os.path.join(config['docs_dir'], folder)
            subfolder_paths = self.get_subfolder_paths(folder_path)
            all_subfolder_paths.extend(subfolder_paths)

        if 'extra' not in config:
            config['extra'] = {}
        config['extra']['subfolder_paths'] = all_subfolder_paths
        return config

    def get_subfolder_paths(self, folder_path):
        """
        This method returns a list of subfolder paths within the specified folder.
        """
        subfolder_paths = []
        # Walk through the directory to find subfolders
        for root, dirs, files in os.walk(folder_path):
            for dir in dirs:
                # Append the relative path based on the given folder in the configuration
                relative_path = os.path.join(root, dir)
                subfolder_paths.append(relative_path)
            break  # Only get the first level of subfolders
        return subfolder_paths

    def on_page_context(self, context, page, config, nav):
        """
        This method is called when the context for a page is generated.
        It adds the subfolder paths to the page context.
        """
        # Add subfolder_paths to the page context
        context['subfolder_paths'] = config['extra'].get('subfolder_paths', [])
        return context