import sqlite3
import streamlit as st
from streamlit_option_menu import option_menu

from streamlit_extras.switch_page_button import switch_page 

import gui
import gallery

st.set_page_config(page_title='Network Image Stitching', layout='wide')

# Custom CSS Style
st.markdown("""
    <style>
        .st-emotion-cache-10oheav.eczjsme4 {
            padding-top: 36px;
        }
        .st-emotion-cache-z5fcl4.ea3mdgi4 {
            padding-top: 40px;
        }
        .element-container:has(iframe[title="streamlit_cookies_manager.cookie_manager.CookieManager.sync_cookies"]) {
            display: none;
        }
        button[title^=Exit]+div [data-testid=stImage]{
            text-align: center;
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 100%;
        }
        # ul.streamlit-expander {
        #     overflow: scroll;
        #     -- width: 1500px;
        # }
    </style>
""", unsafe_allow_html=True)

# Create Gallery Table
gallery.createTable()

# def login():
from streamlit_login_auth_ui.widgets import __login__

__login__obj = __login__(auth_token = "courier_auth_token", 
                    company_name = "Shims",
                    width = 200, height = 250, 
                    logout_button_name = 'Logout', hide_menu_bool = False, 
                    hide_footer_bool = False, 
                    lottie_url = 'https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json')

    # st.session_state.login = __login__obj.build_login_ui()
    # return __login__obj

#Check logged in session by cookies
fetched_cookies = __login__obj.cookies
if '__streamlit_login_signup_ui_username__' in fetched_cookies.keys():
    username = fetched_cookies['__streamlit_login_signup_ui_username__']
    if username == '1c9a923f-fb21-4a91-b3f3-5f18e3f01182':
        username = ' '
else:
    username = ' '


def loginPage():
    LOGGED_IN = __login__obj.build_login_ui()   

    if LOGGED_IN:
        st.subheader(f"Now Login as {username}")

def intro():

    st.write("# Welcome to Networked Image Stitching on WEB! 👋")

    st.markdown(
        """
        ### Presented by Akiraphat Jukgaew

        #
        #
    """
    )  

def imgStitching():
    
    gui.main(username)

def pageLock():
    st.write("# Seems like you've logged in!")

def galleryPage():

    if username is not ' ':
        gallery.main(username)
    else:
        st.subheader('Please login in to see this contents.')

if username is ' ':
    m = "Log In"
else:
    m = "Log Out"
    

page_names_to_funcs = {
    "Home": intro,
    "Image Stitching": imgStitching,
    # "Login": loginPage,
    m: loginPage,
    "My Gallery": galleryPage,
}

# demo_name = st.sidebar.selectbox("Choose a demo", page_names_to_funcs.keys())
# page_names_to_funcs[demo_name]()

selected = option_menu(
    menu_title=None,  # required
    options=["Home", "Image Stitching", "My Gallery", m],  # required
    icons=["house", "pencil-square", "archive", "person-circle"],  # optional
    default_index=0,  # optional
    orientation="horizontal",
)


if __name__ == '__main__':

    if selected in page_names_to_funcs.keys():
        page_names_to_funcs[selected]()