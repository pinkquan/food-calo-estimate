from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from database.models import User
from config.database import users
from bson import ObjectId

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Kiểm tra user đã tồn tại
        if users.find_one({"email": email}):
            flash('Email đã được đăng ký')
            return redirect(url_for('auth.register'))

        # Tạo user mới
        password_hash = generate_password_hash(password)
        new_user = User(username=username, email=email, password_hash=password_hash)
        user_dict = new_user.to_dict()
        result = users.insert_one(user_dict)
        
        # Gán ID cho user và login
        new_user._id = result.inserted_id
        login_user(new_user)
        
        return redirect(url_for('index'))

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user_data = users.find_one({"email": email})
        if user_data and check_password_hash(user_data['password_hash'], password):
            user = User(
                username=user_data['username'],
                email=user_data['email'],
                password_hash=user_data['password_hash'],
                _id=user_data['_id']
            )
            login_user(user)
            return redirect(url_for('index'))
        
        flash('Email hoặc mật khẩu không đúng')
        return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))