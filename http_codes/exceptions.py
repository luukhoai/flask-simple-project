class MobileHealthException(Exception):

    def __init__(self):
        pass


class UserNotFound(MobileHealthException):
    status_code = 404
    message = 'User not Found'

    def to_dict(self):
        return {'StatusCode': self.status_code,
                'message': self.message}