# import libraries
import os
import sys
import streamlit as st
from pathlib import Path

# import functions from src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from preprocess_data import read_file, transform_data, save_file

BASE_DIR = Path(__file__).resolve().parent.parent
IMAGE_PATH = BASE_DIR / "image" / "data_clean.png"

# Define the data transformation page
def transform_data_page():
    col1, col2 = st.columns([1, 5], vertical_alignment="center", gap="medium")
    
    with col1:
        st.image(str(IMAGE_PATH), width=300)  # Adjust width as needed

    with col2:
        st.markdown("<h1 style='margin: 0; display: inline;'>Data Preprocessing and Transformation</h1>", unsafe_allow_html=True)
    
    
    st.write("""
    <div style="text-align: Justify; font-size: 20px;">
    Data Preprocessing and Transformation is a crucial step in preparing your data for analysis. 
    This process involves cleaning and organizing raw data to ensure accuracy and consistency. Here, you'll handle missing values, remove duplicates, and standardize formats to create a reliable dataset.
    Transform your data by reshaping it, merging different sources, or creating new features that enhance your analysis. 
    This foundational work is essential for effective visualization and modeling, ensuring that your insights are based on high-quality data. 
    With the right preprocessing, you'll be well-equipped to draw meaningful conclusions from your analysis.
    </div>
    """, unsafe_allow_html=True)

    # Load the raw data
    data_file_path = '../data/raw_data_posts.json'
    data = read_file(data_file_path)
    
    # Display the first few records for preview
    st.subheader("Preview of Raw Data")
    st.json(data[0])  # Display first post for preview

    # Button to trigger data transformation    
    if st.button("Clean Data"):
        progress_bar = st.progress(0)
        progress_text = st.empty()
        cleaned_data = transform_data(data, progress_bar, progress_text)
        # Store cleaned data in session state
        st.session_state['cleaned_data'] = cleaned_data

        # Save the cleaned data
        save_file(cleaned_data)
        progress_text.text("Progress: 100%")
        st.success("Data cleaned and saved successfully!")
        st.write("""
        <div style="text-align: Justify;">
        Great! Now Your Data is Ready to be Visualized
        With your data cleaned and transformed, it's time to uncover insights through visualization. 
        Head over to the next section to explore powerful visual tools that will help you make sense of your data and communicate your findings effectively. 
        Let’s dive in!
        """, unsafe_allow_html=True)
        
    # Check if cleaned data exists in session state
    if 'cleaned_data' in st.session_state and st.session_state['cleaned_data'] is not None:
        st.subheader("Preview of Cleaned Data")
        st.json(st.session_state['cleaned_data'][0])  # Display first cleaned post for preview