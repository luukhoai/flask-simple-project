from settings.settings import app
from models.users import User
from models.histories import Histories
from http_codes.exceptions import UserNotFound


def create_user(form):
    """
    Create an user
    :param form: eg: form
    :return: user
    """
    user = User(name=form['username'])
    user.save()
    return user


def login_user(form, user_id):
    """
    Generate
    :param form:
    :return:
    """
    if 'day' in form:
        # Need check permission of user.
        history = Histories(day=form['day'])
    else:
        history = Histories()
    history.append(user_id)
    return history

def validate_user(user_id):
    """
    Check user exist or not, raise Error if not found
    :param user_id:
    :return: user
    """
    user = User.get_user(user_id)
    if not user:
        raise UserNotFound()
    return user


def get_users_detail(users):
    """
    Get list users detail
    :param users: list of user_id eg: ['user_1', 'user_2', ...]
    :return:
    """
    response = {}
    for user_id in users:
        name = User.get_user(user_id)
        response[user_id] = name
    return response


def users_presence(day):
    """
    Get list of user presence of day
    :param day: day_id eg: 'histories_1'
    :return:
    """
    history = Histories(day)
    users = history.get_history_of_day()
    return get_users_detail(users)


def users_absence(day):
    """
    Get list of user absence of day
    :param day: day_id eg: 'histories_1'
    :return:
    """
    absence_list = []
    presence_user = users_presence(day)
    user_list = app.db.scan('user_*')
    for each_user in user_list:
        if each_user not in presence_user:
            absence_list.append(each_user)
    return get_users_detail(absence_list)


def users_presence_consecutive():
    """
    Get list of user presence consecutive
    :return:
    """
    precence_consecutive_list = []
    history_list = app.db.scan('histories_*')
    precence_day_1 = None
    i = 0
    while i < (len(history_list) - 1):
        if precence_day_1 is None:
            precence_day_1 = users_presence(history_list[i])
        precence_day_2 = users_presence(history_list[i+1])

        for each_user in precence_day_1:
            if each_user in precence_day_2:
                precence_consecutive_list.append(each_user)
        precence_day_1 = precence_day_2
        i += 1
    list_users_presence = list(set(precence_consecutive_list))
    return get_users_detail(list_users_presence)


def users_absence_consecutive():
    """
    Get list of user absence consecutive
    :return:
    """
    absence_consecutive_list = []
    history_list = app.db.scan('histories_*')
    absence_day_1 = None
    i = 0
    while i < (len(history_list) - 1):
        if absence_day_1 is None:
            absence_day_1 = users_absence(history_list[i])
        absence_day_2 = users_absence(history_list[i+1])

        for each_user in absence_day_1:
            if each_user in absence_day_2:
                absence_consecutive_list.append(each_user)
        absence_day_1 = absence_day_2
        i += 1
    list_users_absence = list(set(absence_consecutive_list))
    return get_users_detail(list_users_absence)





