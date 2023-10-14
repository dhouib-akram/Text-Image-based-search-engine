import streamlit as st
import numpy as np
import PIL
import re
from st_functions import st_button , load_bootstrap , header
import frontend_config
def is_valid_url(url):
    url_pattern = r'https?://\S+'
    return re.match(url_pattern, url) is not None
load_bootstrap()
st_button('github', frontend_config.github, 'Check Our Github Repository', 20)
header()


def search_by_image():
    pass
def search_by_image_and_text():
    pass
container = st.container()
my_expander1 = st.expander("Filter", expanded=True)
with my_expander1:
    cols = st.columns(3)
    cols[0].caption('Text options ')
    show_result = cols[1].slider('Show results', 1, 100)

    filter=cols[2].selectbox(
      'Filter',
       ('Image', 'Text', 'Text & Image'))

# container_form = st.container()

if  filter == "Text":
    with st.form("my_form"):
        query = st.text_input('How can we help you?')
        submit = st.form_submit_button("Search")

if filter == "Image":
    with st.form("my_form_image"):
        url = st.text_input('Search by image URL')
        uploaded_file = st.file_uploader("Upload a file", type=["png", "jpg"])
        submit = st.form_submit_button("Search")
        if submit :
            if is_valid_url(url) or uploaded_file:
                search_by_image()   
            else :
                st.warning("Please provide an image")

if filter =="Text & Image" :
    with st.form("my_form_both"):
        cols = st.columns(2)
        query = st.text_input('Filter by Text : ')
        with cols[0]:
            st.write("Provide URL or Browse Image")
            url = st.text_input("Search by URL : ")
        uploaded_file = cols[1].file_uploader("Upload a file", type=["png", "jpg"])
        submit = st.form_submit_button("Search")
        if submit :
            if is_valid_url(url) or uploaded_file:
                search_by_image_and_text()   
            else :
                st.warning("Please provide an image")