import os


def get_assets(path: str) -> list[str]:
    assets = [
        'whiterose_shocked_1.png',
        'whiterose_shocked_2.png',
    ]
    return [os.path.join(path, asset) for asset in assets]
