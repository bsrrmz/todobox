# -*- coding: utf-8 -*-
#Copyright (c) 2020
"""Users Utilities

App.users.utils
~~~~~~~~~~~~~~~~~
This package contain methods for user.

This file can be imported as a package and contains the following
routes:

    - savePicture - save user profile picture
    - sendResetEmail - send password reset request to user's email address if request
"""

import secrets
import os
from PIL import Image
from flask import url_for, current_app
from App import mail
from flask_mail import Message
from App import mail


def savePicture(avatar):
    """
    Save picture to static/avatars folder.

    :type avatar: files
    :param avatar: Image file to save.

    :rtype str
    :returns: Image name with its extension
    """

    # Generate 8 bytes random string in hexadecimal
    random_hex = secrets.token_hex(8)

    _, fileExt = os.path.splitext(avatar.filename)
    picFileName = random_hex + fileExt
    picPath = os.path.join(current_app.root_path, 'static/avatars', picFileName)

    # Pillow Image module open method
    # Opens and identifies the given image file.
    i = Image.open(avatar)
    
    # Image size
    outputSize = (125, 125)
    # This method modifies the image to contain a thumbnail version of itself, no larger than the given size.
    i.thumbnail(outputSize)

    i.save(picPath)

    return picFileName


def sendResetEmail(user):
    """
    Send password reset request to user's email address if request.

    :type user: user
    :param user: user details such as email address and token.
    """

    # get user token
    token = user.getResetToken()

    # message from and recipients
    msg = Message('Password Reset Request', 
                    sender='todoboxcs50@gmail.com', 
                    recipients=[user.email])
    
    # message body with absolute url path
    msg.body = f'''To reset your password, visit the following link:
{url_for('user.resetToken', token=token, _external=True)}
    
If you did not make this request then simply ignore this email.
'''
    # send email
    mail.send(msg)