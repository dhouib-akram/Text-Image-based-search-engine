

def create_index(client ,index : str)-> None :
   if not client.indicclient.exists(index=index):
    client.indices.create(index=index)
   return

def add_mapping(client ,index : str)-> None :
    mapping = {    
    "dynamic": False,
    "properties": {
        "ImageID  ": { "type": "keyword" },
        "featureVec": {
            "type": "elastiknn_dense_float_vector",
            "elastiknn": {
                "dims": 785,
                "model": "lsh",
                "similarity": "l2",
                "L": 60,
                "k": 3,
                "w": 2
            }
        },
        "Title": { "type": "text" },
        "Author": { "type": "text","index":False},
        "Tags": { "type": "text" },
        "OriginalURL":{"type":"text","index":False}
  }
}   
    client.indices.put_mapping(index=index,body=mapping)
    return 

def generate_actions(data_path):
    with open(data_path, mode="r") as f:
       reader = csv.DictReader(f)
       for row in reader :          
          doc = {
             '_id': row["ImageID"],
             'ImageID': row["ImageID"],
             'OriginalURL' : row["ImageID"],
             'Author' : row["Author"],
             'Title' : row["Title"],
             'Tags' : row["Tags"],
             #featureVec : row of list 
          }
          yield doc  

    


if __name__ == '__main__':
    import json
    import csv
    import config_utils
    from elasticsearch import Elasticsearch
    es = Elasticsearch(["http://localhost:9200"])
    #es.cluster.health(wait_for_status='yellow', request_timeout=10)
    index = config_utils.index_name
    create_index(client = es,index = index)
    add_mapping(client = es,index = index)

