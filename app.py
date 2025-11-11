import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

# --- App Configuration ---
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# SECRET_KEY is required for Flask-WTF (CSRF) and Sessions (Task 3)
app.config['SECRET_KEY'] = 'a-very-secret-and-random-key-you-must-change'

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'students.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# --- Initialize Extensions ---
# Ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

# Import models *after* config, then initialize db
from models import db, Student, User
db.init_app(app)

# Initialize Bcrypt for password hashing (Task 5)
bcrypt = Bcrypt(app)

# Initialize CSRF Protection (Task 3)
csrf = CSRFProtect(app)

# Initialize Login Manager for sessions (Task 3 & 5)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' # Route to redirect to if not logged in
login_manager.login_message_category = 'info' # Bootstrap category for flash message

@login_manager.user_loader
def load_user(user_id):
    """Required callback for Flask-Login to load a user from session."""
    return User.query.get(int(user_id))

# --- Import Forms (Task 1) ---
from forms import StudentForm, RegistrationForm, LoginForm

# --- Public & Authentication Routes ---

@app.route("/home")
def home():
    """Public home page."""
    return render_template('home.html')

@app.route("/register", methods=["GET", "POST"])
def register():
    """User Registration Route (Task 5)."""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        # Hash the password (Task 5)
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password_hash=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    """User Login Route (Task 5)."""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
        
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        # Check password hash (Task 5)
        if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Login successful!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check username and password.', 'danger')
            
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    """User Logout Route."""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

# --- Student CRUD Routes (Now Protected) ---

@app.route('/', methods=['GET', 'POST'])
@login_required # Protect this dashboard (Task 3 & 5)
def index():
    """
    Main dashboard: Shows student list and handles adding new students.
    Combined original '/' and '/add' routes.
    """
    # Use WTForms for validation (Task 1) and CSRF (Task 3)
    form = StudentForm()
    
    # Handle adding a student (POST)
    if form.validate_on_submit():
        new_student = Student(
            roll_no=form.roll_no.data,
            name=form.name.data,
            email=form.email.data,
            course=form.course.data
        )
        db.session.add(new_student)
        db.session.commit()
        flash('Student added successfully!', 'success')
        return redirect(url_for('index'))

    # Handle displaying the page (GET)
    # Use SQLAlchemy ORM (Task 2: Parameterized Queries)
    students = Student.query.all()
    return render_template('index.html', students=students, form=form)

@app.route('/delete/<int:id>', methods=['POST']) # Changed to POST (Task 3)
@login_required
def delete_student(id):
    """
    Handles deleting a student.
    MUST be a POST request to prevent CSRF (Task 3).
    """
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    flash('Student deleted.', 'success')
    return redirect(url_for('index'))

@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update_student(id):
    """Handles updating an existing student."""
    student = Student.query.get_or_404(id)
    
    # Use WTForms, pre-populating with existing student data (Task 1 & 3)
    form = StudentForm(obj=student)
    
    if form.validate_on_submit():
        # Update fields from the validated form
        student.roll_no = form.roll_no.data
        student.name = form.name.data
        student.email = form.email.data
        student.course = form.course.data
        db.session.commit()
        flash('Student updated successfully!', 'success')
        return redirect(url_for('index'))
    
    # On GET request, render the update page with the pre-filled form
    return render_template('update.html', form=form, student=student)

# --- Error Handlers (Task 4) ---

@app.errorhandler(404)
def error_404(error):
    """Custom 404 error page to prevent information disclosure."""
    return render_template('404.html'), 404

@app.errorhandler(500)
def error_500(error):
    """Custom 500 error page to prevent information disclosure."""
    db.session.rollback() # Rollback any failed DB transactions
    return render_template('500.html'), 500

# --- Run Application ---
if __name__ == '__main__':
    with app.app_context():
        db.create_all() # Create database tables
    # debug=True should be False in production (Task 4)
    app.run(debug=True)