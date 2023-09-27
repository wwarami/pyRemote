class TechnicalException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(f'Technical ERROR: {message}')


class UserTriggeredException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(f'User-triggered ERROR: {message}')