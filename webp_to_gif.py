import os

from PIL import Image


# https://stackoverflow.com/questions/52016407/how-to-convert-webp-image-to-gif-with-python
def convert_all_images_to_gif():
    for (dirpath, dirnames, filenames) in os.walk('assets'):
        for filename in filenames:
            try:
                if filename.endswith('.gif'):
                    filepath = os.path.join(dirpath, filename)
                    gif = Image.open(filepath)
                    if gif.format == 'WEBP':
                        gif.info.pop('background', None)
                        gif.save(filepath, 'gif', save_all=True, lossless=True, quality=100, method=6, exact=True)
            except:
                continue


def main():
    convert_all_images_to_gif()


if __name__ == '__main__':
    main()
