
from datetime import datetime
from flask import current_app, request, url_for
from werkzeug import generate_password_hash, check_password_hash
from . import db


class Permission:
    REACT   = 1
    EARN    = 2
    ASK     = 4
    ANSWER  = 8
    VERIFY  = 16


class Role(db.Model):
    
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique = True)
    default = db.Column(db.Boolean, default = False, index = True)
    permissions = db.Column(db.Integer)

    users = db.relationship('User', backref = 'role', lazy = 'dynamic')


    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0


    @staticmethod
    def insert_roles():
        roles = {
                'Unregistered'  : [Permission.REACT],
                'User'          : [Permission.ASK, Permission.ANSWER, 
                                    Permission.EARN, Permission.REACT],

                'Student'       : [Permission.ASK, Permission.ANSWER, 
                                    Permission.EARN, Permission.REACT],
                'MVP'           : [Permission.ASK, Permission.ANSWER, 
                                    Permission.EARN, Permission.REACT, 
                                    Permission.VERIFY],

                'TA'            : [Permission.ASK, Permission.ANSWER, 
                                    Permission.EARN, Permission.REACT,
                                    Permission.VERIFY],
                'RA'            : [Permission.ASK, Permission.ANSWER, 
                                    Permission.EARN, Permission.REACT,
                                    Permission.VERIFY],

                'Staff'         : [Permission.ASK, Permission.ANSWER,
                                    Permission.REACT, Permission.VERIFY],
                'Instructor'    : [Permission.ASK, Permission.ANSWER,
                                    Permission.REACT, Permission.VERIFY],
        }

        default_role = 'Unregistered'

        for r in roles:
            role = Role.query.filter_by(name = r).first()

            if role is None:
                role = Role(name = r)
            
            role.reset_permissions()

            for perm in role[r]:
                role.add_permission(perm)

            role.default = (role.name == default_role)
            db.session.add(role)

        db.session.commit()


    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm


    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm


    def reset_permissions(self):
        self.permissions = 0


    def has_permission(self, perm):
        return self.permissions & perm == perm


    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    slack_id = db.Column(db.String(9), unique = True, index = True)

    username = db.Column(db.String(128), unique = True, index = True) 
    password = db.Column(db.String(128))
    drops = db.Column(db.Integer)

    last_seen = db.Column(db.DateTime(), default = datetime.utcnow)
    created_on = db.Column(db.DateTime(), default = datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default = datetime.utcnow)

    posts = db.relationship('Question', backref = 'author', lazy = 'dynamic')
    answers = db.relationship('Answer', backref = 'author', lazy = 'dynamic') 
    comments = db.relationship('Comment', backref = 'author', lazy = 'dynamic')


    def __init__(self):
        super(User, self).__init__(**kwargs)
        
        if self.role is None:
            self.role = Role.query.filter_by(default=True).first()


    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute.')


    @password.setter
    def password(self, password):
        self.password = generate_password_hash(password)


    def verify_password(self, password):
        return check_password_hash(self.password, password)


class Question(db.Model):

    __tablename__ = 'questions'


class Answer(db.Model):

    __tablename__ = 'answers'


class Comment(db.Model):

    __tablename__ = 'comments'

