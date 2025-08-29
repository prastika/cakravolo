#!/usr/bin/env python3
"""
Database initialization script for Palm Oil Monitor
Creates initial admin user and sample data
"""

from app import app, db
from models import User, Company, CensusOperation, CensusData, PalmTree
from utils import create_sample_data
from werkzeug.security import generate_password_hash
from datetime import datetime

def init_database():
    """Initialize database with tables and default data"""
    print("Initializing Palm Oil Monitor database...")
    
    with app.app_context():
        # Create all tables
        db.create_all()
        print("✓ Database tables created")
        
        # Create default admin user if not exists
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            admin_user = User(
                username='admin',
                email='admin@palmoilmonitor.com',
                role='admin'
            )
            admin_user.set_password('admin123')
            db.session.add(admin_user)
            print("✓ Admin user created (admin/admin123)")
        else:
            print("✓ Admin user already exists")
        
        # Create manager user if not exists
        manager_user = User.query.filter_by(username='manager').first()
        if not manager_user:
            manager_user = User(
                username='manager',
                email='manager@palmoilmonitor.com',
                role='manager'
            )
            manager_user.set_password('manager123')
            db.session.add(manager_user)
            print("✓ Manager user created (manager/manager123)")
        else:
            print("✓ Manager user already exists")
        
        # Create viewer user if not exists
        viewer_user = User.query.filter_by(username='viewer').first()
        if not viewer_user:
            viewer_user = User(
                username='viewer',
                email='viewer@palmoilmonitor.com',
                role='viewer'
            )
            viewer_user.set_password('viewer123')
            db.session.add(viewer_user)
            print("✓ Viewer user created (viewer/viewer123)")
        else:
            print("✓ Viewer user already exists")
        
        # Commit user creation
        db.session.commit()
        
        # Create sample data
        print("Creating sample data...")
        create_sample_data()
        print("✓ Sample data created")
        
        print("\n" + "="*50)
        print("🌴 Palm Oil Monitor Database Initialized!")
        print("="*50)
        print("Access the application at: http://localhost:5000")
        print("\nDefault login credentials:")
        print("Admin:   admin/admin123")
        print("Manager: manager/manager123") 
        print("Viewer:  viewer/viewer123")
        print("="*50)

if __name__ == '__main__':
    init_database()
