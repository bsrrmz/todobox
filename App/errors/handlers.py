# -*- coding: utf-8 -*-
"""Error Route

App.errors.handlers
~~~~~~~~~~~~~~~~~
This package handles errors.

This file can be imported as 'errors' package and contains the following
routes:

    - error404 - Page not found Error
    - error403 - Forbidden Error
    - error500 - Internal Server Error
"""

from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def error404(error):
    """Page not found."""
    return render_template('errors/404.html'), 404

@errors.app_errorhandler(403)
def error403(error):
    """Forbidden Error"""
    return render_template('errors/403.html'), 403

@errors.app_errorhandler(500)
def error500(error):
    """Internal Server Error"""
    return render_template('errors/500.html'), 500

@errors.app_errorhandler(405)
def error405(error):
    """Method Not Allowed"""
    return render_template('errors/405.html'), 405