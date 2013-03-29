# -*- coding: iso-8859-1 -*-
def compress_javascript(config, output_path):
    from mediacompress import compress_js_files
    compress_js_files(output_path)


def compress_images(config, output_path):
    from mediacompress import compress_image_files
    compress_image_files(output_path)


def compress_css(config, output_path):
    from mediacompress import compress_css_files
    compress_css_files(output_path)

hooks = {
    'site.output.post': [compress_javascript, compress_images, compress_css],
}
