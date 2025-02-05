import os
from mkdocs.plugins import BasePlugin
from mkdocs.config import config_options

class ListSubfoldersPlugin(BasePlugin):
    # Define the configuration scheme for the plugin
    config_scheme = (
        ('folder_path', config_options.Type(str, default='docs')),
    )

    def on_config(self, config):
        """
        This method is called when the MkDocs configuration is loaded.
        It adds the list of subfolder paths to the MkDocs configuration.
        """
        # Construct the full path to the target folder
        folder_path = os.path.join('docs', self.config['folder_path'])
        
        # Get the list of subfolder paths
        subfolder_paths = self.get_subfolder_paths(folder_path)
        
        # Ensure 'extra' exists in the config
        if 'extra' not in config:
            config['extra'] = {}
        
        # Add the subfolder paths to the 'extra' section of the config
        config['extra']['subfolder_paths'] = subfolder_paths
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
                relative_path = os.path.relpath(os.path.join(root, dir), 'docs')
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