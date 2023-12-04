from flask import jsonify, render_template, Blueprint, request, flash, redirect, url_for
from .models import add_user

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return jsonify({'message': 'Hello, World!'})


@main.route('/add', methods=['POST'])
def add_user_view():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        flash("Username and password are required.")
        return redirect(url_for('main.some_page'))

    try:
        add_user({'username': username, 'password': password})
        flash("User added successfully.")
    except Exception as e:
        flash(str(e))

    return redirect(url_for('main.some_confirmation_page'))
