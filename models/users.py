from settings.settings import app

user_id = 0


class User(object):

    def __init__(self, name):
        self.user_id = self.generate_id()
        self.name = name

    @staticmethod
    def generate_id():
        """
        Generate user_id
        :return:   eg: user_1
        """
        global user_id
        user_id += 1
        return 'user_{}'.format(user_id)

    @staticmethod
    def get_user(user_id):
        """
        Get user from databbase
        :param user_id: eg: 'user_1'
        :return: name of user.  eg: 'User name'
        """
        return app.db.get(key=user_id)

    def save(self):
        """
        Save user into database
        :return: user
        """
        app.db.set(key=self.user_id, value=self.name)
        return self





