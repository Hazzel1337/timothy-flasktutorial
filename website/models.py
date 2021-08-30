from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    posts = db.relationship("Post", backref="user", passive_deletes= True)
    comments = db.relationship("Comment", backref="user",passive_deletes=True)#connects the post to the user ?!
    likes = db.relationship("Like", backref="user",passive_deletes=True)#connects the post to the user ?!


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable= False) #foreign key references the User db model and the id key, must be lowercase in this case, CASCADE deletes everything in this db when the user gets deleted
    comments = db.relationship('Comment', backref='post', passive_deletes=True)
    likes = db.relationship("Like", backref="post",passive_deletes=True)#connects the post to the user ?!


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable= False) #foreign key references the User db model and the id key, must be lowercase in this case, CASCADE deletes everything in this db when the user gets deleted
    post_id = db.Column(db.Integer, db.ForeignKey("post.id", ondelete="CASCADE"), nullable= False) #foreign key references the User db model and the id key, must be lowercase in this case, CASCADE deletes everything in this db when the user gets deleted


class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable= False) #foreign key references the User db model and the id key, must be lowercase in this case, CASCADE deletes everything in this db when the user gets deleted
    post_id = db.Column(db.Integer, db.ForeignKey("post.id", ondelete="CASCADE"), nullable= False) #foreign key references the User db model and the id key, must be lowercase in this case, CASCADE deletes everything in this db when the user gets deleted
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
