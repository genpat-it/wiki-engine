from mkdocs.plugins import BasePlugin
import os
import shutil

class SetHomePagePlugin(BasePlugin):
    def __init__(self):
        super().__init__()
        self.created_index = False
        self.index_page_path = None

    def on_pre_build(self, config):
        # Check if 'home_page' is declared in 'extra'
        home_page = config['extra'].get('home_page')
        
        if home_page:
            # Set the home page
            home_page_path = os.path.join(config['docs_dir'], home_page)
            self.index_page_path = os.path.join(config['docs_dir'], 'index.md')
            
            if os.path.exists(home_page_path):
                index_existed = os.path.exists(self.index_page_path)
                
                if index_existed:
                    os.remove(self.index_page_path)
                
                shutil.copy2(home_page_path, self.index_page_path)
                
                # Only mark for removal if we created it (index.md didn't exist before)
                self.created_index = not index_existed

        return config

    def on_post_build(self, config):
        # Remove the index.md we created if it didn't exist before
        if self.created_index and self.index_page_path and os.path.exists(self.index_page_path):
            os.remove(self.index_page_path)
            self.created_index = False
            self.index_page_path = None

        return config