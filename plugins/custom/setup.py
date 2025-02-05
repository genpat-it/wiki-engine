from setuptools import setup, find_packages

setup(
    name='mkdocs_custom_plugins',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'mkdocs.plugins': [
            'journal_plugin = mkdocs_journal_plugin:JournalPlugin',
            'list_subfolders_plugin = mkdocs_list_subfolders_plugin:ListSubfoldersPlugin',
            'set_home_page_plugin = mkdocs_set_home_page_plugin:SetHomePagePlugin',
        ]
    }
)