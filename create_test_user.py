#!/usr/bin/env python3
"""Create a test user for WSG platform"""

from app import app, db
from models import User

def create_test_user():
    with app.app_context():
        # Check if test user already exists
        existing_user = User.query.filter_by(username='testuser').first()
        if existing_user:
            print("Test user already exists")
            return
        
        # Create test user
        test_user = User()
        test_user.username = 'testuser'
        test_user.email = 'test@wsg.com'
        test_user.set_password('123456')
        
        db.session.add(test_user)
        db.session.commit()
        
        print("Test user created successfully!")
        print("Username: testuser")
        print("Email: test@wsg.com")
        print("Password: 123456")

if __name__ == '__main__':
    create_test_user()