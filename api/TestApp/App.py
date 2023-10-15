from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from utils.feature_extraction import FeatureExtractor
from fastapi import Request , File, UploadFile
import utils.config as config
from PIL import Image
import numpy as np
from elasticsearch import Elasticsearch


app = FastAPI()
fe = FeatureExtractor(config.pca_path)
client = Elasticsearch("https://c8ff-197-26-210-162.ngrok-free.app:443" )

def check_server(client):
    if client.ping() == False:
        print("Elastic Search Server Is Not Running!")

def get_results_search_by_text(content):
        tags=content['tags']

        search_body = {
            "query": {
                "bool": {
                    "must": [
                        {"match": {"Tags": tags}},
                    ]
                }
            }
        }
        results=client.search(index=config.index_name, body=search_body, size=10)
        return results

def get_results_search_by_url(content):
    url = content["url"]

    feature = fe.get_from_link(url)
    # Now you can use the 'url' variable to perform any desired actions
    # Define your Elasticsearch query
    query = {
                    "knn": {
                        "field": "FeatureVector",
                        "query_vector": feature,
                        "k": 10,
                        "num_candidates": 100,
                        "filter": {
                            "multi_match": {
                            "query": query,
                            "fields":["Tags","Title"]
                        },
                }
        }}
    # Execute the Elasticsearch search
    search = client.search(index=config.index_name, body={"query": query}, size=10)
    return search
@app.get('/')
async def root():
    return {"Welcome to our Project"}

@app.post('/search_by_text')
async def search_by_text(request:Request):
    content = await request.json()  
    # Your Elasticsearch search query
    results=get_results_search_by_text(content)
    
    return{"resulttype":results}

@app.post('/get_feature_from_url/')

async def get_feature_from_url(request: Request):
    content = await request.json()
    
    results=get_results_search_by_url(content)

    return {"feature": results}

if __name__ == "__main__":
    import uvicorn
    check_server(client)

    uvicorn.run(app, host="0.0.0.0", port=8000)
