# auth.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

# Initialize database if not exists
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            subject TEXT,
            teacher_name TEXT
        )
    ''')
    # Question Papers Table (for generated question papers)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS question_papers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            subject_code TEXT NOT NULL,
            teacher_name TEXT NOT NULL,
            difficulty TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Sign-Up Route
@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        teacher_name = request.form.get('teacher_name') if role == 'teacher' else None
        subject = request.form.get('subject') if role == 'teacher' else None

        hashed_password = generate_password_hash(password)

        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO users (email, password, role, subject, teacher_name)
                VALUES (?, ?, ?, ?, ?)
            ''', (email, hashed_password, role, subject, teacher_name))
            conn.commit()
            conn.close()

            flash('Sign-up successful! Please log in.', 'success')
            return redirect(url_for('auth.login'))
        except sqlite3.IntegrityError:
            flash('Email already exists. Please use a different email.', 'danger')

    return render_template('signup.html')


# Login Route
@auth_bp.route('/', methods=['GET', 'POST'])
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, password, role FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[1], password):
            session['user_id'] = user[0]
            session['role'] = user[2]

            if user[2] == 'teacher':
                return redirect(url_for('teacher_dashboard'))
            else:
                return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid email or password. Please try again.', 'danger')

    return render_template('index.html')

# Logout Route
@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
