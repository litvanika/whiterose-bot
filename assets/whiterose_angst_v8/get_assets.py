import os


def get_assets(path: str) -> list[str]:
    assets = [
        'whiterose_v8_angst_1.png',
        'whiterose_v8_angst_2.png',
    ]
    return [os.path.join(path, asset) for asset in assets]
