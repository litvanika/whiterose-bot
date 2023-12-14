class IncorrectLengthError(Exception):
    def __init__(self, media_path: str) -> None:
        super().__init__(f'There must 1 to 4 assets inside `{media_path}`')