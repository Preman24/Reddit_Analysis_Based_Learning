# import libraries
import re
import json
import os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import time
import nltk

# Define directories
clean_dir ='../cleaned'
os.makedirs(clean_dir, exist_ok=True)

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()

# Function to read JSON file
def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# Function to preprocess text
def preprocess_text(text): 
    text = text.lower()  # Convert to lowercase
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)  # Remove URLs
    text = re.sub(r'[^\w\s]','',text) # remove punctuation
    text = re.sub(r'\d+', '', text)  # Remove numbers
    text = re.sub(r'\s+', ' ', text)  # Remove extra whitespace
    text = text.strip()  # Remove leading/trailing whitespace
    tokens = word_tokenize(text)  # Tokenize text
    tokens = [word for word in tokens if word not in stopwords.words('english')]  # Remove stopwords
    tokens = [lemmatizer.lemmatize(word) for word in tokens]  # Lemmatize tokens
    return tokens

# Function to transform data
def transform_data(data, update_progress=None, progress_text=None):
    sentiment_analyzer = SentimentIntensityAnalyzer() # Initialize sentiment analyzer
    transformed_data = [] # List to hold transformed data
    
    # Process each post in the data
    for index, post in enumerate(data):
        cleaned_title = preprocess_text(post['title'])
        score = post['score']
        flair = post['flair'].capitalize() if post['flair'] else 'No Flair'
        cleaned_content = preprocess_text(post['content']) if post['content'] else ''
        cleaned_comments = [preprocess_text(comment['content']) for comment in post['comments']] if post['comments'] else []
        post_date = post['date']
        post_time = post['time']
        
        # Calculate sentiment for the post content
        post_sentiment = sentiment_analyzer.polarity_scores(' '.join(cleaned_content))
        post_compound = post_sentiment['compound']

        # Calculate overall sentiment for user comments
        total_compound = post_compound  # Start with post compound
        comment_count = 1  # Start with the post

        for comment in cleaned_comments:
            comment_sentiment = sentiment_analyzer.polarity_scores(' '.join(comment))
            total_compound += comment_sentiment['compound']
            comment_count += 1

        overall_comment_compound = total_compound / comment_count  # Average compound score
        
        transformed_data.append({
            'title': cleaned_title,
            'score': score,
            'flair': flair,
            'content': cleaned_content,
            'comments': cleaned_comments,
            'date': post_date,
            'time': post_time,
            'post_compound': post_compound,  # Add post compound score
            'overall_comment_compound': overall_comment_compound  # Add overall comment compound score
        })
        # Update progress bar
        if update_progress:
            progress = (index + 1) / len(data)
            update_progress.progress(progress)
            if progress_text:
                progress_text.text(f"Data Transformation Progress: {int(progress * 100)}%")
            time.sleep(0.1)   
            
    return transformed_data

# Function to save cleaned data to a JSON file
def save_file(data):
    with open(os.path.join(clean_dir, 'cleaned_data.json'), 'w') as f:
        json.dump(data, f, indent=4)
