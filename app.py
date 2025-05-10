import streamlit as st
import base64
from pathlib import Path

# Set page configuration must be the first Streamlit command
st.set_page_config(
    page_title="Salary Prediction App",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import and apply the dropdown fix to ensure all dropdown options are visible
from fix_dropdowns import fix_dropdowns
fix_dropdowns()

from predict_page import show_predict_page
from explore_page import show_explore_page
from login_page import show_login_page

# Function to get base64 encoded image
def get_base64_of_bin_file(bin_file):
    """
    Function to load and encode a binary file to base64
    """
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Function to set background image and add logo
def add_bg_and_logo():
    """
    Add a background image and logo to the Streamlit app
    """
    # URL of a coding/programming background image
    bg_url = "https://images.unsplash.com/photo-1555066931-4365d14bab8c?q=80&w=2000&auto=format&fit=crop"

    # URL for the logo/icon
    logo_url = "https://cdn-icons-png.flaticon.com/512/2942/2942789.png"

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: linear-gradient(rgba(255, 255, 255, 0.7), rgba(255, 255, 255, 0.7)), url("{bg_url}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
            color: #000000;
        }}

        /* Add semi-transparent overlay to make text more readable */
        .main .block-container, .sidebar .sidebar-content {{
            background-color: rgba(240, 240, 240, 0.98);
            padding: 2rem;
            border-radius: 10px;
            color: #000000;
            border: 2px solid rgba(59, 130, 246, 0.6);
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
        }}

        /* Style for the sidebar */
        .sidebar .sidebar-content {{
            background-color: rgba(240, 240, 240, 0.98);
        }}

        /* Style for headers */
        h1, h2, h3 {{
            color: #000000;
            text-shadow: none;
        }}

        /* Style for text */
        p, li, label, .stMarkdown, div, span, text {{
            color: #000000 !important;
            font-weight: 400;
        }}

        /* Make form labels more visible */
        .stSelectbox label, .stTextInput label, .stSlider label, .stNumberInput label {{
            color: #000000 !important;
            font-weight: bold !important;
            font-size: 16px !important;
        }}

        /* Make form inputs visible */
        .stTextInput input, .stNumberInput input, .stTextArea textarea, .stDateInput input {{
            color: #000000 !important;
            border: 1px solid #3b82f6 !important;
            border-radius: 4px !important;
            font-size: 16px !important;
        }}

        /* Make dropdown text visible */
        .stSelectbox div[data-baseweb="select"] span {{
            color: #000000 !important;
            font-size: 16px !important;
        }}

        .stSelectbox div[data-baseweb="select"] {{
            border: 1px solid #3b82f6 !important;
            border-radius: 4px !important;
        }}

        /* Override for specific elements that need different colors */
        .social-login-button span {{
            color: white !important;
        }}

        /* Ensure buttons have visible text */
        .stButton button span {{
            color: white !important;
        }}

        /* Ensure buttons have visible text */
        .stButton button span {{
            color: white !important;
        }}

        /* Style for dropdown options */
        div[data-baseweb="popover"] div[data-baseweb="menu"] {{
            border: 1px solid #3b82f6 !important;
        }}

        div[data-baseweb="popover"] div[data-baseweb="menu"] li,
        div[data-baseweb="popover"] div[data-baseweb="menu"] li div,
        div[data-baseweb="popover"] div[data-baseweb="menu"] li span {{
            color: #000000 !important;
            font-size: 16px !important;
        }}

        /* Force all dropdown menu items to be visible */
        [role="listbox"] {{
            background-color: #ffffff !important;
        }}

        [role="listbox"] ul {{
            background-color: #ffffff !important;
        }}

        [role="listbox"] li {{
            color: #000000 !important;
            background-color: #ffffff !important;
        }}

        /* Force all dropdown option text to be black */
        [role="option"] {{
            color: #000000 !important;
            background-color: #ffffff !important;
        }}

        /* Style for the login container */
        .login-container {{
            background-color: rgba(240, 240, 240, 0.98);
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
            margin-top: 2rem;
            border: 1px solid rgba(59, 130, 246, 0.2);
            color: #000000;
        }}

        /* Style for the top navigation bar */
        .stButton button {{
            background-color: #3b82f6;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 0.5rem 1rem;
            font-weight: bold;
            transition: all 0.3s ease;
            border: 1px solid rgba(59, 130, 246, 0.2);
        }}

        .stButton button:hover {{
            background-color: #2563eb;
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.4);
            transform: translateY(-2px);
        }}

        /* Fix for top margin in Streamlit */
        .main .block-container {{
            padding-top: 1rem;
        }}

        .stTextInput label, .stNumberInput label, .stTextArea label, .stDateInput label, .stCheckbox label {{
            color: #000000 !important;
            font-weight: 600 !important;
            font-size: 16px !important;
        }}

        /* Style for checkboxes */
        .stCheckbox {{
            padding: 5px !important;
        }}

        /* Style for radio buttons */
        .stRadio label {{
            color: #000000 !important;
            font-weight: 600 !important;
        }}

        /* Style for sliders */
        .stSlider label {{
            color: #000000 !important;
            font-weight: 600 !important;
            font-size: 16px !important;
        }}

        /* Ensure text is visible in all navigation elements */
        .stSelectbox label {{
            color: #000000 !important;
            font-weight: 600 !important;
        }}

        /* Make dropdown text visible */
        .stSelectbox div[data-baseweb="select"] span {{
            color: #000000 !important;
            font-size: 16px !important;
        }}

        .stSelectbox div[data-baseweb="select"] {{
            border: 1px solid #3b82f6 !important;
            border-radius: 4px !important;
        }}

        /* Style for dropdown options */
        div[data-baseweb="popover"] div[data-baseweb="menu"] {{
            border: 1px solid #3b82f6 !important;
        }}

        div[data-baseweb="popover"] div[data-baseweb="menu"] li,
        div[data-baseweb="popover"] div[data-baseweb="menu"] li div,
        div[data-baseweb="popover"] div[data-baseweb="menu"] li span {{
            color: #000000 !important;
            font-size: 16px !important;
        }}

        div[data-baseweb="popover"] div[data-baseweb="menu"] li:hover,
        div[data-baseweb="popover"] div[data-baseweb="menu"] li:hover div,
        div[data-baseweb="popover"] div[data-baseweb="menu"] li:hover span {{
            background-color: #e6f0ff !important;
            color: #000000 !important;
        }}

        /* Fix for dropdown arrows */
        .stSelectbox div[data-baseweb="select"] svg {{
            fill: #000000 !important;
        }}

        /* Make sure dropdown text is black */
        .stSelectbox div[data-baseweb="select"] div {{
            color: #000000 !important;
        }}

        /* Ensure all dropdown options are visible */
        .stSelectbox ul, .stMultiSelect ul {{
            background-color: #ffffff !important;
        }}

        .stSelectbox ul li, .stMultiSelect ul li {{
            color: #000000 !important;
        }}

        /* Force all dropdown menu items to be visible */
        [role="listbox"] {{
            background-color: #ffffff !important;
        }}

        [role="listbox"] ul {{
            background-color: #ffffff !important;
        }}

        [role="listbox"] li {{
            color: #000000 !important;
            background-color: #ffffff !important;
        }}

        /* Force all dropdown option text to be black */
        [role="option"] {{
            color: #000000 !important;
            background-color: #ffffff !important;
        }}

        /* Style for multiselect */
        .stMultiSelect div[data-baseweb="select"] {{
            background-color: #ffffff !important;
            border: 2px solid #3b82f6 !important;
        }}

        .stMultiSelect div[data-baseweb="tag"] {{
            background-color: rgba(59, 130, 246, 0.2) !important;
            color: #000000 !important;
        }}

        /* Logo styling */
        .logo-container {{
            display: flex;
            justify-content: center;
            margin-bottom: 1rem;
        }}

        .logo {{
            width: 120px;
            height: 120px;
            object-fit: contain;
            filter: drop-shadow(0px 4px 6px rgba(0, 0, 0, 0.1));
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    # Add logo at the top of the page
    st.markdown(
        f"""
        <div class="logo-container">
            <img class="logo" src="{logo_url}" alt="Salary Prediction App Logo">
        </div>
        """,
        unsafe_allow_html=True
    )

# Apply background image and add logo
add_bg_and_logo()

# Initialize session state for login status if it doesn't exist
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = ""
if 'user_role' not in st.session_state:
    st.session_state['user_role'] = ""

# Show login page first
is_authenticated = show_login_page()

# Only show the main app content if user is authenticated
if is_authenticated:
    st.sidebar.markdown("<h2 style='color: #000000; text-shadow: none;'>Navigation</h2>", unsafe_allow_html=True)

    # Get available pages based on user role
    available_pages = ["Predict", "Explore"]

    # Add admin section if user is an admin
    if st.session_state.get('user_role') == "admin":
        available_pages.append("Admin")

    # Add custom styling for the selectbox label
    st.sidebar.markdown("""
    <style>
    div[data-testid="stVerticalBlock"] div[data-testid="stSelectbox"] label {
        color: #000000 !important;
        font-weight: 600 !important;
        font-size: 18px !important;
        text-shadow: none;
        margin-bottom: 8px !important;
    }

    /* Ensure dropdown text is black */
    div[data-testid="stVerticalBlock"] div[data-testid="stSelectbox"] div[data-baseweb="select"] {
        color: #000000 !important;
    }

    div[data-testid="stVerticalBlock"] div[data-testid="stSelectbox"] div[data-baseweb="select"] span {
        color: #000000 !important;
        font-weight: 600 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Page selection with a more visible label
    st.sidebar.markdown("<div style='margin-bottom: 5px;'></div>", unsafe_allow_html=True)
    page = st.sidebar.selectbox("📊 Select Page", available_pages)

    # Display user info in sidebar with better styling
    st.sidebar.markdown("""
    <div style='background-color: rgba(240, 240, 240, 0.98);
                padding: 15px;
                border-radius: 8px;
                margin-bottom: 15px;
                border: 2px solid #3b82f6;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);'>
    """, unsafe_allow_html=True)
    st.sidebar.markdown(f"""
    <div style='font-size: 18px; font-weight: 700; color: black; text-shadow: none;'>
        👤 <span style='color: #000000;'>{st.session_state['username']}</span>
    </div>
    <div style='font-size: 16px; margin-top: 8px; color: black; text-shadow: none;'>
        🔑 Role: <span style='color: #000000; font-weight: 600;'>{st.session_state.get('user_role', 'User')}</span>
    </div>
    """, unsafe_allow_html=True)
    st.sidebar.markdown("</div>", unsafe_allow_html=True)

    # Add a divider
    st.sidebar.markdown("<hr style='margin: 15px 0px; opacity: 0.3;'>", unsafe_allow_html=True)

    # Show the selected page
    if page == "Predict":
        show_predict_page()
    elif page == "Explore":
        show_explore_page()
    elif page == "Admin" and st.session_state.get('user_role') == "admin":
        # Admin page
        st.title("Admin Dashboard")
        st.write("This is the admin dashboard. Only administrators can access this page.")

        # Create tabs for different admin functions
        user_tab, database_tab = st.tabs(["User Management", "Database Viewer"])

        with user_tab:
            st.subheader("User Management")

            # Simple user list from auth backend
            from auth_backend import AuthBackend
            auth = AuthBackend()

            # Get all users
            users = auth.users

            # Add user button
            with st.expander("Add New User"):
                new_username = st.text_input("Username", key="admin_new_username")
                new_password = st.text_input("Password", type="password", key="admin_new_password")
                new_email = st.text_input("Email (optional)", key="admin_new_email")
                new_role = st.selectbox("Role", ["user", "admin"], key="admin_new_role")

            if st.button("Create User"):
                if not new_username or not new_password:
                    st.error("Username and password are required")
                else:
                    success, message = auth.create_account(new_username, new_password, email=new_email, role=new_role)
                    if success:
                        st.success(f"User '{new_username}' created successfully")
                        st.rerun()
                    else:
                        st.error(message)

            # Display users in a table
            if users:
                user_data = []
                for username, user_info in users.items():
                    # Check if user_info is a dictionary (new format) or string (old format)
                    if isinstance(user_info, dict):
                        user_data.append({
                            "Username": username,
                            "Role": user_info.get("role", "user"),
                            "Email": user_info.get("email", ""),
                            "Last Login": user_info.get("last_login", "Never"),
                            "Failed Attempts": user_info.get("failed_attempts", 0)
                        })
                    else:
                        # Handle old format (just a password hash string)
                        user_data.append({
                            "Username": username,
                            "Role": "user",
                            "Email": "",
                            "Last Login": "Never",
                            "Failed Attempts": 0
                        })

                st.dataframe(user_data)

                # User management section
                st.markdown("""
                <h4 style="color: #000000; background-color: rgba(240, 240, 240, 0.98); padding: 10px; border-radius: 5px;">Manage Users</h4>
                """, unsafe_allow_html=True)

                # Select a user to manage
                selected_user = st.selectbox("Select User", list(users.keys()))

                # Create columns for actions
                col1, col2 = st.columns(2)

                with col1:
                    # Reset password
                    with st.expander("Reset Password"):
                        new_password = st.text_input("New Password", type="password", key="reset_password")
                        confirm_password = st.text_input("Confirm Password", type="password", key="confirm_reset_password")

                        if st.button("Reset Password"):
                            if new_password != confirm_password:
                                st.error("Passwords do not match")
                            elif not new_password:
                                st.error("Password cannot be empty")
                            else:
                                success, message = auth.reset_password(selected_user, new_password)
                                if success:
                                    st.success(message)
                                else:
                                    st.error(message)

                with col2:
                    # Change role
                    with st.expander("Change Role"):
                        current_role = "user"
                        if isinstance(users[selected_user], dict):
                            current_role = users[selected_user].get("role", "user")

                        new_role = st.selectbox("Role", ["user", "admin"], index=0 if current_role == "user" else 1)

                        if st.button("Update Role"):
                            success, message = auth.update_user_info(selected_user, role=new_role)
                            if success:
                                st.success(f"Role for {selected_user} updated to {new_role}")
                                st.rerun()
                            else:
                                st.error(message)

                # Delete user
                st.write("---")
                with st.expander("Delete User"):
                    st.warning(f"Are you sure you want to delete user '{selected_user}'? This action cannot be undone.")
                    confirm_delete = st.text_input("Type the username to confirm deletion:", key="confirm_delete")

                    if st.button("Delete User"):
                        if confirm_delete != selected_user:
                            st.error("Username doesn't match. Deletion cancelled.")
                        else:
                            success, message = auth.delete_user(selected_user)
                            if success:
                                st.success(message)
                                st.rerun()
                            else:
                                st.error(message)

        with database_tab:
            st.markdown("""
            <h3 style="color: #000000; background-color: rgba(240, 240, 240, 0.98); padding: 10px; border-radius: 5px;">Database Viewer</h3>
            <p style="color: #000000; background-color: rgba(240, 240, 240, 0.98); padding: 10px; border-radius: 5px;">This shows the raw content of the user database file.</p>
            """, unsafe_allow_html=True)

            import os
            import json

            # Path to the user database file
            db_file = "user_credentials.json"

            if os.path.exists(db_file):
                try:
                    with open(db_file, "r") as f:
                        db_content = json.load(f)

                    # Option to show/hide password hashes
                    show_passwords = st.checkbox("Show password hashes", value=False)

                    # Create a copy of the database for display
                    display_db = {}
                    for username, user_data in db_content.items():
                        display_db[username] = user_data.copy() if isinstance(user_data, dict) else user_data

                        # Optionally hide password hashes
                        if not show_passwords and isinstance(display_db[username], dict) and "password_hash" in display_db[username]:
                            display_db[username]["password_hash"] = "********"

                    # Display the database as JSON
                    st.json(display_db)

                    # Option to download the database
                    st.download_button(
                        label="Download Database",
                        data=json.dumps(db_content, indent=2),
                        file_name="user_credentials.json",
                        mime="application/json"
                    )

                except Exception as e:
                    st.error(f"Error reading database file: {e}")
            else:
                st.warning(f"Database file '{db_file}' not found.") 