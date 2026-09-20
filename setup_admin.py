"""
Setup script to initialize admin password
Run this after setting up the database to properly hash the admin password
"""

from werkzeug.security import generate_password_hash
import mysql.connector
from config import Config

def setup_admin_password():
    # Generate password hash
    password = "Admin@123"
    hashed_password = generate_password_hash(password)
    
    print(f"Generated password hash for 'Admin@123':")
    print(hashed_password)
    
    # Update database
    try:
        connection = mysql.connector.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME
        )
        
        cursor = connection.cursor()
        
        # Update admin password
        cursor.execute(
            "UPDATE users SET password = %s WHERE email = %s",
            (hashed_password, 'admin@preplate.com')
        )
        
        connection.commit()
        print("Admin password updated successfully in database!")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"Error updating database: {e}")
        print("Please manually update the password hash in the database.")

if __name__ == "__main__":
    setup_admin_password()
