import unittest
from app import create_app
from database import db
from models import Admin

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
            admin = Admin(username='testadmin')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_admin_login(self):
        response = self.client.post('/admin/login', data={
            'username': 'testadmin',
            'password': 'admin123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful login
