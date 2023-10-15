from elasticsearch import Elasticsearch
import backend_config
import requests
from urllib import request
from io import BytesIO
from PIL import Image
import pickle as pkl
import json
from feature_extractor import FeatureExtractor
client = Elasticsearch(["http://localhost:9200"])
fe = FeatureExtractor()

def get_results_search_by_text(query):

        search_body = {
            "query": {
                "bool": {
                    "must": [
                        {"match": {"Tags": query}},
                    ]
                }
            }
        }
        results=client.search(index=backend_config.index_name, body=search_body)
        return{"resulttype":results}

def get_results_search_by_url(url):
    feature = fe.get_from_link(url)

    body = {
        "knn": {
        "field": "FeatureVector",
        "query_vector": feature,
        "k": 10,
        "num_candidates": 100
     }
    }
    results =  client.search(index=backend_config.index_name, body=body)
    return{"resulttype":results}
        
def get_results_search_by_image(img):
    image_feature= fe.get_from_image(img)
    body = {
        "knn": {
        "field": "FeatureVector",
        "query_vector": image_feature,
        "k": 10,
        "num_candidates": 100
     }
    }
    results =  client.search(index=backend_config.index_name, body=body)
    return{"resulttype":results}
def get_results_search_by_image_and_text(img,query):
    image_feature= fe.get_from_image(img)
    body = {

            
                "knn": {
                    "field": "FeatureVector",
                    "query_vector": image_feature,
                    "k": 10,
                    "num_candidates": 100,
                    "filter": {
                        "multi_match": {
                        "query": query,
                        "fields":["Tags","Title"]
                    },
            }
    }}
    results =  client.search(index=backend_config.index_name, body=body)
    return{"resulttype":results}