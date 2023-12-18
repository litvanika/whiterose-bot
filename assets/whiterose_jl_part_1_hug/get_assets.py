import os


def get_assets(path: str) -> list[str]:
    assets = [
        'whiterose_ruby_sparkling_eyes_glad_to_see_weiss.jpeg',
        'whiterose_justice_league_jump_hug.jpeg',
        'whiterose_justice_league_hug.jpeg',
        'whiterose_jl_part_1_hug_weiss_with_closed_eyes.jpeg',
    ]
    return [os.path.join(path, asset) for asset in assets]
