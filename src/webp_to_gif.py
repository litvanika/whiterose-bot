import os

from PIL import Image


def webp_to_gif(filepath: str) -> None:
    gif = Image.open(filepath)
    if gif.format == 'WEBP':
        gif.info.pop('background', None)
        gif.save(filepath, 'gif', save_all=True, lossless=True, quality=100, method=6, exact=True)


# https://stackoverflow.com/questions/52016407/how-to-convert-webp-image-to-gif-with-python
def convert_all_images_to_gif() -> None:
    for (dirpath, dirnames, filenames) in os.walk('assets'):
        for filename in filenames:
            try:
                if filename.endswith('.gif'):
                    filepath = os.path.join(dirpath, filename)
                    webp_to_gif(filepath)
            except:
                continue
