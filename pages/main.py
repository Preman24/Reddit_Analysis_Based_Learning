# import libraries
import streamlit as st
from streamlit_option_menu import option_menu
import os
import shutil
import atexit

# import app modules here
from get_data import retrieval_data_page
from visualize_data import visualization_page
from transform_data import transform_data_page
from home import home_page

# multi-page app class
class MultiApp:
    def __init__(self):
        self.apps = []

    # Add a new application
    def add_app(self, title, function):
        self.apps.append({
            "title": title,
            "function": function
        })
    # Run the main app
    def run(self):
        with st.sidebar:
            app = option_menu(
                menu_title="Main Menu",
                options=[app["title"] for app in self.apps],
                menu_icon='house-fill',
                default_index=0
            )
        
        if app == "Application Description":
            home_page()  
        elif app == "Data Retrieval":
            retrieval_data_page()
        elif app == "Data Transformation":
            if os.path.exists('../data/raw_data_posts.json'):
                transform_data_page()
            else:
                st.warning("Please fetch data first.")
        elif app == "Data Visualization":
            if os.path.exists('../cleaned/cleaned_data.json'):
                visualization_page()
            else:
                st.warning("Please transform data first.")
# Cleanup function to remove data folders on exit
def cleanup():
    folders = [
        '../data',
        '../cleaned',
    ]
    for path in folders:
        if os.path.exists(path):
            shutil.rmtree(path)

if __name__ == "__main__":
    
    app = MultiApp()

    # Initialize session state only if not already set
    if 'data' not in st.session_state:
        st.session_state['data'] = None
    if 'cleaned_data' not in st.session_state:
        st.session_state['cleaned_data'] = None
        
    app.add_app("Application Description", home_page)
    app.add_app("Data Retrieval", retrieval_data_page)
    app.add_app("Data Transformation", transform_data_page)
    app.add_app("Data Visualization", visualization_page)
    app.run()
    atexit.register(cleanup)