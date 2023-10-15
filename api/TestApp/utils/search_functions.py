from utils.feature_extraction import FeatureExtractor
import utils.config as config
from elasticsearch import Elasticsearch

fe = FeatureExtractor(config.pca_path)
client = Elasticsearch("https://c8ff-197-26-210-162.ngrok-free.app:443"  )
def get_results_search_by_text(tags,fuzzy):
    if fuzzy:
         search_body = {
    "query": {
            "fuzzy": {
            "tags": {
                "value": tags
                }
            }
                }
            }
    else:   
        search_body = {
        "query": {
                "bool": {
                    "must": [
                        {"match": {"Tags": tags}},
                            ]
                        }
                    }
                }
    return client.search(index=config.index_name, body=search_body, size=10)
def get_results_search_by_url(tags):

    feature = fe.get_from_link(url)

    query = {
        "knn": {
        "field": "FeatureVector",
        "query_vector": feature,
        "k": 10,
        "num_candidates": 100
     }
    }
    return client.search(index=config.index_name, body={"query": query}, size=10)