import importlib
import importlib.machinery
import importlib.util
import os
import random
import requests
import tweepy

from log import log
from webp_to_gif import convert_all_webp_to_gif


def get_assets(path: str) -> list[str]:
    loader = importlib.machinery.SourceFileLoader('get_assets', os.path.join(path, 'get_assets.py'))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    assets_module = importlib.util.module_from_spec(spec)
    loader.exec_module(assets_module)
    return assets_module.get_assets(path)


def get_random_assets() -> list[str]:
    path = 'assets'
    all_assets = os.listdir(path)

    random.shuffle(all_assets)
    asset = random.choice(all_assets)

    asset_path = os.path.join(path, asset)
    if os.path.isfile(asset_path):
        return [asset_path]
    
    if not os.path.isfile(os.path.join(asset_path, 'get_assets.py')):
        raise FileNotFoundError(f'`get_assets.py` must exist inside `{asset_path}`')
    
    return get_assets(asset_path)


def auth_v1(consumer_key, consumer_secret, access_token, access_token_secret) -> tweepy.API:
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return tweepy.API(auth)


def auth_v2(consumer_key, consumer_secret, access_token, access_token_secret) -> tweepy.Client:
    return tweepy.Client(
        consumer_key=consumer_key, consumer_secret=consumer_secret,
        access_token=access_token, access_token_secret=access_token_secret,
        return_type=requests.Response,
    )


def tweet(assets: list[str]) -> requests.Response:
    consumer_key = os.environ['CONSUMER_KEY']
    consumer_secret = os.environ['CONSUMER_SECRET']
    access_token = os.environ['ACCESS_TOKEN']
    access_token_secret = os.environ['ACCESS_TOKEN_SECRET']

    api_v1 = auth_v1(consumer_key, consumer_secret,
                     access_token, access_token_secret)
    client_v2 = auth_v2(consumer_key, consumer_secret,
                        access_token, access_token_secret)

    media_ids = [api_v1.media_upload(asset).media_id_string for asset in assets]

    return client_v2.create_tweet(media_ids=media_ids)


def main():
    assets = None
    try:
        convert_all_webp_to_gif()
        assets = get_random_assets()
        response = tweet(assets)
    except Exception as e:
        log(e, assets)
    else:
        log(response, assets)


if __name__ == '__main__':
    main()
