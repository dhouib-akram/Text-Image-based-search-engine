from fastapi import FastAPI

from fastapi import Request 
from elasticsearch import Elasticsearch
import utils.search_functions as sf

app = FastAPI()
client = Elasticsearch("https://c8ff-197-26-210-162.ngrok-free.app:443" )

def check_server(client):
    if client.ping() == False:
        print("Elastic Search Server Is Not Running!")

@app.get('/')
async def root():
    return {"Welcome to our Project"}

@app.post('/search_by_text')
async def search_by_text(request:Request):
    content = await request.json()  
    tags=content['tags']

    return sf.get_results_search_by_text(tags)

@app.post('/search_by_url/')

async def search_by_url(request: Request):
    content = await request.json()
    
    url = content["url"]

    return sf.get_results_search_by_url(url)
@app.post('/search_by_img/')

async def search_by_img(request: Request):
    content = await request.json()
    
    url = content["url"]

    return sf.get_results_search_by_url(url)

if __name__ == "__main__":
    import uvicorn
    check_server(client)

    uvicorn.run(app, host="0.0.0.0", port=8000)
