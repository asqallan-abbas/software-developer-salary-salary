import streamlit as st

def fix_dropdowns():
    """
    Apply CSS fixes to make all dropdown menus visible with black text on white background.
    This function should be called at the beginning of your Streamlit app.
    """
    st.markdown("""
    <style>
    /* Global fix for all dropdown menus */
    div[data-baseweb="popover"],
    div[data-baseweb="menu"],
    div[role="listbox"],
    ul[role="listbox"],
    li[role="option"] {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    
    /* Target all dropdown menu items */
    div[data-baseweb="popover"] div,
    div[data-baseweb="popover"] ul,
    div[data-baseweb="popover"] li,
    div[data-baseweb="popover"] span {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    
    /* Ensure dropdown options are visible */
    div[role="listbox"] li,
    [role="option"] {
        background-color: #ffffff !important;
        color: #000000 !important;
        font-weight: 500 !important;
        font-size: 16px !important;
    }
    
    /* Fix for hover state */
    div[role="listbox"] li:hover,
    [role="option"]:hover {
        background-color: #3b82f6 !important;
        color: #ffffff !important;
    }
    
    /* Fix for selected state */
    div[aria-selected="true"] {
        background-color: rgba(59, 130, 246, 0.2) !important;
    }
    </style>
    """, unsafe_allow_html=True)