from database import db
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(db.Model):
    id = db.Column(db.String(64), primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    transactions = db.relationship('Transaction', backref='user', lazy=True)

class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(64), db.ForeignKey('user.id'), nullable=False)
    count = db.Column(db.Integer, default=0)
    amount = db.Column(db.Float, default=0.0)
    points = db.Column(db.Integer, default=0)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
    last_transaction_date = db.Column(db.DateTime)
    weekly_streak = db.Column(db.Integer, default=0)
    transaction_frequency = db.Column(db.Integer, default=0)

    def calculate_points(self):
        """Calculate points based on various factors including transaction count, amount, and bonuses"""
        try:
            # Base points
            transaction_points = self.count * 10  # 10 points per transaction
            amount_points = int(self.amount / 100)  # 1 point per $100

            # Large transaction bonus (extra 50 points for transactions over $1000)
            large_transaction_bonus = int(self.amount / 1000) * 50

            # Frequency bonus (more points for higher daily transaction frequency)
            frequency_bonus = self.transaction_frequency * 5  # 5 points per daily transaction

            # Weekly streak bonus (25 points per consecutive week)
            streak_bonus = self.weekly_streak * 25

            # Calculate total points
            self.points = (
                transaction_points + 
                amount_points + 
                large_transaction_bonus + 
                frequency_bonus + 
                streak_bonus
            )

            return self.points
        except Exception as e:
            print(f"Error calculating points: {str(e)}")
            return 0

    def update_streak_and_frequency(self):
        """Update weekly streak and transaction frequency"""
        try:
            current_time = datetime.utcnow()
            
            if self.last_transaction_date:
                # Update weekly streak
                days_since_last = (current_time - self.last_transaction_date).days
                if days_since_last <= 7:
                    self.weekly_streak += 1
                else:
                    self.weekly_streak = 0  # Reset streak if more than a week has passed

                # Update transaction frequency
                if days_since_last == 0:
                    self.transaction_frequency += 1
                else:
                    self.transaction_frequency = 1  # Reset if not same day
            
            self.last_transaction_date = current_time
        except Exception as e:
            print(f"Error updating streak and frequency: {str(e)}")
