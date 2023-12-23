import os


def get_assets(path: str) -> list[str]:
    assets = [
        'whiterose_storyboard_clip_0.png',
        'whiterose_storyboard_clip_1.png',
        'whiterose_storyboard_clip_2.png',
    ]
    return [os.path.join(path, asset) for asset in assets]
