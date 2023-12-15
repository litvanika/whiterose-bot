import logging
import logging.handlers
import os
import random
import requests
import tweepy

from errors import IncorrectLengthError


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


def get_random_medias() -> list[str]:
    path = 'assets'
    objects = os.listdir(path)

    media = random.choice(objects)
    media_path = os.path.join(path, media)
    if os.path.isfile(media_path):
        return [media_path]
    
    medias = os.listdir(media_path)
    if 'order.txt' not in medias:
        raise FileNotFoundError(f'`order.txt` must exists inside `{media_path}`')
    if len(medias) < 2 or len(medias) > 5: # +1 file for order.txt
        raise IncorrectLengthError(media_path)
    
    with open(os.path.join(media_path, 'order.txt'), 'r') as order_file:
        medias = order_file.readlines()
    
    return [os.path.join(media_path, media) for media in medias]


def tweet(medias: list[str]) -> requests.Response:
    consumer_key = os.environ['CONSUMER_KEY']
    consumer_secret = os.environ['CONSUMER_SECRET']
    access_token = os.environ['ACCESS_TOKEN']
    access_token_secret = os.environ['ACCESS_TOKEN_SECRET']

    api_v1 = auth_v1(consumer_key, consumer_secret,
                     access_token, access_token_secret)
    client_v2 = auth_v2(consumer_key, consumer_secret,
                        access_token, access_token_secret)

    media_ids = [api_v1.media_upload(media).media_id for media in medias]

    return client_v2.create_tweet(media_ids=media_ids)


def log(response: requests.Response | Exception, medias: list[str]):
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

    if isinstance(response, Exception) or not isinstance(response, requests.Response):
        logger.error(f'Failed to upload media: {medias}: response')
    else:
        default_message = f'{response.status_code}: {response.reason}'
        if response.status_code // 100 == 2:
            json = response.json()
            if 'data' in json and 'id' in json['data']:
                tweet_id = json['data']['id']
                logger.info(
                    f'Created a tweet with media: {medias} id {tweet_id}: '
                    f'https://twitter.com/1715435861431451648/status/{tweet_id}/')
            else:
                logger.info(f'Uploaded media: {medias}: {default_message}')
        elif response.status_code // 100 == 3:
            logger.warn(f'Tried to upload media: {medias}: {default_message}')
        else:
            logger.error(f'Failed to upload media: {medias}: {default_message}')


def main():
    medias = get_random_medias()
    try:
        response = tweet(medias)
    except Exception as e:
        log(e, medias)
    else:
        log(response, medias)


if __name__ == '__main__':
    main()
