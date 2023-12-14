import logging
import logging.handlers
import os
import random
import requests
import tweepy


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


def get_random_media() -> str:
    path = 'assets'
    objects = os.listdir(path)
    media = random.choice(objects)
    return os.path.join(path, media)


def tweet() -> requests.Response:
    consumer_key = os.environ('CONSUMER_KEY')
    consumer_secret = os.environ('CONSUMER_SECRET')
    access_token = os.environ('ACCESS_TOKEN')
    access_token_secret = os.environ('ACCESS_TOKEN_SECRET')

    api_v1 = auth_v1(consumer_key, consumer_secret,
                     access_token, access_token_secret)
    client_v2 = auth_v2(consumer_key, consumer_secret,
                        access_token, access_token_secret)

    media = get_random_media()
    media_id = api_v1.media_upload(media).media_id

    return client_v2.create_tweet(media_ids=[media_id])


def log(response: requests.Response | Exception):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger_file_handler = logging.handlers.RotatingFileHandler(
        "status.log",
        maxBytes=1024 * 1024,
        backupCount=1,
        encoding="utf8",
    )
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    logger_file_handler.setFormatter(formatter)
    logger.addHandler(logger_file_handler)

    if response is Exception or response is not requests.Request:
        logger.error(response)
    else:
        default_message = f'{response.status_code}: {response.reason}'
        if response.status_code // 100 == 2:
            data = response.json()
            if 'id' in data:
                tweet_id = data['id']
                logger.info(
                    f'Tweeted a tweet with id {tweet_id}: https://twitter.com/WhiteRoseBot/status/{tweet_id}/')
            else:
                logger.info(default_message)
        elif response.status_code // 100 == 3:
            logger.warn(default_message)
        elif response.status_code == 418:  # Error 418 - I'm a teapot
            logger.info(default_message)
        else:
            logger.error(default_message)


def main():
    try:
        response = tweet()
    except Exception as e:
        log(e)
    else:
        log(response)


if __name__ == '__main__':
    main()
