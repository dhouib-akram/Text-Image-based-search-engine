import requests
import base64
import frontend_config
import streamlit as st

def search_by_text(query):
    cols = st.columns(2)
    col_heights = [0, 0]
    displayed_images = 0
    base_url = frontend_config.base_url
    url = base_url + '/search_by_text/'
    json = {"tags":query}
    response = requests.post(url,json=json)

    if response.status_code == 200:
        data = response.json()
        for hit in data["resulttype"]["hits"]["hits"] :
            image = hit["_source"]['OriginalURL']

            col_id = 0 if col_heights[0] <= col_heights[1] else 1
            with st.spinner("Loading Image"):
                cols[col_id].image(image)
                col_heights[col_id] += 1
            #
def search_by_url(link):
    cols = st.columns(2)
    col_heights = [0, 0]
    displayed_images = 0
    base_url = frontend_config.base_url
    url = base_url + '/search_by_url/'
    json = {"url":link}
    response = requests.post(url,json=json)
    print(response.status_code)
    if response.status_code == 200:
        print("ok")
        data = response.json()
        
        for hit in data["resulttype"]["hits"]["hits"] :
            image = hit["_source"]['OriginalURL']
            col_id = 0 if col_heights[0] <= col_heights[1] else 1
            with st.spinner("Loading Image"):
                cols[col_id].image(image)
                col_heights[col_id] += 1
def search_by_image_and_text(query,uploaded):
    cols = st.columns(2)
    col_heights = [0, 0]
    displayed_images = 0
    base_url = frontend_config.base_url
    url = base_url + '/search_by_image_and_text/'
    image_base64 = base64.b64encode(uploaded).decode('utf-8')
    json = {'img': image_base64, "query":query}
    response = requests.post(url,json=json)
    print(response.status_code)
    if response.status_code == 200:
        print("ok")
        data = response.json()
        
        for hit in data["resulttype"]["hits"]["hits"] :
            image = hit["_source"]['OriginalURL']
            col_id = 0 if col_heights[0] <= col_heights[1] else 1
            with st.spinner("Loading Image"):
                cols[col_id].image(image)

def search_by_upload_image(uploaded):
    cols = st.columns(2)
    col_heights = [0, 0]
    displayed_images = 0
    base_url = frontend_config.base_url
    url = base_url + '/search_by_image/'
    image_base64 = base64.b64encode(uploaded).decode('utf-8')
    json = {'img': image_base64}
    print(json)
    response = requests.post(url,json=json)
    print(response.status_code)
    if response.status_code == 200:
        print("ok")
        data = response.json()
        
        for hit in data["resulttype"]["hits"]["hits"] :
            image = hit["_source"]['OriginalURL']
            col_id = 0 if col_heights[0] <= col_heights[1] else 1
            with st.spinner("Loading Image"):
                cols[col_id].image(image)

