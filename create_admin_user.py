#!/usr/bin/env python3
"""
Script to create an initial admin user for the Multi-Business Chatbot.
Run this script to create the first admin user that can access the admin dashboard.
"""

import asyncio
import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app.services.mongodb_service import MongoDBService
from backend.app.models.user import UserCreate
from backend.app.utils import hash_password

async def create_admin_user():
    """Create an initial admin user"""
    
    # Initialize MongoDB service
    mongo_service = MongoDBService()
    await mongo_service.connect()
    
    # Admin user details
    admin_username = "admin"
    admin_email = "admin@example.com"
    admin_password = "admin123"  # Change this to a secure password
    
    try:
        # Check if admin user already exists
        existing_user = await mongo_service.get_user_by_username(admin_username)
        if existing_user:
            print(f"Admin user '{admin_username}' already exists!")
            return
        
        # Create admin user
        user_data = UserCreate(
            username=admin_username,
            email=admin_email,
            password=admin_password,
            role="admin",
            business_id=""  # Admin users use empty string for business_id
        )
        
        hashed_password = hash_password(admin_password)
        admin_user = await mongo_service.create_user(user_data, hashed_password)
        
        print(f"✅ Admin user created successfully!")
        print(f"Username: {admin_username}")
        print(f"Email: {admin_email}")
        print(f"Password: {admin_password}")
        print(f"Role: admin")
        print(f"User ID: {admin_user.user_id}")
        print("\n🔐 You can now login to the admin dashboard with these credentials.")
        print("⚠️  Please change the password after first login for security.")
        
    except Exception as e:
        print(f"❌ Error creating admin user: {str(e)}")
    
    finally:
        # Close MongoDB connection
        if mongo_service.client:
            mongo_service.client.close()

if __name__ == "__main__":
    print("🚀 Creating initial admin user...")
    asyncio.run(create_admin_user())
