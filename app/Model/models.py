from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash


postTags = db.Table('postTags',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)   
)




class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    happiness_level = db.Column(db.Integer, default = 3)
    body = db.Column(db.String(1500))
    likes = db.Column(db.Integer, default = 0)


    tags = db.relationship('Tag',  secondary = postTags, primaryjoin=(postTags.c.post_id == id),
                           backref=db.backref('postTags', lazy='dynamic'), lazy='dynamic')
    

    def get_tags(self):
        return self.tags

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))


    def __repr__(self):
       return f"<Tag id={self.id} name={self.name}>"
    

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(128))


    def __repr__(self):
        return f"<User id={self.id} username={self.username} email={self.email}>"
    

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    
    def get_password(self):
        return check_password_hash(self.password_hash)