

def create_index(client ,index : str)-> None :
   if not client.indices.exists(index=index):
    client.indices.create(index=index)
   return

def add_mapping(client ,index : str)-> None :
    mapping = {    
    "dynamic": False,
    "properties": {
        "ImageID  ": { "type": "keyword" },
        "FeatureVector": {
            "type": "dense_vector",
            "dims": 786,
            "index": True,
            "similarity": "l2_norm",
            },
        "Title": { "type": "text" },
        "Author": { "type": "text","index":False},
        "Tags": { "type": "text" },
        "OriginalURL":{"type":"text","index":False}
  }}
  
    client.indices.put_mapping(index=index,body=mapping)
    return 

def generate_actions(index,data_path) -> dict :
    with open(data_path, mode="r",encoding='utf-8') as f:
       reader = csv.DictReader(f)
       for row in reader :   
          feature_vector_str = row["FeatureVector"]
          feature_vector_list = json.loads(feature_vector_str)   
          doc = {
             '_id': row["ImageID"],
             "_index": index,
             'ImageID': row["ImageID"],
             'OriginalURL' : row["OriginalURL"],
             'Author' : row["Author"],
             'Title' : row["Title"],
             'Tags' : row["Tags"],
             'FeatureVector' : feature_vector_list
          }
          yield doc  

def bulk_data(client,data_path,index) :
    bulk(client= client,actions = generate_actions(index,data_path),
                          chunk_size = 500 , max_retries =2)
      
    client.indices.refresh(index=index)
    client.indices.forcemerge(index=index, max_num_segments=1, request_timeout=1200)

if __name__ == '__main__':
    import json
    import numpy as np
    import tqdm
    import csv
    import argparse
    import config_utils
    from elasticsearch import Elasticsearch
    from elasticsearch.helpers import bulk
    parser = argparse.ArgumentParser()
    parser.add_argument('--index_name', type=str, default=config_utils.index_name,
                      help="specify the decoder model")
    parser.add_argument('--data_path', type=str, default=config_utils.data_path,
                      help="specify the data path to index")
    parser.add_argument('--add_mapping', type=str, default="no",
                      help="add mapping to the elasticsearch index [yes | no]")
    
    args = parser.parse_args()

    es = Elasticsearch("http://localhost:9200",basic_auth=("elastic", "souak"))
    #es.cluster.health(wait_for_status='yellow', request_timeout=10)
    index = args.index_name
    create_index(client = es,index = index)
    if args.add_mapping == "yes":
        add_mapping(client = es,index = index)
    bulk_data(client=es,data_path=args.data_path,index=index)

#python indexation.py --data_path "path" --add_mapping no