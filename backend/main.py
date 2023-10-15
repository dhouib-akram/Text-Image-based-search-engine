from fastapi import FastAPI, HTTPException
from fastapi import Request , File, UploadFile
import backend_config
from PIL import Image
import numpy as np
from elasticsearch import Elasticsearch
import search_functions
app = FastAPI()
client = Elasticsearch(["http://localhost:9200"])
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
    return search_functions.get_results_search_by_text(text)
    

@app.post('/search_by_url/')
async def get_feature_from_url(request: Request):
    content = await request.json()
    url = content["url"]
    return search_functions.get_results_search_by_url(url)

@app.post('/search_by_image/')
async def get_feature_from_url(request: Request):
    content = await request.json()
    img = content["img"]
    return search_functions.get_results_search_by_image(img)

@app.post('/search_by_image_and_text/')
async def get_feature_from_url(request: Request):
    content = await request.json()
    img = content["img"]
    query =content["query"]
    return search_functions.get_results_search_by_image_and_text(img,query)
if __name__ == "_main_":
    import uvicorn
    check_server(client)

    uvicorn.run(app, host="0.0.0.0", port=8000)