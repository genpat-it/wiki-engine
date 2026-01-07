import logging
from mkdocs.plugins import BasePlugin
from mkdocs.structure.nav import get_navigation


log = logging.getLogger(__name__)


class NavOnlyPlugin(BasePlugin):
    """Restrict documentation pages to those declared in nav."""

    def on_files(self, files, config, **kwargs):
        nav = get_navigation(files, config)
        nav_page_src_paths = {
            page.file.src_path
            for page in getattr(nav, "pages", [])
            if getattr(page, "file", None)
        }
        if not nav_page_src_paths:
            return files
        kept = []
        for file in files:
            if file.is_documentation_page():
                if file.src_path in nav_page_src_paths:
                    kept.append(file)
            else:
                kept.append(file)
        log.info(
            "nav-only plugin: keeping %s files from %s total",
            len(kept),
            len(files),
        )
        return files.__class__(kept)
