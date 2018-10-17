

class UserCreated(object):

    def __init__(self, user_id):
        self.status_code = 201
        self.message = 'User Created'
        self.user_id = user_id

    def to_dict(self):
        return {'StatusCode': self.status_code,
                'Message': self.message,
                'Payload': {'Id': self.user_id}}


class HistoryCreated(object):

    def __init__(self):
        self.status_code = 201
        self.message = 'History Created'

    def to_dict(self):
        return {'StatusCode': self.status_code,
                'Message': self.message,
                'Payload': {}}