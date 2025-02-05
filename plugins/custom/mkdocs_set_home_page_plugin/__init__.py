from mkdocs.plugins import BasePlugin
import os

class SetHomePagePlugin(BasePlugin):
    def on_pre_build(self, config):
        # Check if 'home_page' is declared in 'extra'
        home_page = config['extra'].get('home_page')
        
        if home_page:
            # Set the home page
            home_page_path = os.path.join(config['docs_dir'], home_page)
            index_page_path = os.path.join(config['docs_dir'], 'index.md')
            
            if os.path.exists(home_page_path):
                if os.path.exists(index_page_path):
                    os.remove(index_page_path)
                os.symlink(home_page_path, index_page_path)

        return config