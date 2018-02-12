# coding=utf-8
from flask import jsonify
from flask import Flask, render_template, request, redirect, url_for, flash, current_app

app = Flask(__name__)

# Routing from here
@app.route('/', methods=['GET', 'POST'])
def test():
    return jsonify({'one':1, 'two':2})

if __name__ == '__main__':
    # app.debug = True
    app.run(host = '0.0.0.0', port = 5000)