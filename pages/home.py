import streamlit as st
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IMAGE_PATH = BASE_DIR / "image" / "reddit.png"
print(IMAGE_PATH)

def home_page():
    col1, col2 = st.columns([0.3, 5])  # Adjust the first column to be narrower
    
    with col1:
        st.image(str(IMAGE_PATH), width=200)  # Adjust width and height as needed

    with col2:
        st.markdown("<h1 style='margin: 0; display: inline;'>Welcome to the Reddit Learning Application</h1>", unsafe_allow_html=True)
    
    st.write("""
    <div style="text-align: Justify;font-size: 20px;">
    Welcome to the Reddit Data Reporting Learning Application! This platform is designed to help you explore and analyze data from Reddit, one of the largest online communities. 
    Whether you're a data enthusiast, researcher, or just curious about social media trends, this application provides you with the tools to retrieve, transform, and visualize Reddit data effectively.
    Navigate through the different sections using the sidebar menu. Start by retrieving data from your favorite subreddits, then move on to transforming and cleaning that data for better analysis. Finally, visualize the insights you've uncovered with interactive charts and graphs.
    Let's dive in and discover what Reddit has to offer!
    </div>
    """, unsafe_allow_html=True)