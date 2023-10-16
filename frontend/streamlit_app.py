import streamlit as st
import numpy as np
from PIL import Image
import re
from io import BytesIO

from st_templates import st_button , load_bootstrap , header , footer
import st_functions as sf
import frontend_config
def is_valid_url(url):
    url_pattern = r'https?://\S+'
    return re.match(url_pattern, url) is not None
load_bootstrap()
st_button('github', frontend_config.github, 'Check Our Github Repository', 20)
header()

container = st.container()
my_expander1 = st.expander("Filter", expanded=True)
with my_expander1:
    cols = st.columns(3)
    cols[0].caption('Search options ')
    show_result = cols[1].slider('Show results', 1, 15)
    filter=cols[2].selectbox(
      'Filter',
       ('Image', 'Text', 'Text & Image'))

if  filter == "Text":
    with st.form("my_form"):
        cols = st.columns([3,1]) 
        query = cols[0].text_input('How can we help you?')
        search_type= cols[1].selectbox(
      'search type',
       ('fuzzy', 'match'))
        st.write("")
        submit = st.form_submit_button("Search")
        if submit and query :
            sf.search_by_text(query,search_type,show_result)
if filter == "Image":
    with st.form("my_form_image"):
        url = st.text_input('Search by image URL')
        uploaded_file = st.file_uploader("Upload a file", type=["png", "jpg"])
        submit = st.form_submit_button("Search")
        if submit :
            if is_valid_url(url):
                sf.search_by_url(url)   
            elif uploaded_file: 
                uploaded = uploaded_file.read()
                sf.search_by_upload_image(uploaded)
            else :
                st.warning("Please provide an image")
if filter == "Text & Image" :
    with st.form("my_form_both"):
        cols = st.columns([2,2]) 
        query = cols[0].text_input('Filter by text')
        search_type= cols[1].selectbox(
      'search type',
       ('fuzzy', 'multi_match'))
        with cols[0]:
            st.write("Provide URL or Browse Image")
            url = st.text_input("Search by URL : ")
        uploaded_file = cols[1].file_uploader("Upload a file", type=["png", "jpg"])
        submit = st.form_submit_button("Search")
        if submit :
            if is_valid_url(url) or uploaded_file:
                sf.search_by_image_and_text(uploaded = uploaded_file.read(),query=query,search_type=search_type,show_result=show_result)   
            else :
                st.warning("Please provide an image")

footer()