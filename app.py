import os
from flask import Flask, redirect, url_for
from extensions import db, login_manager, bcrypt

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-me')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shipment.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    login_manager.login_view = 'auth.login'

    from auth import auth_bp, seed_admin_user
    from shipment import shipment_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(shipment_bp)

    with app.app_context():
        from models import User, Shipment
        db.create_all()
        seed_admin_user()

    @app.route('/')
    def index():
        from flask_login import current_user
        if current_user.is_authenticated:
            return redirect(url_for('shipment.list_shipments'))
        return redirect(url_for('auth.login'))

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
