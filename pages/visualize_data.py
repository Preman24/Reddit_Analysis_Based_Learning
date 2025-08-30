# import libraries
import os
from pathlib import Path
import sys
import streamlit as st
import json
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
import pandas as pd
import numpy as np


# Import the agent from the agent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../agent')))
from agent_summarizer import AI_agent_evaluation

BASE_DIR = Path(__file__).resolve().parent.parent
IMAGE_PATH = BASE_DIR / "image" / "data_visual.png"

# Load data
def load_data(data_path):
    with open(data_path, 'r') as f:
        data = json.load(f)
    return data

# Create data frame
def create_dataframe(data):
    df = {
        'Overall': {
            'title_words': [],
            'content_words': [],
            'flair_count': 0,
            'comments_words': [],
            'post_compound': [],
            'comment_compound': [],
            'post_scores': [],
            'dates': []
        }
    }

    for post in data:
        # Add overall data
        df['Overall']['title_words'].append(post['title'])
        df['Overall']['content_words'].append(post['content'])
        df['Overall']['flair_count'] += 1
        df['Overall']['comments_words'].extend(post['comments']) # change to extend
        df['Overall']['post_compound'].append(post['post_compound'])
        df['Overall']['comment_compound'].append(post['overall_comment_compound'])
        df['Overall']['post_scores'].append(post['score'])
        df['Overall']['dates'].append(post['date'])

        # Add data to specific flair category
        post_category = post['flair']
        if post_category not in df:
            df[post_category] = {
                'title_words': [],
                'content_words': [],
                'flair_count': 0,
                'comments_words': [],
                'post_compound': [],
                'comment_compound': [],
                'post_scores': [],
                'dates': []
            }
        df[post_category]['title_words'].append(post['title'])
        df[post_category]['content_words'].append(post['content'])
        df[post_category]['flair_count'] += 1
        df[post_category]['comments_words'].extend(post['comments'])  
        df[post_category]['post_compound'].append(post['post_compound'])
        df[post_category]['comment_compound'].append(post['overall_comment_compound'])
        df[post_category]['post_scores'].append(post['score'])
        df[post_category]['dates'].append(post['date'])

    return df # return the complete dataframe

# world cloud generation
def generate_word_cloud(text, title):
    st.subheader(f"{title} Word Cloud")
    content_wordcloud = WordCloud(width=400, height=400, background_color='white').generate(text)
    content_wordcloud_array = np.array(content_wordcloud)        
    plt.figure(figsize=(4, 4))
    plt.imshow(content_wordcloud_array, interpolation='bilinear')
    plt.axis("off")
    st.pyplot(plt)

# Bar Chart generation
def generate_bar_chart(x, y, title):
    plt.figure(figsize=(10, 5))
    plt.bar(x, y)
    plt.tight_layout()
    plt.xlabel('Words')
    plt.ylabel('Count')
    st.subheader(title)
    st.pyplot(plt)

# Summary Table generation
def table_summary(data, measure_metrics):
    summary = {
        "Metric": measure_metrics,
        "Value": [
            max(data) if data else 0,
            min(data) if data else 0,
            sum(data) / len(data) if data else 0
        ]
    }
    summary_df = pd.DataFrame(summary)
    return summary_df

# Line Graph generation
def generate_line_graph(x,y,x_title,y_title):
    plt.figure(figsize=(10, 5))
    plt.plot(x, y)
    plt.xlabel(x_title)
    plt.ylabel(y_title)
    x_ticks = plt.xticks()[0] 
    plt.xticks(x_ticks[::len(x_ticks)//5], rotation=45)
    plt.grid()
    plt.tight_layout()
    st.pyplot(plt)
  
# Streamlit App  
def visualization_page():
    data_path = '../cleaned/cleaned_data.json'
    data = load_data(data_path)
    df = create_dataframe(data)
    
    # Streamlit App Layout
    flair_options = st.sidebar.selectbox("Select Flair Category", list(df.keys()))
    selected_data = df[flair_options]
    
    col1, col2 = st.columns([1, 5], vertical_alignment="center", gap="medium")

    with col1:
        st.image(str(IMAGE_PATH), width=300)

    with col2:
        st.markdown("<h1 style='margin: 0; display: inline;'>Reddit Visualization and Analysis by {}</h1>".format(flair_options), unsafe_allow_html=True)
    
    
    col3, col4 = st.columns(2)

    with col3:
        # Comments Word Cloud
        comments_text = ' '.join(word for sublist in selected_data['comments_words'] for word in sublist if word)
        if comments_text:
            generate_word_cloud(comments_text, f"{flair_options} Comments")
        else:
            st.warning("No comments available to generate a comments word cloud.")

    with col4:
        # Content Word Cloud
        content_text = ' '.join(word for sublist in selected_data['content_words'] for word in sublist if word)
        if content_text:
            generate_word_cloud(content_text, f"{flair_options} Content")
        else:
            st.warning("No content available to generate a content word cloud.")

    # Comments Bar Chart
    comments = [word for sublist in selected_data['comments_words'] for word in sublist]  
    sorted_comments = sorted(dict(Counter(comments)).items(), key=lambda item: item[1], reverse=True)[:10]
    top_10_words_comments = "No data available"
    if sorted_comments and (comments_x := [word for word in zip(*sorted_comments)][0]) and (comments_y := [word for word in zip(*sorted_comments)][1]):
        generate_bar_chart(comments_x, comments_y, 'Top 10 Words Frequently Appeared in the Comments')
        top_10_words_comments = f"Words: {comments_x}, Count: {comments_y}, derived analysis from word cloud and found these result from barchart visualization"
    else:
        st.warning("No comments available to generate a comments bar chart.")
        
    # Content Bar Chart
    content = [word for sublist in selected_data['content_words'] for word in sublist]   
    sorted_content = sorted(dict(Counter(content)).items(), key=lambda item: item[1], reverse=True)[:10]
    top_10_words_content = "No data available"
    if sorted_content and (content_x := [word for word in zip(*sorted_content)][0]) and (content_y := [word for word in zip(*sorted_content)][1]):
        generate_bar_chart(content_x, content_y, 'Top 10 Words Frequently Appeared in the Content')
        top_10_words_content = f"Words: {content_x}, Count: {content_y}, derived analysis from word cloud and found these result from barchart visualization"
    else:
        st.warning("No content available to generate a content bar chart.")
        
    col5, col6, col7 = st.columns(3)

    with col5:
        # Comments Summary Table
        st.write(f"<h3 style='text-align: left;'>{flair_options} Comment Compound Score Summary</h3>", unsafe_allow_html=True)
        comment_summary = table_summary(selected_data['comment_compound'], ['Highest Comment Content', 'Lowest Comment Content', 'Average Comment Content'])
        st.markdown(comment_summary.style.hide(axis="index").to_html(), unsafe_allow_html=True)


    with col6:
        #  Post Summary Table
        st.write(f"<h3 style='text-align: left;'>{flair_options} Post Compound Score Summary</h3>", unsafe_allow_html=True)
        post_summary = table_summary(selected_data['post_compound'], ['Highest Post Content', 'Lowest Post Content', 'Average Post Content'])
        st.markdown(post_summary.style.hide(axis="index").to_html(), unsafe_allow_html=True)

    with col7:
        # Post Score Summary Table
        st.write(f"<h3 style='text-align: left;'>{flair_options} Post Score Summary</h3>", unsafe_allow_html=True)
        post_score_summary = table_summary(selected_data['post_scores'], ['Highest Post Scores', 'Lowest Post Scores', 'Average Post Scores'])
        st.markdown(post_score_summary.style.hide(axis="index").to_html(), unsafe_allow_html=True)

    # Prepare Insights
    comments_insights = f"Comments Summary: {comment_summary}"
    post_insights = f"Posts Summary: {post_summary}"
    post_score_insights = f"Post Scores Summary: {post_score_summary}"

    # Flair Count Pie Chart
    if flair_options == "Overall":
        flair_categories = []
        flair_counts = []
        for keys, values in df.items():
            if keys != 'Overall':
                flair_categories.append(keys)
                flair_counts.append(values['flair_count'])
        st.subheader("Percentage of Posts by Flair Category")
        plt.figure(figsize=(10, 5))
        plt.pie(labels=flair_categories, x=flair_counts, autopct='%1.1f%%', textprops={'fontsize': 8})
        st.pyplot(plt)
        flair_counts = f"Number of posts by category: {dict(zip(flair_categories, flair_counts))}"
    else:
        flair_counts = f'Number of {flair_options} posts: {selected_data["flair_count"]}, used pie chart for visualization'

    # Daily Post Count
    st.subheader(f'Daily Post Count for {flair_options}')
    date_counts = Counter(selected_data['dates'])
    sorted_dates = sorted(date_counts.keys())
    post_counts = [date_counts[date] for date in sorted_dates]
    date_objects = [date for date in sorted_dates]
    daily_post_counts = f"{dict(zip(date_objects, post_counts))}, used line graph for visualization"
    generate_line_graph(date_objects, post_counts, 'Date', 'Number of Posts')

    # Compile Insights
    insights = f"""
    Data Insights for {flair_options} Category as a guideline for users input answer:
    - Top 10 Words in Comments: {top_10_words_comments}
    - Top 10 Words in Content: {top_10_words_content}
    - Comments Insights: {comments_insights}
    - Posts Insights: {post_insights}
    - Post Scores Insights: {post_score_insights}
    - Daily Post Count: {daily_post_counts}
    - Flair Counts: {flair_counts}
    """
    # Display Insights
    user_input = st.text_area("Enter your analysis request or question about the data insights:", height=250)
    
    if st.button("Check summary"):
            # Run the agent to get the summary
            if user_input:
                summary_response = AI_agent_evaluation(user_input, insights) # Pass insights to the agent
                st.write("AI Feedback Summary:")
                if summary_response:
                    st.success(summary_response.content) # Display the content of the response
                else:
                    st.warning("No summary response received.")
            else:
                st.warning("No user input provided for evaluation.") # Warning message for empty input