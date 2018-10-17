from settings.settings import app, logger
from flask import jsonify, request
from databases.redis import RedisManager
from controllers import controllers
from http_codes.exceptions import MobileHealthException
from http_codes.codes import UserCreated, HistoryCreated


@app.before_request
def before_request():
    app.db = RedisManager()


@app.errorhandler(MobileHealthException)
def handle_invalid_usage(error):
    logger.error('Error_handler: {}'.format(error))
    return jsonify(error.to_dict()), error.status_code


@app.route('/')
def index():
    return 'Mobile Health Test'


@app.route('/user/create', methods=['POST'])
def create_user():
    if request.method == 'POST':
        user = controllers.create_user(request.form)
        response = UserCreated(user.user_id)
        return jsonify(response.to_dict()), response.status_code


@app.route('/user/login', methods=['POST'])
def login_user():
    if request.method == 'POST':
        user_id = request.form['user_id']
        controllers.validate_user(user_id)
        controllers.login_user(request.form, user_id)
        response = HistoryCreated()
        return jsonify(response.to_dict()), response.status_code


@app.route('/users/presence/<day>', methods=['GET'])
def users_presence(day):
    users = controllers.users_presence(day)
    return jsonify(users)


@app.route('/users/absence/<day>', methods=['GET'])
def users_absence(day):
    users = controllers.users_absence(day)
    return jsonify(users)


@app.route('/users/presence/consecutive', methods=['GET'])
def users_presence_consecutive():
    users = controllers.users_presence_consecutive()
    return jsonify(users)


@app.route('/users/absence/consecutive', methods=['GET'])
def users_absence_consecutive():
    users = controllers.users_absence_consecutive()
    return jsonify(users)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)