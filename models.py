from app import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    
    def set_password(self, password):
        if not self.validate_password(password):
            raise ValueError("Password must be at least 8 characters long and contain at least one number")
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def update_username(self, new_username):
        if not self.validate_username(new_username):
            raise ValueError("Username must be between 3 and 80 characters long")
        if Admin.query.filter(Admin.username == new_username, Admin.id != self.id).first():
            raise ValueError("Username already exists")
        self.username = new_username
        
    @staticmethod
    def validate_password(password):
        return (len(password) >= 8 and 
                any(c.isdigit() for c in password))
    
    @staticmethod
    def validate_username(username):
        return 3 <= len(username) <= 80
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(255))

    def set_password(self, password):
        if not self.validate_password(password):
            raise ValueError("Password must be at least 8 characters long and contain at least one number")
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def update_username(self, new_username):
        if not self.validate_username(new_username):
            raise ValueError("Username must be between 3 and 80 characters long")
        if Admin.query.filter(Admin.username == new_username, Admin.id != self.id).first():
            raise ValueError("Username already exists")
        self.username = new_username
        
    @staticmethod
    def validate_password(password):
        return (len(password) >= 8 and 
                any(c.isdigit() for c in password))
    
    @staticmethod
    def validate_username(username):
        return 3 <= len(username) <= 80

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vly_user_id = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vly_user_id = db.Column(db.String(64), db.ForeignKey('user.vly_user_id'), nullable=False)
    tx_count = db.Column(db.Integer, default=0)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

# テスト用のin-memoryデータベース設定
# engine = create_engine('sqlite:///:memory:')
# Session = sessionmaker(bind=engine)
# session = Session()

# データベーステーブルの作成
# db.create_all(engine)