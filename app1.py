import streamlit as st
import json
from passlib.hash import sha256_crypt
import os

# File paths
NEWS_FILE = 'news.json'
UPLOADS_DIR = 'uploads'

# Create uploads directory if it doesn't exist
os.makedirs(UPLOADS_DIR, exist_ok=True)

# Your designated username and password
ADMIN_USERNAME = 'AryanChanana'
ADMIN_PASSWORD = 'Aryankapackage@7crore'

# Function to load news articles
def load_news():
    try:
        with open(NEWS_FILE, 'r') as f:
            news = json.load(f)
    except FileNotFoundError:
        news = []
    return news

# Function to save news articles
def save_news(news):
    with open(NEWS_FILE, 'w') as f:
        json.dump(news, f, indent=4)

# Function to handle image upload
def handle_image_upload(image_file):
    if image_file is not None:
        image_path = os.path.join(UPLOADS_DIR, image_file.name)
        with open(image_path, 'wb') as f:
            f.write(image_file.getbuffer())
        st.success(f'Image uploaded successfully: {image_file.name}')
        return image_path
    return None

# Function to render the login page
def render_login():
    st.title('Admin Login')
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')

    if st.button('Login'):
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            st.session_state.username = username
            st.session_state.role = 'admin'
            st.success(f'Logged in as: {username}')
        else:
            st.error('Invalid username or password')
def render_news():
    st.title('IIIT News Page')
    news = load_news()

    if not news:
        st.info('No news available.')
    else:
        for article in reversed(news):
            st.subheader(article['title'])
            st.write(f"Author: {article['author']}")
            st.write(article['content'])
            if article.get('image'):
                st.image(article['image'], caption='Uploaded Image', use_column_width=True)
            st.markdown('---')


# Function to render the news upload form
def render_upload_news():
    st.title('Upload News')
    news_title = st.text_input('News Title')
    news_date=st.date_input('News Date')
    news_content = st.text_area('News Content')
    news_image = st.file_uploader('Upload an image', type=['jpg', 'jpeg', 'png'])

    if st.button('Upload News'):
        if news_title and news_content:
            image_path = handle_image_upload(news_image)

            news_article = {
                'title': news_title,
                'date':  news_date,
                'content': news_content,

                'author': st.session_state.username,
                'image': image_path if image_path else None
            }

            news = load_news()
            news.append(news_article)
            save_news(news)
            st.success('News uploaded successfully!')
        else:
            st.warning('Please fill in both the title and content')

# Function to render the news display

# Function to handle logout
def handle_logout():
    st.session_state.username = None
    st.session_state.role = None
    st.success('Logged out successfully.')

def main():
    st.sidebar.title('Navigation')
    menu = ['College News','Login', 'Upload News' , 'Logout']
    choice = st.sidebar.selectbox('Menu', menu)

    if choice == 'Login':
        render_login()
    elif choice == 'Upload News':
        if st.session_state.username == ADMIN_USERNAME:
            render_upload_news()
        else:
            st.warning('Please login as admin to upload news.')
    elif choice == 'College News':
        render_news()
    elif choice == 'Logout':
        handle_logout()

if __name__ == '__main__':
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'role' not in st.session_state:
        st.session_state.role = None
    main()
