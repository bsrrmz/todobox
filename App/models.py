from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as serializer
from flask import current_app
from App import db, loginManager
from flask_login import UserMixin


@loginManager.user_loader
def loadUser(user_id):
    return users.query.get(int(user_id))

class users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    hash = db.Column(db.String(255), nullable=False)
    gender = db.Column(db.String(22), nullable=False)
    job = db.Column(db.String(255), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='avatar.png')
    createdOn = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    todo_items = db.relationship('todo_items', backref='author', lazy=True)

    def getResetToken(self, expires_sec=1800):
        s = serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')
    
    @staticmethod
    def verifyResetToken(token):
        s = serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return users.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', {self.email}, '{self.gender}', '{self.job}', '{self.createdOn}')"

class todo_items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    createdOn = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    _isDeleted = db.Column(db.Boolean, nullable=False, default=False)
    _isDone = db.Column(db.Boolean, nullable=False, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f"todo_item('{self.title}', '{self.createdOn}')"