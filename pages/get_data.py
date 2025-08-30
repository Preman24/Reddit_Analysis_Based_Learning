# import libraries
import os
import sys
import streamlit as st
from pathlib import Path

# import functions from src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from retrieve_data import fetch_subreddit_data, save_file

BASE_DIR = Path(__file__).resolve().parent.parent
IMAGE_PATH = BASE_DIR / "image" / "data_collect.png"

# Define the data retrieval page
def retrieval_data_page():
    col1, col2 = st.columns([1, 5], vertical_alignment="center", gap="medium")

    with col1:
        st.image(str(IMAGE_PATH), width=300)

    with col2:
        st.markdown("<h1 style='margin: 0; display: inline;'>Reddit Data Retrieval</h1>", unsafe_allow_html=True)

    st.markdown("""
       <div style="text-align: Justify; font-size: 20px;">       
       The Data Retrieval feature allows you to extract valuable insights from any subreddit of your choice. 
       By entering the name of a subreddit, you can fetch posts and comments, enabling you to analyze community interactions and trends. 
       This tool streamlines the data collection process, providing you with the necessary resources to visualize and summarize findings effectively. 
       Whether you're conducting research, exploring topics, or simply curious about community dynamics, this feature empowers you to harness the collective knowledge of Reddit.
       </div>
    """, unsafe_allow_html=True)
    
    # Input field for subreddit name
    subreddit_input = st.text_input("Enter the subreddit name:")
    num_of_posts = st.number_input("Enter the number of posts to fetch:", min_value=1, value=1000)
    # Button to fetch data
    if st.button("Fetch Data"):
        if subreddit_input:
            try:
                progress_bar = st.progress(0)
                progress_text = st.empty()
                data = fetch_subreddit_data(subreddit_input, num_of_posts, update_progress=progress_bar, progress_text=progress_text) # Pass progress bar and text updater
                
                if len(data) == 0: # No data fetched
                    st.warning(f"No posts found for r/{subreddit_input}.") # Show warning if no data
                else:
                    save_file(data) # Save fetched data
                    st.success(f"Fetched {len(data)} posts from r/{subreddit_input}.") # Show success message
            
                progress_bar.progress(100) # Ensure progress bar is full
                progress_text.text("Data fetching complete!") # Final progress text
            
            except Exception as e:
                st.error(f"Error fetching data: {e}") # Show error message
                progress_bar.progress(0) # Reset progress bar
        else:
            st.warning("Please enter a subreddit name!") # Warn if input is empty