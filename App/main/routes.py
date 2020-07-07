# -*- coding: utf-8 -*-
"""Main Route

App.main.routes
~~~~~~~~~~~~~~~~~
This package show portfolio of TodoBox application.

This file can be imported as 'main' package and contains the following
routes:

    - home - View portfolio/home templates
"""

from flask import render_template, redirect, url_for, Blueprint
from flask_login import current_user

main = Blueprint('main', __name__)

@main.route("/")
def home():
    """View portfolio/home templates"""
  
    # If user is authenticated return tasks
    if current_user.is_authenticated:
        return redirect(url_for('tasks.task'))

    return render_template("index.html")