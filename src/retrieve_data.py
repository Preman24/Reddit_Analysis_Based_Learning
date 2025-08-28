# import libraries
import os
from dotenv import load_dotenv
import praw
import json
from datetime import datetime, timezone
import time  

# Load environment variables from .env file
load_dotenv()

# Define directories
data_dir = '../data'
os.makedirs(data_dir, exist_ok=True)

# Function to fetch subreddit data
def fetch_subreddit_data(subreddit_name, num_of_posts, update_progress=None, progress_text=None):
    reddit = praw.Reddit(
        client_id=os.getenv("client_id"),
        client_secret=os.getenv("client_secret"),
        password=os.getenv("password"),
        username=os.getenv("user_name"),
        user_agent=os.getenv("user_agent")
    )
    
    data = [] # List to hold fetched data
    subreddit = reddit.subreddit(subreddit_name) # Access the specified subreddit
    posts = subreddit.new(limit=num_of_posts) # Fetch new posts with a limit

    post_list = list(posts)  # Convert to list to allow multiple passes
    
    # Process each post
    for index, post in enumerate(post_list):
        post_comments = []
        post.comments.replace_more(limit=0)
        
        # Extract comments
        for comment in post.comments.list():
            post_comments.append({
                "score": comment.score,
                "content": comment.body,
                "likes": comment.ups,
                "downvotes": comment.downs
            })
        # Extract post date and time
        post_datetime = datetime.fromtimestamp(post.created_utc, timezone.utc)
        post_date = post_datetime.strftime('%Y-%m-%d')
        post_time = post_datetime.strftime('%H:%M:%S')
        # Append post data to the list
        data.append({
            "title": post.title,
            "score": post.score,
            "url": post.url,
            "content": post.selftext,
            "flair": post.link_flair_text,
            "date": post_date,  
            "time": post_time,
            "comments": post_comments
        })

        # Update progress bar
        if update_progress:
            progress = (index + 1) / len(post_list)
            update_progress.progress(progress)
            if progress_text:
                progress_text.text(f"Data Retrieving Progress: {int(progress * 100)}%")
            time.sleep(0.1)

    return data

# Function to save fetched data to a JSON file
def save_file(data):
    with open(os.path.join(data_dir, "raw_data_posts.json"), "w") as f:
        json.dump(data, f, indent=4)