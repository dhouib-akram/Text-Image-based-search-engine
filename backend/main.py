from fastapi import FastAPI, HTTPException
from fastapi import Request , File, UploadFile
import backend_config
from PIL import Image
import numpy as np
from elasticsearch import Elasticsearch
import search_functions
import backend_config as config 
app = FastAPI()
client = Elasticsearch([backend_config.elastic_url])
def check_server(client):
    if client.ping() == False:
        print("Elastic Search Server Is Not Running!")

@app.get('/')
async def root():
    return {"it is working"}

@app.post('/search_by_text')
async def search_by_text(request:Request):
    content = await request.json()  
    text = content["tags"]
    search_type = content["type"]
    show_result = int(content["number"])
    return search_functions.get_results_search_by_text(text,search_type,show_result)
    

@app.post('/search_by_url/')
async def get_feature_from_url(request: Request):
    content = await request.json()
    url = content["url"]
    show_result = int(content["number"])
    return search_functions.get_results_search_by_url(url,show_result)

@app.post('/search_by_image/')
async def get_feature_from_url(request: Request):
    content = await request.json()
    img = content["img"]
    show_result = int(content["number"])
    return search_functions.get_results_search_by_image(img,show_result)

@app.post('/search_by_image_and_text/')
async def get_feature_from_url(request: Request):
    content = await request.json()
    img = content["img"]
    query =content["query"]
    search_type = content["type"]
    show_result = int(content["number"])
    return search_functions.get_results_search_by_image_and_text(img,query,search_type,show_result)
if __name__ == "_main_":
    import uvicorn
    check_server(client)

    uvicorn.run(app, host="0.0.0.0", port=8000)
