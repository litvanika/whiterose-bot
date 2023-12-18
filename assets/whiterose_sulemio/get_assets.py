import os


def get_assets(path: str) -> list[str]:
    assets = [
        'whiterose_sulemio.jpg',
    ]
    return [os.path.join(path, asset) for asset in assets]
