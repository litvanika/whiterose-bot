import os


def get_assets(path: str) -> list[str]:
    assets = [
        'whiterose_justice_league_jump_hug.jpeg',
        'whiterose_justice_league_hug.jpeg',
    ]
    return [os.path.join(path, asset) for asset in assets]
