from flask import render_template, request, redirect, url_for, flash, send_file
from models import db, User, Transaction
import csv
from io import BytesIO, StringIO
from datetime import datetime

def register_routes(app):
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            user_id = request.form.get('user_id')
            if not user_id:
                flash('Please enter a valid User ID', 'error')
                return redirect(url_for('register'))
            
            existing_user = User.query.filter_by(id=user_id).first()
            if existing_user:
                flash('User ID already registered', 'error')
                return redirect(url_for('register'))
            
            new_user = User(id=user_id)
            db.session.add(new_user)
            try:
                db.session.commit()
                flash('Registration successful!', 'success')
                return redirect(url_for('leaderboard'))
            except Exception as e:
                db.session.rollback()
                flash('Error registering user. Please try again.', 'error')
                return redirect(url_for('register'))
        
        return render_template('register.html')

    @app.route('/leaderboard')
    def leaderboard():
        try:
            transactions_points = Transaction.query.order_by(Transaction.points.desc()).limit(10).all()
            transactions_count = Transaction.query.order_by(Transaction.count.desc()).limit(10).all()
            transactions_amount = Transaction.query.order_by(Transaction.amount.desc()).limit(10).all()
            return render_template('leaderboard.html', 
                                transactions_points=transactions_points,
                                transactions_count=transactions_count,
                                transactions_amount=transactions_amount)
        except Exception as e:
            flash('Error loading leaderboard data.', 'error')
            return redirect(url_for('index'))

    @app.route('/transaction-history', methods=['GET', 'POST'])
    def transaction_history_search():
        if request.method == 'POST':
            user_id = request.form.get('user_id')
            if not user_id:
                flash('Please enter a valid User ID', 'error')
                return redirect(url_for('transaction_history_search'))
            return redirect(url_for('transaction_history', user_id=user_id))
        return render_template('transaction_history_search.html')

    @app.route('/transaction-history/<user_id>')
    def transaction_history(user_id):
        try:
            user = User.query.get_or_404(user_id)
            transaction = Transaction.query.filter_by(user_id=user_id).first()
            
            if not transaction:
                flash('No transaction history found for this user.', 'error')
                return redirect(url_for('transaction_history_search'))
                
            return render_template('transaction_history.html', 
                                user=user,
                                transaction=transaction)
        except Exception as e:
            flash('Error loading transaction history.', 'error')
            return redirect(url_for('transaction_history_search'))

    @app.route('/export-csv')
    def export_csv():
        try:
            output = BytesIO()
            string_buffer = StringIO()
            writer = csv.writer(string_buffer)
            
            writer.writerow(['User ID', 'Transaction Count', 'Total Amount', 'Points', 'Last Updated'])
            
            transactions = Transaction.query.all()
            for t in transactions:
                writer.writerow([str(t.user_id), t.count, t.amount, t.points, t.last_updated])
            
            output.write(string_buffer.getvalue().encode('utf-8'))
            string_buffer.close()
            output.seek(0)
            
            return send_file(
                output,
                mimetype='text/csv',
                as_attachment=True,
                download_name=f'leaderboard_{datetime.now().strftime("%Y%m%d")}.csv'
            )
        except Exception as e:
            flash('Error exporting data.', 'error')
            return redirect(url_for('leaderboard'))
