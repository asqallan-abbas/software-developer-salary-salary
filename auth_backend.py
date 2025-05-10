import hashlib
import json
import os
import secrets
import time
import re
from datetime import datetime, timedelta

# File to store user credentials and metadata
USER_DB_FILE = "user_credentials.json"
# Maximum failed login attempts before temporary lockout
MAX_LOGIN_ATTEMPTS = 5
# Lockout duration in minutes
LOCKOUT_DURATION = 4
# Password requirements
PASSWORD_MIN_LENGTH = 8
PASSWORD_REQUIRES_SPECIAL = True
PASSWORD_REQUIRES_NUMBER = True
PASSWORD_REQUIRES_UPPERCASE = True

class AuthBackend:
    def __init__(self):
        """Initialize the authentication backend"""
        self.users = self.load_users()
    
    def load_users(self):
        """Load user credentials and metadata from file"""
        if os.path.exists(USER_DB_FILE):
            with open(USER_DB_FILE, "r") as f:
                return json.load(f)
        else:
            # Create default admin user if file doesn't exist
            default_users = {
                "admin": {
                    "password_hash": self._hash_password("admin123"),
                    "created_at": datetime.now().isoformat(),
                    "last_login": None,
                    "failed_attempts": 0,
                    "locked_until": None,
                    "role": "admin",
                    "email": "admin@example.com"
                }
            }
            self.save_users(default_users)
            return default_users
    
    def save_users(self, users=None):
        """Save user credentials and metadata to file"""
        if users is None:
            users = self.users
        with open(USER_DB_FILE, "w") as f:
            json.dump(users, f, indent=2)
    
    def _hash_password(self, password, salt=None):
        """Create a hashed version of the password with optional salt"""
        if salt is None:
            salt = secrets.token_hex(16)
        
        # Combine password and salt
        salted_password = password + salt
        # Hash the salted password
        hash_obj = hashlib.sha256(salted_password.encode())
        password_hash = hash_obj.hexdigest()
        
        # Return the hash and salt
        return f"{password_hash}:{salt}"
    
    def _verify_password(self, stored_hash, password):
        """Verify if the provided password matches the stored hash"""
        # Split the stored hash into hash and salt
        if ":" not in stored_hash:
            # Handle legacy passwords without salt
            return hashlib.sha256(password.encode()).hexdigest() == stored_hash
        
        hash_part, salt = stored_hash.split(":")
        # Hash the password with the salt
        salted_password = password + salt
        hash_obj = hashlib.sha256(salted_password.encode())
        password_hash = hash_obj.hexdigest()
        
        # Compare the hashes
        return password_hash == hash_part
    
    def is_account_locked(self, username):
        """Check if the account is locked due to too many failed login attempts"""
        if username not in self.users:
            return False
        
        user = self.users[username]
        if "locked_until" in user and user["locked_until"]:
            locked_until = datetime.fromisoformat(user["locked_until"])
            if datetime.now() < locked_until:
                # Account is still locked
                return True
            else:
                # Lock period has expired, reset failed attempts
                user["failed_attempts"] = 0
                user["locked_until"] = None
                self.save_users()
        
        return False
    
    def get_remaining_lockout_time(self, username):
        """Get the remaining lockout time in minutes"""
        if username not in self.users:
            return 0
        
        user = self.users[username]
        if "locked_until" in user and user["locked_until"]:
            locked_until = datetime.fromisoformat(user["locked_until"])
            if datetime.now() < locked_until:
                # Calculate remaining time in minutes
                remaining = (locked_until - datetime.now()).total_seconds() / 60
                return round(remaining)
        
        return 0
    
    def authenticate(self, username, password):
        """Authenticate a user with username and password"""
        # Check if user exists
        if username not in self.users:
            return False, "Invalid username or password"
        
        user = self.users[username]
        
        # Check if account is locked
        if self.is_account_locked(username):
            remaining_minutes = self.get_remaining_lockout_time(username)
            return False, f"Account is locked. Try again in {remaining_minutes} minutes."
        
        # Verify password
        if not self._verify_password(user["password_hash"], password):
            # Increment failed attempts
            user["failed_attempts"] = user.get("failed_attempts", 0) + 1
            
            # Check if account should be locked
            if user["failed_attempts"] >= MAX_LOGIN_ATTEMPTS:
                # Lock the account
                locked_until = datetime.now() + timedelta(minutes=LOCKOUT_DURATION)
                user["locked_until"] = locked_until.isoformat()
                self.save_users()
                return False, f"Too many failed attempts. Account locked for {LOCKOUT_DURATION} minutes."
            
            self.save_users()
            return False, "Invalid username or password"
        
        # Authentication successful
        user["failed_attempts"] = 0
        user["last_login"] = datetime.now().isoformat()
        self.save_users()
        
        return True, "Login successful"
    
    def validate_password_strength(self, password):
        """Validate password strength"""
        errors = []
        
        # Check length
        if len(password) < PASSWORD_MIN_LENGTH:
            errors.append(f"Password must be at least {PASSWORD_MIN_LENGTH} characters long")
        
        # Check for uppercase letter
        if PASSWORD_REQUIRES_UPPERCASE and not any(c.isupper() for c in password):
            errors.append("Password must contain at least one uppercase letter")
        
        # Check for number
        if PASSWORD_REQUIRES_NUMBER and not any(c.isdigit() for c in password):
            errors.append("Password must contain at least one number")
        
        # Check for special character
        if PASSWORD_REQUIRES_SPECIAL and not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            errors.append("Password must contain at least one special character")
        
        return errors
    
    def create_account(self, username, password, email=None, role="user"):
        """Create a new user account"""
        # Check if username already exists
        if username in self.users:
            return False, "Username already exists"
        
        # Validate username
        if not re.match(r'^[a-zA-Z0-9_]{3,20}$', username):
            return False, "Username must be 3-20 characters and contain only letters, numbers, and underscores"
        
        # Validate password strength
        password_errors = self.validate_password_strength(password)
        if password_errors:
            return False, password_errors[0]
        
        # Create user
        self.users[username] = {
            "password_hash": self._hash_password(password),
            "created_at": datetime.now().isoformat(),
            "last_login": None,
            "failed_attempts": 0,
            "locked_until": None,
            "role": role,
            "email": email
        }
        
        self.save_users()
        return True, "Account created successfully"
    
    def change_password(self, username, current_password, new_password):
        """Change a user's password"""
        # Authenticate first
        auth_success, _ = self.authenticate(username, current_password)
        if not auth_success:
            return False, "Current password is incorrect"
        
        # Validate password strength
        password_errors = self.validate_password_strength(new_password)
        if password_errors:
            return False, password_errors[0]
        
        # Update password
        self.users[username]["password_hash"] = self._hash_password(new_password)
        self.save_users()
        
        return True, "Password changed successfully"
    
    def get_user_info(self, username):
        """Get user information"""
        if username not in self.users:
            return None
        
        user = self.users[username]
        # Return a copy without the password hash
        user_info = user.copy()
        user_info.pop("password_hash", None)
        
        return user_info
    
    def update_user_info(self, username, email=None, role=None):
        """Update user information"""
        if username not in self.users:
            return False, "User not found"

        if email is not None:
            self.users[username]["email"] = email

        if role is not None:
            self.users[username]["role"] = role

        self.save_users()
        return True, "User information updated successfully"

    def reset_password(self, username, new_password):
        """Reset a user's password (admin function)"""
        if username not in self.users:
            return False, "User not found"

        # Validate password strength
        password_errors = self.validate_password_strength(new_password)
        if password_errors:
            return False, password_errors[0]

        # Update password
        self.users[username]["password_hash"] = self._hash_password(new_password)
        # Reset failed attempts and lock
        self.users[username]["failed_attempts"] = 0
        self.users[username]["locked_until"] = None

        self.save_users()
        return True, f"Password for {username} has been reset"

    def delete_user(self, username):
        """Delete a user account (admin function)"""
        if username not in self.users:
            return False, "User not found"

        # Don't allow deleting the last admin
        if self.users[username].get("role") == "admin":
            # Count admins
            admin_count = sum(1 for user in self.users.values()
                             if isinstance(user, dict) and user.get("role") == "admin")
            if admin_count <= 1:
                return False, "Cannot delete the last admin account"

        # Delete the user
        del self.users[username]
        self.save_users()
        return True, f"User {username} has been deleted"