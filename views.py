from flask import render_template, request, redirect, url_for, flash, send_file, jsonify, session
from models import db, User, Transaction, Admin
from flask_login import login_user, logout_user, login_required, current_user
from flask_babel import gettext as _
import csv
from io import BytesIO, StringIO
from datetime import datetime
from flask_wtf.csrf import CSRFProtect

def register_routes(app):
    csrf = CSRFProtect(app)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            user_id = request.form.get('user_id')
            print(f"request.form.get: {user_id}")
            if not user_id:
                flash(_('Please enter a valid vly_User_ID'), 'error')
                return redirect(url_for('register'))
            
            existing_user = User.query.filter_by(vly_user_id=user_id).first()
            if existing_user:
                flash(_('User ID already registered'), 'error')
                return redirect(url_for('register'))
            
            new_user = User(
                vly_user_id=user_id,
                )
            db.session.add(new_user)
            try:
                db.session.commit()
                flash(_('Registration successful!'), 'success')
                return redirect(url_for('leaderboard'))
            except Exception as e:
                db.session.rollback()
                print(f"Database error: {str(e)}")  # 具体的なDBエラーを確認
                flash(_('Error registering user. Please try again.'), 'error')
                return redirect(url_for('register'))
        
        return render_template('register.html')

    @app.route('/admin/login', methods=['GET', 'POST'])
    def admin_login():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            admin = Admin.query.filter_by(username=username).first()
            
            if admin and admin.check_password(password):
                login_user(admin)
                flash(_('Login successful!'), 'success')
                return redirect(url_for('leaderboard'))
            
            flash(_('Invalid username or password'), 'error')
        return render_template('admin_login.html')

    @app.route('/admin/logout')
    @login_required
    def admin_logout():
        logout_user()
        flash(_('Logged out successfully'), 'success')
        return redirect(url_for('index'))

    @app.route('/admin/profile')
    @login_required
    def admin_profile():
        return render_template('admin_profile.html')

    @app.route('/admin/profile/update-username', methods=['POST'])
    @login_required
    def admin_update_username():
        new_username = request.form.get('new_username')
        if not new_username:
            flash(_('Username cannot be empty'), 'error')
            return redirect(url_for('admin_profile'))
        
        try:
            current_user.update_username(new_username)
            db.session.commit()
            flash(_('Username updated successfully'), 'success')
        except ValueError as e:
            flash(_(str(e)), 'error')
        except Exception as e:
            db.session.rollback()
            flash(_('Error updating username'), 'error')
        
        return redirect(url_for('admin_profile'))

    @app.route('/admin/profile/update-password', methods=['POST'])
    @login_required
    def admin_update_password():
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        if not current_user.check_password(current_password):
            flash(_('Current password is incorrect'), 'error')
            return redirect(url_for('admin_profile'))
        
        if new_password != confirm_password:
            flash(_('New passwords do not match'), 'error')
            return redirect(url_for('admin_profile'))
            
        try:
            current_user.set_password(new_password)
            db.session.commit()
            flash(_('Password updated successfully'), 'success')
        except ValueError as e:
            flash(_(str(e)), 'error')
        except Exception as e:
            db.session.rollback()
            flash(_('Error updating password'), 'error')
        
        return redirect(url_for('admin_profile'))

    @app.route('/set-language/<lang>')
    def set_language(lang):
        session['lang'] = lang
        return redirect(request.referrer or url_for('index'))

    @app.route('/leaderboard')
    @login_required
    def leaderboard():
        try:
            transactions_vly_user_id = Transaction.query.order_by(Transaction.tx_count.desc()).limit(10).all()
            transactions_count = Transaction.query.order_by(Transaction.tx_count.desc()).limit(10).all()
            transactions_last_updated = Transaction.query.order_by(Transaction.tx_count.desc()).limit(10).all()

            
            count_data = [{'vly_user_id': t.vly_user_id, 'tx_count': t.tx_count} for t in transactions_count]
            
            return render_template('leaderboard.html', 
                               transactions_points=count_data,
                               transactions_count=count_data,
                               transactions_amount=count_data)
                               
                       
        except Exception as e:
            print(f"Leaderboard error: {str(e)}")  # ターミナルにエラー詳細を出力
            app.logger.error(f"Leaderboard error: {str(e)}")  # ログファイルにエラー詳細を記録
            flash(_('Error loading leaderboard data.'), 'error')
            return redirect(url_for('index'))
    
