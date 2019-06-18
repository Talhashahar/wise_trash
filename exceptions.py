class SMSSendError(Exception):
    def __init__(self, message):
        super().__init__(message)


class InvalidCredentials(Exception):
    def __init__(self, user='', password=''):
        super().__init__(f'Invalid Credentials {user} {password}')


class UserNotExists(Exception):
    def __init__(self, user=''):
        super().__init__(f'User {user} not exists')


class UserNotVerified(Exception):
    def __init__(self, user=''):
        super().__init__(f'Account {user} is not verified')


class TokenNotExists(Exception):
    def __init__(self):
        super().__init__('Missing token')


class PuzzleNotExists(Exception):
    def __init__(self, user=''):
        super().__init__(f'Puzzle not exists for user {user}')


class WrongAnswer(Exception):
    def __init__(self, user=''):
        super().__init__(f'Wrong answer submitted for user {user}')


class EmptyForm(Exception):
    def __init__(self):
        super().__init__(f'Missing form data')


class UserAlreadyExists(Exception):
    def __init__(self, user=''):
        super().__init__(f'User {user} already exists')


class EmptyBalance(Exception):
    def __init__(self, message):
        super().__init__(message)


class PasswordInvalid(Exception):
    def __init__(self):
        super().__init__('Password is not matching the requirements')
