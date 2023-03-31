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

    profile = db.relationship('Profile', uselist=False, backref="user") # <Profile 1>

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "is_active": self.is_active,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    def serialize_with_profile(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "is_active": self.is_active,
            "profile": self.profile.serialize(),
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }


class Profile(Base):
    __tablename__ = 'profiles'

    biography = db.Column(db.Text(), default="")
    facebook = db.Column(db.String(50), default="")
    twitter = db.Column(db.String(50), default="")
    instagram = db.Column(db.String(50), default="")
    github = db.Column(db.String(50), default="")
    linkedin = db.Column(db.String(50), default="")
    avatar = db.Column(db.Text(), default="")
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)

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
    
