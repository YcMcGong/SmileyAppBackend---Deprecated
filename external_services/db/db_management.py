from flask import jsonify
from flask import Flask, render_template, request, redirect, url_for, flash, current_app
import requests

app = Flask(__name__)
DB_ENDPOINT = 'http://0.0.0.0:5000'


# Routing from here
@app.route('/get_user_management', methods = ['GET', 'POST'])
def get_user():
    if request.method == 'GET':
        user_ID = request.args.get('user_ID')
        if user_ID is None:
            return 'user_ID is not provided'
        data = '?user_ID=' + user_ID
        response = requests.get(DB_ENDPOINT + '/get_user' + data)
        feedback = response.json()
        return jsonify(feedback)

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 7000)