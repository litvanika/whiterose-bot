import os
import random


FILE_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.webp']


def get_assets(path: str) -> list[str]:
    assets_path = os.path.split(path)[0]
    all_assets = os.listdir(assets_path)
    file_assets = list(filter(
        lambda asset:
            os.path.isfile(os.path.join(assets_path, asset)) and
            os.path.splitext(asset)[1] in FILE_EXTENSIONS,
        all_assets,
    ))
    assets = random.sample(file_assets, 3)
    full_path_assets = [os.path.join(assets_path, asset) for asset in assets]
    return [os.path.join(path, 'perfection.png')] + full_path_assets
