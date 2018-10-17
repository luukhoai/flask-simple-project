import os
import unittest
import requests
from random import randint
from unittest import TestCase


class UnittestProject(TestCase):

    def setUp(self):
        # Clear redis
        os.system('redis-cli flushall')

        # Add 2 users.
        add_user_url = 'http://localhost:5000/user/create'
        user_1 = requests.post(add_user_url, data={'username': 'User 1'}).json()
        self.user_1_id = user_1['Payload']['Id']
        user_2 = requests.post(add_user_url, data={'username': 'User 2'}).json()
        self.user_2_id = user_2['Payload']['Id']

        # Add 3 histories.
        add_history_url = 'http://localhost:5000/user/login'
        self.history_1 = requests.post(add_history_url, data={'user_id': self.user_1_id, 'day': 'histories_1'}).json()
        self.history_2 = requests.post(add_history_url, data={'user_id': self.user_1_id, 'day': 'histories_2'}).json()
        self.history_3 = requests.post(add_history_url, data={'user_id': self.user_2_id, 'day': 'histories_3'}).json()

    def test_users_presence(self):
        user_presence_url = 'http://localhost:5000/users/presence/{}'

        day = 'histories_1'
        response = requests.get(user_presence_url.format(day)).json()
        assert len(response) == 1
        assert self.user_1_id in response

        day = 'histories_3'
        response = requests.get(user_presence_url.format(day)).json()
        assert len(response) == 1
        assert self.user_2_id in response

    def test_users_absent(self):
        user_absence_url = 'http://localhost:5000/users/absence/{}'

        day = 'histories_1'
        response = requests.get(user_absence_url.format(day)).json()
        assert len(response) == 1
        assert self.user_2_id in response

        day = 'histories_3'
        response = requests.get(user_absence_url.format(day)).json()
        assert len(response) == 1
        assert self.user_1_id in response

    def test_users_presence_consecutive(self):
        user_presence_consecutive_url = 'http://localhost:5000/users/presence/consecutive'
        response = requests.get(user_presence_consecutive_url).json()
        assert len(response) == 1
        assert self.user_1_id in response

    def test_users_absence_consecutive(self):
        user_presence_consecutive_url = 'http://localhost:5000/users/absence/consecutive'
        response = requests.get(user_presence_consecutive_url).json()
        assert len(response) == 1
        assert self.user_2_id in response

    def test_100_users(self):
        # Generate 100 user random
        user_create = 'http://localhost:5000/user/create'
        for i in range(100):
            requests.post(user_create, data={'username': 'User '.format(i)}).json()

        # Generate 100 histories
        add_history_url = 'http://localhost:5000/user/login'
        for i in range(100):
            random = randint(0,1)
            if random == 0:
                requests.post(add_history_url, data={'user_id': 'user_1', 'day': 'histories_1'}).json()
            else:
                requests.post(add_history_url, data={'user_id': 'user_1', 'day': 'histories_2'}).json()

        # User presence_day 1
        users_precense_day_1 = requests.get('http://localhost:5000/users/presence/histories_1').json()
        print(users_precense_day_1)

        # User absence day 2
        users_absence_day_2 = requests.get('http://localhost:5000/users/absence/histories_2').json()
        print(users_absence_day_2)

        # User presence_consecutive
        presence_consecutive_day_2 = requests.get('http://localhost:5000/users/presence/consecutive').json()
        print(presence_consecutive_day_2)

        # User absence_consecutive
        absence_consecutive_day_2 = requests.get('http://localhost:5000/users/absence/consecutive').json()
        print(absence_consecutive_day_2)



if __name__ == '__main__':
    unittest.main()


