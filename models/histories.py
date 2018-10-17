from settings.settings import app
from datetime import datetime


class Histories(object):

    def __init__(self, day=None):
        if day:
            self.key = day
        else:
            self.key = 'histories_{}'.format(self.get_current_date())

    def get_current_date(self):
        """Get current_date"""
        return datetime.today().strftime('%Y_%m_%d')

    def get_history_of_day(self):
        """
        Get histories of this day
        :return: list of user logged-in,  eg: ['user_1', ...]
        """
        histories_day = app.db.get(self.key)
        if not histories_day:
            histories_day = []
        return histories_day

    def set_history_of_day(self, histories):
        """
        Set histories of this day
        :param histories: list of user logged-in,  eg: ['user_1', ....]
        :return: True
        """
        app.db.set(self.key, histories)
        return True

    def append(self, user_id):
        """
        Add user_id logged-in into histories
        :param user_id:   eg: user_1
        :return: True
        """
        histories_current_day = self.get_history_of_day()
        histories_current_day.append(user_id)
        self.set_history_of_day(histories_current_day)
        return True