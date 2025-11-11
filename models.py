from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

# Initialize SQLAlchemy
db = SQLAlchemy()

class Student(db.Model):
    """Model for the Student table."""
    id = db.Column(db.Integer, primary_key=True)
    roll_no = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    course = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<Student {self.name}>"

class User(db.Model, UserMixin):
    """Model for the User table (Task 5)."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False) # Store hash, not password

    def __repr__(self):
        return f"<User {self.username}>"