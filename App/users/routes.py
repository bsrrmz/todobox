# -*- coding: utf-8 -*-
"""Users Route

App.users.routes
~~~~~~~~~~~~~~~~~
This package allows the user to authenticate, edit account and logout.

This file can be imported as 'user' package and contains the following
routes:

    - login - Log user in
    - logout - Log user out
    - register - Register new user
    - account - User account
    - resetRequest - Password reset request
    - resetToken - Reset password
"""

import re
from flask import render_template, request, url_for, flash, redirect, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import func 
from App.models import users
from App import db, bcrypt
from App.users.utils import savePicture, sendResetEmail

user = Blueprint('user', __name__)

@user.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    
    # If user is authenticated return tasks
    if current_user.is_authenticated:
        return redirect(url_for('tasks.task'))

    # User reached route via POST (as by submitting a form via POST)
    if request.method == 'POST':
 
        # Regular expression for validating an Email 
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

        # Make sure user exist
        if (re.search(regex, request.form.get('username'))):
            # Query database for email address
            user = users.query.filter_by(email=request.form.get('username')).first()
            if not user:
                flash("Email does not exits", "info") 
                return redirect(url_for('user.login'))
        else:
            # Query database for username
            user = users.query.filter(func.lower(users.username) == func.lower(request.form.get('username'))).first()
            if not user:
                flash("Username does not exits", "info") 
                return redirect(url_for('user.login'))

        # Ensure username exists and password is correct
        if user and bcrypt.check_password_hash(user.hash, request.form.get('user_password')):
            login_user(user)
            flash("login Successful", "info")  
            return redirect(url_for('tasks.task'))
        else:
            flash("Incorrect username or password.", "danger") 
            return redirect(url_for('user.login'))    
    
    return render_template("login.html")


@user.route("/logout")
def logout():
    """Logout user"""

    # Log out user
    logout_user()
    flash("Logout Successfull", "info")
    return redirect(url_for('main.home'))


@user.route("/register", methods=['GET', 'POST'])
def register():
    """Register user"""
    
    # If user is authenticated return tasks
    if current_user.is_authenticated:
        return redirect(url_for('tasks.task'))

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        # Ensure password and confirmation are the same
        if request.form.get("user_password") != request.form.get("password_confirmation"):
            flash("The password did not match", "danger")
            return redirect(url_for('user.register'))

        # Form variables
        username = request.form.get("username")
        email = request.form.get('email')
        password = request.form.get("user_password")
        gender = request.form.get('user_gender')
        userJob = request.form.get('user_job')

        # Generate hash password
        hash = bcrypt.generate_password_hash(password).decode('utf-8')

        # Ensure username does not exist 
        user = users.query.filter_by(username=username).first()
        if user:
            flash("Username exit. Please try another username", "danger")
            return redirect(url_for('user.register'))
        
        # Ensure email address does not exist 
        userEmail = users.query.filter_by(email=email).first()
        if userEmail:
            flash("E-mail address exit. Please try another E-mail address", "danger")
            return redirect(url_for('user.register'))

        # Add user to database
        user = users(username=username, email=email, hash=hash, gender=gender, job=userJob)
        db.session.add(user)
        db.session.commit()
        flash("Register successfull", "info")
        return redirect(url_for("user.login"))
    else:
        return render_template("register.html")


@user.route("/account", methods=['GET', 'POST'])
@login_required 
def account():
    """User account"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == 'POST':

        # Form variables
        username = request.form.get("username")
        email = request.form.get('email')
        password = request.form.get("new_password")
        avatar = request.files['file']

        # Ensure username was submitted
        if username:
            # Query database for username
            user = users.query.filter(func.lower(users.username) == func.lower(username)).first()
            
            # Ensure username does not exist
            if user:
                flash("Username exit. Please try another username", "info")
                return redirect(url_for('user.account'))
            # Update database user's username
            else:
                current_user.username  = username
                db.session.commit()

        # Ensure email was submitted
        if email:      
            
            # Ensure email address match with pattern 'example@example.com'
            regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
            if (re.search(regex, email)):

                # Query database for username
                userEmail = users.query.filter(func.lower(users.email) == func.lower(email)).first()
               
                # Ensure email does not exist
                if userEmail:
                    flash("Email exit. Please try another username", "info")
                    return redirect(url_for('user.account'))
                else:
                    current_user.email  = email
                    db.session.commit()
            else:
                flash("Invalid Email format", "info")
                return redirect(url_for('user.account'))
        
        # Ensure password was submitted
        if password:

            # Ensure password and confirmation are the same
            if request.form.get("new_password") != request.form.get("password_confirmation"):
                flash("The password did not match", "danger")
                return redirect(url_for('user.account'))

            # Ensure old password is correct
            elif bcrypt.check_password_hash(current_user.hash, request.form.get('user_password')):
                hash = bcrypt.generate_password_hash(password).decode('utf-8')
                current_user.hash = hash
                db.session.commit()
            else:
                flash("Wrong password. Try again", "danger")
                return redirect(url_for('user.account'))
        
        # Ensure image was submitted
        if avatar:

            # Save avatar img return img name
            picFile = savePicture(avatar)

            # Update user's image_file
            current_user.image_file  = picFile
            db.session.commit()

        # Make sure to show message if account updated
        if username or email or password or avatar:
            flash("Your account has been updated", "info")
            return redirect(url_for('user.account'))

    # User image file 'avatar'
    image_file = url_for('static', filename='avatars/' + current_user.image_file)
    return render_template('account.html', avatar=image_file)


@user.route("/reset_password", methods=['GET', 'POST'])
def resetRequest():
    """Password reset request
    This route send reset password to user's email address if exists.
    """

    # If user is authenticated return tasks
    if current_user.is_authenticated:
        return redirect(url_for('tasks.task'))
    
    # User reached route via POST (as by submitting a form via POST)
    if request.method == 'POST':

        # Query database for email
        user = users.query.filter_by(email=request.form.get('email')).first()
       
       # Make sure email does not exist
        if user is None:
            flash('Email does not exit! Create an account.', 'info')
            return redirect(url_for('user.resetRequest'))
        
        # For this method check users/utils.py 
        # Send reset password email with valid token 
        sendResetEmail(user)
        flash('An email has been sent to reset your password', 'info')
        return redirect(url_for('user.login'))

    return render_template('reset_request.html')


@user.route("/reset_password/<token>", methods=['GET', 'POST'])
def resetToken(token):
    """Reset password
    Render reset_token.html template with valid token sent to user's email

    :type token: str
    :param token: password reset request token

    """

    # If user is authenticated return tasks
    if current_user.is_authenticated:
        return redirect(url_for('task.task'))
    
    # Verify token
    user = users.verifyResetToken(token)

    # Ensure valid token
    if user is None:
        flash('That is an invalid or expired token', 'info')
        return redirect(url_for('user.resetRequest'))

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":  

        # Ensure password and password confirmation are the same   
        if request.form.get("new_password") != request.form.get("password_confirmation"):
            flash("The password did not match", "danger")
            return redirect(url_for('user.resetToken'))
        
        # hash and update password
        hash = bcrypt.generate_password_hash(request.form.get("new_password")).decode('utf-8')
        user.hash = hash
        db.session.commit()
        flash('Your password has been updated!', 'info')
        return redirect(url_for('user.login'))

    return render_template('reset_token.html', token=token)
