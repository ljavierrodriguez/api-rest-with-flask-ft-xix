from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)

    created_at = db.Column(db.DateTime(), default=db.func.now())
    updated_at = db.Column(db.DateTime(), default=db.func.now(), onupdate=db.func.now())
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class User(Base):
    __tablename__ = 'users'
    name = db.Column(db.String(120))
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    is_active = db.Column(db.Boolean(), default=True)

    profile = db.relationship('Profile', cascade="all, delete", uselist=False, backref="user") # <Profile 1>
    posts = db.relationship('Post', cascade="all, delete", backref="user", lazy=False) # [<Post 1>, <Post 2>]

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "is_active": self.is_active,
            "total_posts": self.total_posts(),
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    def serialize_with_profile(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "is_active": self.is_active,
            "total_posts": self.total_posts(),
            "titles": self.get_all_post_title(),
            "profile": self.profile.serialize(),
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    def total_posts(self):
        return len(self.posts)

    def get_all_post_title(self):
        return list(map(lambda post: post.title, self.posts))

class Profile(Base):
    __tablename__ = 'profiles'

    biography = db.Column(db.Text(), default="")
    facebook = db.Column(db.String(50), default="")
    twitter = db.Column(db.String(50), default="")
    instagram = db.Column(db.String(50), default="")
    github = db.Column(db.String(50), default="")
    linkedin = db.Column(db.String(50), default="")
    avatar = db.Column(db.Text(), default="")
    users_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, unique=True)

    def serialize(self):
        return {
            "biography": self.biography,
            "facebook": self.facebook,
        }

    def serialize_with_user_name(self):
        return {
            "user": self.user.name,
            "is_active": self.user.is_active,
            "biography": self.biography,
            "facebook": self.facebook
        }

"""
class TagPost(db.Model):
    __tablename__ = 'tags_posts'
    tags_id = db.Column(db.Integer, db.ForeignKey('tags.id'), nullable=False, primary_key=True)
    posts_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False, primary_key=True)
"""

tags_posts = db.Table(
    "tags_posts",
    db.Column("tags_id", db.Integer, db.ForeignKey('tags.id'), nullable=False, primary_key=True),
    db.Column("posts_id", db.Integer, db.ForeignKey('posts.id'), nullable=False, primary_key=True)
)

class Post(Base):
    __tablename__ = 'posts'
    title = db.Column(db.String(255), nullable=False, unique=True) # Hola Mundo
    slug = db.Column(db.String(255), nullable=False, unique=True) # hola-mundo
    content = db.Column(db.Text(), default="", nullable=False)
    date = db.Column(db.DateTime(), default=db.func.now())
    is_published = db.Column(db.Boolean(), default=False)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    #tags = db.relationship('Tag', secondary="tags_posts")
    tags = db.relationship('Tag', secondary=tags_posts, lazy=False)

    def serialize(self):
        return {
            "id": self.id,
            "title":self.title,
            "slug": self.slug,
            "content": self.content,
            "date": self.date,
            "is_published": self.is_published,
            "users_id": self.users_id,
            "author": self.user.name,
            "tags": self.get_tags(),
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    def get_tags(self):
        return list(map(lambda tag: tag.name, self.tags ))

class Tag(Base):
    __tablename__ = 'tags'
    name = db.Column(db.String(30), nullable=False, unique=True)

    #posts = db.relationship('Post', secondary="tags_posts")
    posts = db.relationship('Post', secondary=tags_posts, lazy=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }



 