from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User

@app.route('/')
def index():
    return redirect ('/users')

@app.route("/users")
def users():
    users = User.get_all()
    print(users)
    return render_template("read_all.html", users = users)

@app.route('/users/create_new')
def new_user():
    return render_template("create.html")

@app.route('/users/create_new/add_user', methods=['POST'])
def add_new_user():
    if not User.validate_user(request.form):
        return redirect ('/users/create_new')
    else:
        User.create_user(request.form)
        return redirect ('/users')

@app.route('/users/user/<int:user_id>')
def user(user_id):
    user = User.get_one(user_id)
    return render_template('read_one.html', user = user)

@app.route('/users/user/update/<int:user_id>')
def update_user(user_id):
    user = User.get_one(user_id)
    return render_template('update.html', user = user)

@app.route('/users/user/update/edit', methods=['POST'])
def edit_user():
    User.update_user(request.form)
    return redirect('/users')

@app.route('/users/delete/<int:user_id>')
def delete(user_id):
    User.delete_user(user_id)
    return redirect('/')