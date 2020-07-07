# -*- coding: utf-8 -*-
#Copyright (c) 2020
"""
This is a simple Todo Application

the aim was to get more familiar with flask and build user-friendly Todo App.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from App import config

# Configure SQLAlchemy to use database
db = SQLAlchemy()


# Configure Bcrypt to hash passwords
bcrypt = Bcrypt()

# Config LoginManager to use sessions and authintication
loginManager = LoginManager()
loginManager.login_view = 'user.login'
loginManager.login_message_category = 'info'

#: Initialize mail from flask-mail
mail = Mail()

def createApp(configClass=config):
    """
    create and configure the app.

    :type Config: Config
    :param Config: values for certain config options.
    :returns: Flask 'App'
    """

    # Configure application
    app = Flask(__name__)

    #: load the config if passed in
    if app.config['ENV'] == 'production':
        app.config.from_object(config.productionConfig)
    else:
        app.config.from_object(config.developmentConfig)

    #: Initialize application for the use with database setup
    db.init_app(app)
    bcrypt.init_app(app)
    loginManager.init_app(app)
    mail.init_app(app)

    #: register route blueprints
    from App.users.routes import user
    from App.tasks.routes import tasks
    from App.main.routes import main 
    from App.errors.handlers import errors
    app.register_blueprint(user)
    app.register_blueprint(tasks)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app