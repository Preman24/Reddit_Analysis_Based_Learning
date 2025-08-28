# Use a base image with Python
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install nltk dependencies
RUN python -m nltk.downloader stopwords punkt wordnet punkt_tab

# Copy the entire project into the container
COPY . .

# Expose the port for Streamlit (default is 8501)
EXPOSE 8501

# Command to run the Streamlit app
CMD ["streamlit", "run", "pages/main.py"]