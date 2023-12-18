import logging
import logging.handlers
import requests


def log(response: requests.Response | Exception, assets: list[str] | None = None) -> None:
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
        logger.error(f'Failed to upload media: {assets}: {response}')
    else:
        default_message = f'{response.status_code}: {response.reason}'
        if response.status_code // 100 == 2:
            json = response.json()
            if 'data' in json and 'id' in json['data']:
                tweet_id = json['data']['id']
                logger.info(
                    f'Created a tweet with media: {assets} and id {tweet_id}: '
                    f'https://twitter.com/1715435861431451648/status/{tweet_id}/')
            else:
                logger.info(f'Uploaded media: {assets}: {default_message}')
        elif response.status_code // 100 == 3:
            logger.warn(f'Tried to upload media: {assets}: {default_message}')
        else:
            logger.error(f'Failed to upload media: {assets}: {default_message}')
