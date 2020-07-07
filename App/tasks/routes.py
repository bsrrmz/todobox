# -*- coding: utf-8 -*-
"""Task Route

App.tasks.routes
~~~~~~~~~~~~~~~~~
This package allows the user to create, edit task.

This file can be imported as 'tasks' package and contains the following
routes:

    - task - View tasks templates
    - newTask - Post new task
    - update - Update task
    - delete - Delete task
"""

from flask import render_template, request, url_for, flash, redirect, abort, Blueprint 
from flask_login import current_user, login_required
from App import db
from App.models import todo_items

tasks = Blueprint('tasks', __name__)

@tasks.route("/task")
@login_required     #: Decoretor used for route restriction
def task():
    """Show tasks"""

    # Query database for todo items 
    tasks = todo_items.query.order_by(todo_items.createdOn.desc()).filter_by(user_id=current_user.id).all()
    return render_template('tasks.html', tasks=tasks)


@tasks.route("/task/new", methods=['POST'])
@login_required     #: Decoretor used for route restriction
def newTask():
    """Post new task"""

    title = request.form.get('title')
    description = request.form.get('description')
    
    # Ensure title or description was submitted
    if title or description:

        # Add new todo items to database
        newTask = todo_items(title=title, description=description, author=current_user)
        db.session.add(newTask)
        db.session.commit()
    else:
        flash("Please provide task Title and Description!", "info")
        return redirect(url_for('tasks.task'))

    flash("Task has been added!", "info")
    return redirect(url_for('tasks.task'))


@tasks.route("/task/<int:task_id>/update")
@login_required     #: Decoretor used for route restriction
def update(task_id):
    """Update task
    This route mark a task as complete and viseversa

    :type task_id: int
    :param task_id: Todo items ID 
    """

    # Query todo items for task_id if not fount through 404
    todo = todo_items.query.get_or_404(task_id)

    # Ensure the same author can update
    if todo.author != current_user:
        abort(403)

    # Todo item is not done mark it done 
    if todo._isDone == False:
        todo._isDone = True
        db.session.commit()
        flash("Task has been updated!", "info")

    # Todo item is done mark it not done
    else:
        todo._isDone = False
        db.session.commit()
        flash("Task has been updated!", "info")
        
    return redirect(url_for('tasks.task'))


@tasks.route("/task/<int:task_id>/delete")
@login_required     #: Decoretor used for route restriction
def delete(task_id):
    """Delete task
    
    :type task_id: int
    :param task_id: Todo items ID 
    """

    # Query todo items for task_id if not fount through 404
    todo = todo_items.query.get_or_404(task_id)

    # Ensure the author of the post is current user
    if todo.author != current_user:
        abort(403)

    # Todo item is not deleted it mark it deleted
    todo._isDeleted = True
    db.session.commit()
    flash("Task has been deleted!", "info")
    return redirect(url_for('tasks.task'))




