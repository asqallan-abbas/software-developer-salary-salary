import streamlit as st
import os
import json
from auth_backend import AuthBackend

# Initialize the authentication backend
auth = AuthBackend()

# Check if old user credentials file exists and migrate if needed
def migrate_old_users():
    old_file = "user_credentials.json"
    if os.path.exists(old_file):
        try:
            with open(old_file, "r") as f:
                old_users = json.load(f)

            # Check if the format is the old one (username: hash)
            if old_users and isinstance(next(iter(old_users.values())), str):
                # Migrate to new format
                for username, password_hash in old_users.items():
                    if username not in auth.users:
                        auth.users[username] = {
                            "password_hash": password_hash,
                            "created_at": datetime.now().isoformat(),
                            "last_login": None,
                            "failed_attempts": 0,
                            "locked_until": None,
                            "role": "user",
                            "email": None
                        }
                auth.save_users()
                # Rename old file to avoid future migrations
                os.rename(old_file, old_file + ".bak")
        except Exception as e:
            print(f"Error migrating users: {e}")

# Try to migrate old users
try:
    from datetime import datetime
    migrate_old_users()
except Exception as e:
    print(f"Migration error: {e}")

def show_login_page():
    """Display the login page"""
    # The logo is already added in app.py, so we just need the title
    st.markdown("""
    <h1 style='text-align: center; color: #3b82f6; margin-top: 0;
               text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
               font-size: 2.5rem; font-weight: 800;
               background: linear-gradient(45deg, #3b82f6, #60a5fa);
               -webkit-background-clip: text;
               -webkit-text-fill-color: transparent;
               padding: 10px;'>
        Salary Prediction App
    </h1>
    """, unsafe_allow_html=True)

    # Initialize session state for login status if it doesn't exist
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    if 'username' not in st.session_state:
        st.session_state['username'] = ""
    if 'user_role' not in st.session_state:
        st.session_state['user_role'] = ""

    # If already logged in, show user profile and logout option
    if st.session_state['logged_in']:
        # Get user info
        user_info = auth.get_user_info(st.session_state['username'])

        # Create a container for the top navigation bar with logout button
        top_nav = st.container()

        with top_nav:
            # Create columns for the top navigation bar
            welcome_col, logout_col = st.columns([3, 1])

            with welcome_col:
                st.markdown(f"""
                <div style='padding: 10px 0px; margin-top: -60px;'>
                    <h4 style='color: #3b82f6; text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);'>Welcome, {st.session_state['username']}!</h4>
                </div>
                """, unsafe_allow_html=True)

            with logout_col:
                # Add logout button to the top right
                if st.button("Logout", key="logout_button_top", use_container_width=True):
                    st.session_state['logged_in'] = False
                    st.session_state['username'] = ""
                    st.session_state['user_role'] = ""
                    st.rerun()

        # Display welcome message with user info
        st.markdown(f"""
        <div style='text-align: center; padding: 20px; background-color: rgba(15, 23, 42, 0.9);
                    border-radius: 10px; margin: 20px 0; box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
                    border: 2px solid rgba(59, 130, 246, 0.6);'>
            <h2 style='color: #3b82f6; text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);'>Welcome to the Salary Prediction App</h2>
            <p style='color: #ffffff; font-size: 18px; font-weight: 500;'>Explore salary data and get predictions based on your profile</p>
        </div>
        """, unsafe_allow_html=True)

        # Create tabs for user profile and account settings
        profile_tab, settings_tab = st.tabs(["Profile", "Account Settings"])

        with profile_tab:
            if user_info:
                st.subheader("User Profile")
                st.write(f"**Username:** {st.session_state['username']}")

                # Safely display user info
                if isinstance(user_info, dict):
                    st.write(f"**Role:** {user_info.get('role', 'User')}")
                    if user_info.get('email'):
                        st.write(f"**Email:** {user_info.get('email')}")
                    if user_info.get('last_login'):
                        st.write(f"**Last Login:** {user_info.get('last_login')}")
                else:
                    st.write("**Role:** User")
                    st.write("**Note:** Limited profile information available.")

        with settings_tab:
            st.subheader("Change Password")

            current_password = st.text_input("Current Password", type="password", key="current_password")
            new_password = st.text_input("New Password", type="password", key="new_password")
            confirm_new_password = st.text_input("Confirm New Password", type="password", key="confirm_new_password")

            if st.button("Update Password", key="update_password"):
                if not current_password or not new_password or not confirm_new_password:
                    st.error("All fields are required")
                elif new_password != confirm_new_password:
                    st.error("New passwords do not match")
                else:
                    success, message = auth.change_password(
                        st.session_state['username'],
                        current_password,
                        new_password
                    )
                    if success:
                        st.success(message)
                    else:
                        st.error(message)

            st.write("---")

            # Email update section
            st.subheader("Update Email")

            # Safely get email value
            current_email = ""
            if user_info and isinstance(user_info, dict):
                current_email = user_info.get('email', '')

            email = st.text_input("Email", value=current_email, key="email")

            if st.button("Update Email", key="update_email"):
                success, message = auth.update_user_info(st.session_state['username'], email=email)
                if success:
                    st.success(message)
                else:
                    st.error(message)

        return True

    # Create a container with styling for the login form
    login_container = st.container()

    with login_container:
        st.markdown("""
        <div style='background-color: rgba(15, 23, 42, 0.9);
                    padding: 30px;
                    border-radius: 15px;
                    box-shadow: 0 8px 24px rgba(0,0,0,0.4);
                    border: 2px solid rgba(59, 130, 246, 0.6);
                    margin-top: 10px;'>
        </div>
        """, unsafe_allow_html=True)

        # Create tabs for login and signup
        tab1, tab2, tab3 = st.tabs(["Login", "Sign Up", "Help"])

        with tab1:
            st.markdown("<h3 style='text-align: center; color: #000000; text-shadow: none;'>Welcome Back!</h3>", unsafe_allow_html=True)

            # Add a welcome message
            st.markdown("""
            <div style="text-align: center; margin-bottom: 20px; color: #000000;">
                Enter your credentials below to access your personalized salary insights.
            </div>
            """, unsafe_allow_html=True)

            # Create a more visually appealing login form
            with st.container():
                st.markdown("""
                <div style="background-color: rgba(240, 240, 240, 0.98);
                            padding: 20px;
                            border-radius: 10px;
                            border: 2px solid rgba(59, 130, 246, 0.3);
                            margin-bottom: 20px;">
                """, unsafe_allow_html=True)

                # Add icon to username field
                st.markdown('<p style="font-size: 16px; font-weight: 600; margin-bottom: 5px; color: #000000;">👤 Username</p>', unsafe_allow_html=True)
                username = st.text_input("", key="login_username", placeholder="Enter your username")

                # Add icon to password field
                st.markdown('<p style="font-size: 16px; font-weight: 600; margin-bottom: 5px; color: #000000;">🔒 Password</p>', unsafe_allow_html=True)
                password = st.text_input("", type="password", key="login_password", placeholder="Enter your password")

                # Remember me checkbox with better styling
                col1, col2 = st.columns([3, 1])
                with col1:
                    remember_me = st.checkbox("Remember me", key="remember_me")
                with col2:
                    st.markdown("""
                    <div style="text-align: right;">
                        <a href="#" style="color: #3b82f6; text-decoration: none; font-size: 14px;">Forgot?</a>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("</div>", unsafe_allow_html=True)

            # Create a stylish login button
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                login_button = st.button("🚀 Sign In", use_container_width=True)

            # Add social login options
            st.markdown("""
            <div style="text-align: center; margin-top: 20px;">
                <p style="color: #000000; margin-bottom: 10px;">Or sign in with</p>
                <div style="display: flex; justify-content: center; gap: 15px;">
                    <div style="background-color: #1877F2; color: white; padding: 8px 15px; border-radius: 5px; cursor: pointer;">
                        <span>Facebook</span>
                    </div>
                    <div style="background-color: #DB4437; color: white; padding: 8px 15px; border-radius: 5px; cursor: pointer;">
                        <span>Google</span>
                    </div>
                    <div style="background-color: #0A66C2; color: white; padding: 8px 15px; border-radius: 5px; cursor: pointer;">
                        <span>LinkedIn</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if login_button:
                if not username or not password:
                    st.error("⚠️ Please enter both username and password")
                else:
                    # Add a loading spinner for better UX
                    with st.spinner("🔄 Authenticating..."):
                        import time
                        time.sleep(0.5)  # Simulate authentication time

                        success, message = auth.authenticate(username, password)
                        if success:
                            st.session_state['logged_in'] = True
                            st.session_state['username'] = username

                            # Get user role
                            user_info = auth.get_user_info(username)
                            if user_info and 'role' in user_info:
                                st.session_state['user_role'] = user_info['role']

                            # Show success with confetti animation
                            st.balloons()
                            st.success("✅ Login successful!")
                            st.rerun()
                        else:
                            st.error("❌ " + message)

        with tab2:
            st.markdown("<h3 style='text-align: center; color: #000000; text-shadow: none;'>Join Our Community</h3>", unsafe_allow_html=True)

            # Add a welcome message
            st.markdown("""
            <div style="text-align: center; margin-bottom: 20px; color: #000000;">
                Create an account to get personalized salary predictions and insights.
            </div>
            """, unsafe_allow_html=True)

            # Create a more visually appealing signup form
            with st.container():
                st.markdown("""
                <div style="background-color: rgba(240, 240, 240, 0.98);
                            padding: 20px;
                            border-radius: 10px;
                            border: 2px solid rgba(59, 130, 246, 0.3);
                            margin-bottom: 20px;">
                """, unsafe_allow_html=True)

                # Add icon to username field
                st.markdown('<p style="font-size: 16px; font-weight: 600; margin-bottom: 5px; color: #000000;">👤 Choose a Username</p>', unsafe_allow_html=True)
                new_username = st.text_input("", key="signup_username", placeholder="3-20 characters, letters, numbers, and underscores only")

                # Add icon to email field
                st.markdown('<p style="font-size: 16px; font-weight: 600; margin-bottom: 5px; color: #000000;">📧 Email Address (optional)</p>', unsafe_allow_html=True)
                new_email = st.text_input("", key="signup_email", placeholder="your.email@example.com")

                # Add icon to password field
                st.markdown('<p style="font-size: 16px; font-weight: 600; margin-bottom: 5px; color: #000000;">🔒 Create a Password</p>', unsafe_allow_html=True)
                new_password = st.text_input("", type="password", key="signup_password", placeholder="At least 8 characters with uppercase, number, and special character")

                # Add icon to confirm password field
                st.markdown('<p style="font-size: 16px; font-weight: 600; margin-bottom: 5px; color: #000000;">🔐 Confirm Password</p>', unsafe_allow_html=True)
                confirm_password = st.text_input("", type="password", key="confirm_password", placeholder="Re-enter your password")

                st.markdown("</div>", unsafe_allow_html=True)

            # Password strength indicator with visual meter
            if new_password:
                errors = auth.validate_password_strength(new_password)

                # Calculate password strength
                strength = 0
                if len(new_password) >= 8:
                    strength += 1
                if any(c.isupper() for c in new_password):
                    strength += 1
                if any(c.isdigit() for c in new_password):
                    strength += 1
                if any(not c.isalnum() for c in new_password):
                    strength += 1

                # Display strength meter
                st.markdown(f"""
                <div style="margin-bottom: 15px;">
                    <p style="font-size: 16px; font-weight: 600; margin-bottom: 5px; color: #e2e8f0;">Password Strength:</p>
                    <div style="display: flex; height: 8px; width: 100%; background-color: rgba(255, 255, 255, 0.1); border-radius: 4px; overflow: hidden;">
                        <div style="width: {strength * 25}%; height: 100%; background-color: {['#ef4444', '#f59e0b', '#10b981', '#3b82f6'][min(strength, 3)]};">
                        </div>
                    </div>
                    <p style="font-size: 14px; margin-top: 5px; color: {['#ef4444', '#f59e0b', '#10b981', '#3b82f6'][min(strength, 3)]};">
                        {['Weak', 'Fair', 'Good', 'Strong'][min(strength, 3)]}
                    </p>
                </div>
                """, unsafe_allow_html=True)

                if errors:
                    st.markdown("""
                    <div style="background-color: rgba(239, 68, 68, 0.1); padding: 10px; border-radius: 5px; margin-bottom: 15px;">
                        <p style="font-size: 16px; font-weight: 600; margin-bottom: 5px; color: #ef4444;">Please fix the following:</p>
                        <ul style="margin-left: 20px; color: #e2e8f0;">
                    """, unsafe_allow_html=True)

                    for error in errors:
                        st.markdown(f"<li>{error}</li>", unsafe_allow_html=True)

                    st.markdown("</ul></div>", unsafe_allow_html=True)

            # Terms and conditions checkbox
            terms_agreed = st.checkbox("I agree to the Terms of Service and Privacy Policy", key="terms_agreed")

            # Create a stylish signup button
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                signup_button = st.button("✨ Create My Account", use_container_width=True)

            # Add social signup options
            st.markdown("""
            <div style="text-align: center; margin-top: 20px;">
                <p style="color: #000000; margin-bottom: 10px;">Or sign up with</p>
                <div style="display: flex; justify-content: center; gap: 15px;">
                    <div style="background-color: #1877F2; color: white; padding: 8px 15px; border-radius: 5px; cursor: pointer;">
                        <span>Facebook</span>
                    </div>
                    <div style="background-color: #DB4437; color: white; padding: 8px 15px; border-radius: 5px; cursor: pointer;">
                        <span>Google</span>
                    </div>
                    <div style="background-color: #0A66C2; color: white; padding: 8px 15px; border-radius: 5px; cursor: pointer;">
                        <span>LinkedIn</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if signup_button:
                if not new_username or not new_password:
                    st.error("⚠️ Username and password cannot be empty")
                elif not terms_agreed:
                    st.error("⚠️ You must agree to the Terms of Service and Privacy Policy")
                elif new_password != confirm_password:
                    st.error("⚠️ Passwords do not match")
                else:
                    # Add a loading spinner for better UX
                    with st.spinner("🔄 Creating your account..."):
                        import time
                        time.sleep(0.5)  # Simulate account creation time

                        success, message = auth.create_account(new_username, new_password, email=new_email)
                        if success:
                            # Show success with confetti animation
                            st.balloons()
                            st.success("✅ Account created successfully! You can now login.")
                        else:
                            st.error("❌ " + message)

        with tab3:
            st.markdown("<h3 style='text-align: center; color: #000000; text-shadow: none;'>Help & Support</h3>", unsafe_allow_html=True)

            # Create tabs for different help topics
            help_tab1, help_tab2, help_tab3 = st.tabs(["🔐 Account Help", "💰 Salary Insights", "📱 Contact Us"])

            with help_tab1:
                st.markdown("""
                <div style="background-color: rgba(240, 240, 240, 0.98);
                            padding: 20px;
                            border-radius: 10px;
                            border: 2px solid rgba(59, 130, 246, 0.3);
                            margin-bottom: 20px;">
                    <h4 style="color: #000000; margin-top: 0;">Password Requirements</h4>
                    <p>For your security, we require strong passwords that meet the following criteria:</p>
                    <ul style="color: #000000;">
                        <li><strong>Length:</strong> At least 8 characters</li>
                        <li><strong>Complexity:</strong> Include at least one uppercase letter</li>
                        <li><strong>Numbers:</strong> Include at least one digit (0-9)</li>
                        <li><strong>Special Characters:</strong> Include at least one special character (!@#$%^&*)</li>
                    </ul>

                    <h4 style="color: #000000; margin-top: 20px;">Account Lockout</h4>
                    <p>Your account will be temporarily locked after 5 failed login attempts.
                    If your account is locked, you'll need to wait 15 minutes before trying again.</p>

                    <h4 style="color: #000000; margin-top: 20px;">Account Security Tips</h4>
                    <ul style="color: #000000;">
                        <li>Never share your password with anyone</li>
                        <li>Use a unique password for this application</li>
                        <li>Consider using a password manager</li>
                        <li>Log out when using shared computers</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

            with help_tab2:
                st.markdown("""
                <div style="background-color: rgba(240, 240, 240, 0.98);
                            padding: 20px;
                            border-radius: 10px;
                            border: 2px solid rgba(59, 130, 246, 0.3);
                            margin-bottom: 20px;">
                    <h4 style="color: #000000; margin-top: 0;">About Our Salary Predictions</h4>
                    <p>Our salary predictions are based on data from the Stack Overflow Developer Survey 2020, which includes responses from over 65,000 developers worldwide.</p>

                    <h4 style="color: #000000; margin-top: 20px;">How We Calculate Salaries</h4>
                    <p>Our machine learning model takes into account several factors:</p>
                    <ul style="color: #000000;">
                        <li><strong>Location:</strong> Country of employment</li>
                        <li><strong>Education:</strong> Highest degree obtained</li>
                        <li><strong>Experience:</strong> Years of professional coding experience</li>
                        <li><strong>Industry:</strong> Sector of employment</li>
                        <li><strong>Job Title:</strong> Current or desired position</li>
                    </ul>

                    <h4 style="color: #000000; margin-top: 20px;">Interpreting Results</h4>
                    <p>The predicted salary represents an average based on the provided factors. Actual salaries may vary based on:</p>
                    <ul style="color: #000000;">
                        <li>Company size and funding</li>
                        <li>Specific technical skills</li>
                        <li>Local market conditions</li>
                        <li>Negotiation outcomes</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

            with help_tab3:
                st.markdown("""
                <div style="background-color: rgba(240, 240, 240, 0.98);
                            padding: 20px;
                            border-radius: 10px;
                            border: 2px solid rgba(59, 130, 246, 0.3);
                            margin-bottom: 20px;">
                    <h4 style="color: #000000; margin-top: 0;">Get in Touch</h4>
                    <p>We're here to help! Reach out to us through any of these channels:</p>

                    <div style="display: flex; align-items: center; margin: 15px 0;">
                        <div style="background-color: #3b82f6; border-radius: 50%; width: 40px; height: 40px; display: flex; justify-content: center; align-items: center; margin-right: 15px;">
                            <span style="color: white; font-size: 20px;">📧</span>
                        </div>
                        <div>
                            <p style="margin: 0; font-weight: 600;">Email Support</p>
                            <p style="margin: 0; color: #3b82f6;">support@salaryprediction.com</p>
                        </div>
                    </div>

                    <div style="display: flex; align-items: center; margin: 15px 0;">
                        <div style="background-color: #3b82f6; border-radius: 50%; width: 40px; height: 40px; display: flex; justify-content: center; align-items: center; margin-right: 15px;">
                            <span style="color: white; font-size: 20px;">📱</span>
                        </div>
                        <div>
                            <p style="margin: 0; font-weight: 600;">Phone Support</p>
                            <p style="margin: 0; color: #3b82f6;">+1 (555) 123-4567</p>
                        </div>
                    </div>

                    <div style="display: flex; align-items: center; margin: 15px 0;">
                        <div style="background-color: #3b82f6; border-radius: 50%; width: 40px; height: 40px; display: flex; justify-content: center; align-items: center; margin-right: 15px;">
                            <span style="color: white; font-size: 20px;">💬</span>
                        </div>
                        <div>
                            <p style="margin: 0; font-weight: 600;">Live Chat</p>
                            <p style="margin: 0; color: #3b82f6;">Available 24/7 on our website</p>
                        </div>
                    </div>
                </div>

                <div style="background-color: rgba(240, 240, 240, 0.98);
                            padding: 20px;
                            border-radius: 10px;
                            border: 2px solid rgba(59, 130, 246, 0.3);
                            margin-top: 20px;">
                    <h4 style="color: #000000; margin-top: 0;">Quick Contact Form</h4>
                    <p>Send us a message and we'll get back to you as soon as possible.</p>
                </div>
                """, unsafe_allow_html=True)

                # Add a simple contact form
                contact_name = st.text_input("Your Name", placeholder="Enter your name")
                contact_email = st.text_input("Your Email", placeholder="Enter your email address")
                contact_subject = st.selectbox("Subject", ["General Inquiry", "Technical Support", "Account Issues", "Feedback", "Other"])
                contact_message = st.text_area("Message", placeholder="How can we help you?", height=150)

                if st.button("📤 Send Message", use_container_width=True):
                    if not contact_name or not contact_email or not contact_message:
                        st.error("⚠️ Please fill in all required fields")
                    else:
                        st.success("✅ Thank you for your message! We'll respond shortly.")
                        st.balloons()

    return st.session_state['logged_in']