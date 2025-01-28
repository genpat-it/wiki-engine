import markdown
import os

def define_env(env):

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
