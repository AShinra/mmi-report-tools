import streamlit as st
import pandas as pd
from pymongo import MongoClient
import re
import random
import string
from argon2 import PasswordHasher


@st.cache_resource
def get_client():
    client = MongoClient(st.secrets["mongodb"]["uri"])
    return client

@st.cache_resource
def connect_mongodb():
    client = get_client()
    return client['analysts']

@st.cache_resource
def get_collection(collection_name):
    db = connect_mongodb()
    return db[collection_name]

@st.cache_data
def read_excel_file(excel_file):
    return pd.read_excel(excel_file)

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def generate_password(length=12):
    if length < 6:
        raise ValueError("Password length should be at least 6 characters")

    # Define character pools
    letters = string.ascii_letters      # a-zA-Z
    digits = string.digits              # 0-9
    symbols = string.punctuation        # Special characters like !@#$%

    # Ensure password has at least one of each type
    password = [
        random.choice(letters),
        random.choice(digits),
        random.choice(symbols)
    ]

    # Fill the rest of the password length with random choices from all pools
    all_chars = letters + digits + symbols
    password += random.choices(all_chars, k=length - 3)

    # Shuffle the password list and join into a string
    random.shuffle(password)
    return ''.join(password)


def passhash(my_secure_password):
    ph = PasswordHasher()

    # Hash a password
    hash = ph.hash(my_secure_password)
    
    # Verify a password
    # try:
    #     ph.verify(hash, "my_secure_password")
    #     print("Password is correct")
    # except:
    #     print("Password is incorrect")
    return hash

def ui_settings():
    st.set_page_config(
        # layout="wide",
        page_title="Media Meter Web Tool",
        initial_sidebar_state='expanded')

    st.markdown("""
    <style>
    /* Global page padding */
    .block-container {
        padding-top: 2.5rem;
        padding-bottom: 2.5rem;
        padding-left: 3rem;
        padding-right: 3rem;
    }

    /* Vertical spacing between all elements */
    div[data-testid="stVerticalBlock"] {
        gap: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)