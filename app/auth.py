from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
import pyotp
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password_hash, password):
            flash('Usuario o contraseña inválidos.')
            return redirect(url_for('auth.login'))

        # Si el 2FA está habilitado, redirigir a verificación
        if user.is_2fa_enabled:
            session['pre_2fa_user_id'] = user.id
            return redirect(url_for('auth.verify_2fa'))
        
        # En esta app exigimos 2FA fuertemente. Si no lo tiene, lo obligamos a configurarlo.
        login_user(user, remember=remember)
        return redirect(url_for('auth.setup_2fa'))

    return render_template('login.html')

@auth.route('/verify_2fa', methods=['GET', 'POST'])
def verify_2fa():
    if 'pre_2fa_user_id' not in session:
        return redirect(url_for('auth.login'))
        
    user = User.query.get(session['pre_2fa_user_id'])
    
    if request.method == 'POST':
        token = request.form.get('token')
        totp = pyotp.TOTP(user.totp_secret)
        
        if totp.verify(token):
            login_user(user)
            session.pop('pre_2fa_user_id', None)
            return redirect(url_for('main.index'))
        else:
            flash('Token 2FA inválido.')
            
    return render_template('verify_2fa.html')

@auth.route('/setup_2fa', methods=['GET', 'POST'])
@login_required
def setup_2fa():
    if current_user.is_2fa_enabled:
        return redirect(url_for('main.index'))

    if not current_user.totp_secret:
        current_user.totp_secret = pyotp.random_base32()
        db.session.commit()

    totp = pyotp.TOTP(current_user.totp_secret)
    # Generamos la URI para que el frontend genere el QR usando una librería JS local si es posible, 
    # o como texto plano para evitar depender de Google Charts (sin conexión).
    provisioning_uri = totp.provisioning_uri(name=current_user.username, issuer_name="RetroGamingApp")

    if request.method == 'POST':
        token = request.form.get('token')
        if totp.verify(token):
            current_user.is_2fa_enabled = True
            db.session.commit()
            flash('2FA configurado correctamente.')
            return redirect(url_for('main.index'))
        else:
            flash('El token no es válido, inténtalo de nuevo.')

    return render_template('setup_2fa.html', secret=current_user.totp_secret)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            flash('El usuario ya existe.')
            return redirect(url_for('auth.register'))

        new_user = User(username=username, password_hash=generate_password_hash(password, method='scrypt'))
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registro exitoso. Inicia sesión y configura tu 2FA obligatorio.')
        return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
