from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from extensions import db, bcrypt

auth_bp = Blueprint('auth', __name__, url_prefix='')

def seed_admin_user():
    from models import User
    if not User.query.filter_by(username='admin').first():
        hashed = bcrypt.generate_password_hash('admin123').decode('utf-8')
        user = User(username='admin', password_hash=hashed)
        db.session.add(user)
        db.session.commit()

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    from models import User
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('shipment.list_shipments'))
        flash('Invalid username or password', 'danger')
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully', 'success')
    return redirect(url_for('auth.login'))
