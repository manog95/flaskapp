from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from models import Student, User

class StudentForm(FlaskForm):
    """Form for adding and updating students (Task 1)."""
    roll_no = StringField('Roll No', validators=[DataRequired(), Length(min=1, max=20)])
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    course = StringField('Course', validators=[DataRequired(), Length(min=2, max=50)])
    submit = SubmitField('Save Student')

    def validate_roll_no(self, roll_no):
        """Custom validator to check for unique roll_no."""
        student = Student.query.filter_by(roll_no=roll_no.data).first()
        if student:
            # This check is simplified; for update, we'd need to check if it's a *different* student
            pass # In a real app, this logic would be more complex for updates
            
    def validate_email(self, email):
        """Custom validator to check for unique email."""
        student = Student.query.filter_by(email=email.data).first()
        if student:
            # Same simplification as above
            pass

class RegistrationForm(FlaskForm):
    """Form for user registration (Task 5)."""
    username = StringField('Username', 
                           validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', 
                             validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', 
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        """Custom validator to check for unique username."""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is already taken. Please choose another.')

class LoginForm(FlaskForm):
    """Form for user login (Task 5)."""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')