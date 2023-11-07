import backend_config
import backend_config as config
from elasticsearch import Elasticsearch
from feature_extractor import FeatureExtractor

client = Elasticsearch(
    [backend_config.elastic_url], basic_auth=(config.elastic_usr, config.elastic_pass)
)
fe = FeatureExtractor()


def get_results_search_by_text(query, search_type, show_result):
    if search_type == "match":
        search_body = {
            "query": {
                "bool": {
                    "must": [
                        {"match": {"Tags": query}},
                    ]
                }
            },
            "_source": ["OriginalURL", "ImageID", "Tags"],
        }
    elif search_type == "fuzzy":
        search_body = {
            "query": {"fuzzy": {"Tags": {"value": query}}},
            "_source": ["OriginalURL", "ImageID", "Tags"],
        }
    results = client.search(
        index=backend_config.index_name, body=search_body, size=show_result
    )
    return {"resulttype": results}


def get_results_search_by_url(url, show_result):
    feature = fe.get_from_link(url)

    body = {
        "knn": {
            "field": "FeatureVector",
            "query_vector": feature,
            "k": 10,
            "num_candidates": 50,
        },
        "_source": ["OriginalURL"],
    }
    results = client.search(
        index=backend_config.index_name, body=body, size=show_result
    )
    return {"resulttype": results}


def get_results_search_by_image(img, show_result):
    image_feature = fe.get_from_image(img)
    body = {
        "knn": {
            "field": "FeatureVector",
            "query_vector": image_feature,
            "k": 10,
            "num_candidates": 50,
        },
        "_source": ["OriginalURL"],
    }
    results = client.search(
        index=backend_config.index_name, body=body, size=show_result
    )
    return {"resulttype": results}


def get_results_search_by_image_and_text(img, query, search_type, show_result):
    image_feature = fe.get_from_image(img)
    if search_type == "multi_match":
        body = {
            "query": {"match": {"Tags": {"query": query, "boost": 0.1}}},
            "knn": {
                "field": "FeatureVector",
                "query_vector": image_feature,
                "k": 5,
                "num_candidates": 50,
                "boost": 0.9,
            },
            "_source": ["OriginalURL"],
        }
    else:
        body = {
            "knn": {
                "field": "FeatureVector",
                "query_vector": image_feature,
                "k": 5,
                "num_candidates": 50,
                "boost": 0.9,
            },
            "query": {"fuzzy": {"Tags": {"value": query, "boost": 0.1}}},
            "_source": ["OriginalURL"],
        }

    results = client.search(
        index=backend_config.index_name, body=body, size=show_result
    )
    return {"resulttype": results}
