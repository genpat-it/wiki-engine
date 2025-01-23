def define_env(env):
    
    @env.macro
    def image(src, alt, caption=None):
        html_code = (
            '<figure>'
                f'<img src="{src}" alt="{alt}">'
        )
        if caption:
            html_code += f'<figcaption class="caption">{caption}</figcaption>'
        html_code += '</figure>'
        return html_code
    
    @env.macro
    def youtube(src):
        html_code = (
            '<div class="embedded-video">'
                f'<iframe src="{src}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen="true"></iframe>'
            '</div>'
        )
        return html_code
    
    @env.macro
    def video(src):
        html_code = (
            '<div class="video-container">'
                '<video controls="" style="width: 100%">'
                    f'<source src="{src}" type="video/mp4">'
                '</video>'
            '</div>'
        )
        return html_code

    @env.macro
    def footnote_ref(number):
        return f'<sup id="ref-{number}"><a href="#footnote-{number}">[{number}]</a></sup>'
      
    @env.macro
    def footnote_def(number):
        return f'<span class="footnote-number" id="footnote-{number}"">[{number}]</span>'