import os
import time
import markdown
import shutil
import subprocess
from pathlib import Path
from filelock import FileLock

def define_env(env):

    @env.macro
    def drawio_export(drawio_file, alt="drawio diagram", fmt=None):
        """
        Convert a .drawio file to an image (SVG/PNG/etc.) via drawio-converter CLI.
        
        This macro uses an extra configuration parameter in mkdocs.yml:
        extra:
            drawio_output_format: svg
        or in your PDF config:
        extra:
            drawio_output_format: png

        Usage:
        {{ drawio_export("diagram.drawio") }}
        {{ drawio_export("diagram.drawio", "some alt text") }}
        {{ drawio_export("diagram.drawio", "some alt text", "png") }}
        """

        def wait_for_file(file_path, timeout=10, check_interval=0.2):
            """Waits for the file to be created and its size to stabilize within a specified timeout."""
            start_time = time.time()
            last_size = -1
            while time.time() - start_time < timeout:
                if file_path.exists():
                    current_size = file_path.stat().st_size
                    if current_size == last_size:
                        # File size has stabilized
                        return True
                    last_size = current_size
                time.sleep(check_interval)
            return False

        if not env.page:
            return f"Error: No page context for {drawio_file}"
        
        # Read default format from mkdocs config, fallback to 'svg' if not found
        config_default_format = env.conf.get("extra", {}).get("drawio_output_format", "svg")

        # If caller didn't supply a format, use the config default
        if fmt is None:
            fmt = config_default_format

        # If neither the config nor the caller supplied a format, use 'svg' as the default
        if fmt is None:
            fmt = "svg"

        # Directory of the .md file being processed
        page_dir = Path(env.page.file.abs_src_path).parent

        # Full path to the .drawio file
        src_path = page_dir / drawio_file
        if not src_path.is_file():
            return f"Error: {drawio_file} not found at {src_path}"

        # Output directory under site_dir relative to the current page
        output_dir = Path(env.conf['site_dir']) / Path(env.page.url).parent / 'drawio'
        output_dir.mkdir(parents=True, exist_ok=True)
        final_out_path = output_dir / (src_path.stem + f".{fmt}")

        # we use filelock to prevent concurrency or resource contention issues when multiple macros run in quick succession serializing calls to Draw.io
        lock_path = "/app/drawio.lock"
        lock = FileLock(lock_path)

        # Run drawio-converter
        with lock:
            try:
                result = subprocess.run([
                    "drawio-converter",
                    "-x",      # export
                    "-f", fmt, # format
                    "-o", str(final_out_path),
                    str(src_path)
                ], capture_output=True, text=True)

                # Verify return code
                if result.returncode != 0:
                    return (f"Error: Conversion failed for {drawio_file}. "
                            f"Return code: {result.returncode} - See logs above.")
                
                # Attendi che il file venga creato con un timeout
                if not wait_for_file(final_out_path, timeout=10):
                    return f"Error: Timeout waiting for {final_out_path.name} to be created."

            except subprocess.CalledProcessError as e:
                return f"Error: Conversion failed for {drawio_file}. {e}"

        # Verify output actually got created
        if not final_out_path.exists():
            return f"Error: {final_out_path.name} was not created."

        # Return relative path from the page's directory
        relative_out_path = final_out_path.relative_to(Path(env.conf['site_dir']) / Path(env.page.url).parent)
        return f'<img src="{relative_out_path}" class="drawio" alt="{alt}" />'

    @env.macro
    def button(text, link):
        """
        Generates HTML code for a button that opens a link in a new window.
        
        Args:
            text (str): The text to display on the button.
            link (str): The URL to open when the button is clicked.
        
        Returns:
            str: HTML code for the button.
        """
        sanitized_link = link.replace("'", "\\'")
        return f'<button onclick="window.open(\'{sanitized_link}\')">{text}</button>'
    
    @env.macro
    def image(src, alt, caption=None):
        """
        Generates HTML code for an image with an optional caption.
        
        Args:
            src (str): The source URL of the image.
            alt (str): The alt text for the image.
            caption (str, optional): The caption for the image. Defaults to None.
        
        Returns:
            str: HTML code for the image.
        """
        html_code = (
            '<figure>'
                f'<img src="{src}" alt="{alt}">'
        )
        if caption:
            html_code += f'<figcaption class="caption">{caption}</figcaption>'
        html_code += '</figure>'
        return html_code
    
    @env.macro
    def youtube(src, caption=None):
        """
        Generates HTML code to embed a YouTube video.
        
        Args:
            src (str): The source URL of the YouTube video (embed URL format preferred).
            caption (str, optional): The caption for the video. Defaults to None.
        
        Returns:
            str: HTML code for the embedded YouTube video.
        """
        if caption:
            html_code = (
                '<div class="embedded-video">'
                    f'<iframe src="{src}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen="true"></iframe>'
                    f'<a href="{src}">{caption}</a>'
                '</div>'
            )
        else:
            html_code = (
                '<div class="embedded-video">'
                    f'<iframe src="{src}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen="true"></iframe>'
                '</div>'
            )
        return html_code
    
    @env.macro
    def video(src, caption=None):
        """
        Generates HTML code to embed a video.
        
        Args:
            src (str): The source URL of the video.
            caption (str, optional): The caption for the video. Defaults to None.
        
        Returns:
            str: HTML code for the embedded video.
        """
        if caption:
            html_code = (
                '<div class="video-container">'
                    '<video controls="" style="width: 100%;">'
                        f'<source src="{src}" type="video/mp4">'
                    '</video>'
                    f'<a href="{src}">{caption}</a>'
                '</div>'
            )
        else:
            html_code = (
                '<div class="video-container">'
                    '<video controls="" style="width: 100%;">'
                        f'<source src="{src}" type="video/mp4">'
                    '</video>'
                '</div>'
            )
        return html_code

    @env.macro
    def footnote_ref(number):
        """
        Generates HTML code for a footnote reference.
        
        Args:
            number (int): The footnote number.
        
        Returns:
            str: HTML code for the footnote reference.
        """
        return f'<sup id="ref-{number}"><a href="#footnote-{number}">[{number}]</a></sup>'
      
    @env.macro
    def footnote_def(number):
        """
        Generates HTML code for a footnote definition.
        
        Args:
            number (int): The footnote number.
        
        Returns:
            str: HTML code for the footnote definition.
        """
        return f'<span class="footnote-number" id="footnote-{number}">[{number}]</span>'
      
    @env.macro
    def get_media_url():
        """
        Retrieves the media URL from the environment configuration.
        
        Returns:
            str: The media URL.
        """
        try:
            return env.conf['extra']['media_url']
        except KeyError:
            raise KeyError("The key 'media_url' is missing in 'env.conf['extra']'")
      
    @env.macro
    def list_contents(directory):
        """
        Lists the contents of a given directory or a single Markdown file.

        Args:
            directory (str): The directory or file to process.

        Returns:
            str: HTML content generated from Markdown files.
        """
        # Get the base directory of the script
        base_dir = os.path.dirname(__file__)
        absolute_path = os.path.join(base_dir, directory)

        if os.path.isdir(absolute_path):
            # Process directory
            html_content = ""
            filenames = sorted([f for f in os.listdir(absolute_path) if f.endswith('.md')])
            for filename in filenames:
                file_path = os.path.join(absolute_path, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    markdown_content = file.read()
                html_content += '<div class="expandable-content"><div class="expandable-trigger"></div>' + markdown.markdown(markdown_content) + '</div>'
        elif os.path.isfile(absolute_path) and absolute_path.endswith('.md'):
            # Process single Markdown file
            with open(absolute_path, 'r', encoding='utf-8') as file:
                markdown_content = file.read()
            html_content = '<div class="expandable-content"><div class="expandable-trigger"></div>' + markdown.markdown(markdown_content) + '</div>'
        else:
            raise FileNotFoundError(f"The directory or Markdown file '{absolute_path}' does not exist.")

        return html_content
  
    @env.filter
    def get_keys(value):
        """
        Retrieves the keys of the __dict__ attribute of a page object in MkDocs.
        
        Args:
            value (object): The page object to retrieve the keys from.
        
        Returns:
            list: A list of keys from the page object's __dict__ attribute.
        """
        return value.__dict__.keys()
