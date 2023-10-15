
from elasticsearch import Elasticsearch
es = Elasticsearch(["http://localhost:9200"])
es.indices.delete(index="all-images")
# from IPython.display import Image, display, Markdown, Code, HTML

# def display_hits(res):
#     print(f"Found {res['hits']['total']['value']} hits in {res['took']} ms. Showing top {len(res['hits']['hits'])}.")
#     print("")
#     for hit in res['hits']['hits']:
#         s = hit['_source']
#         print(f"Title   {s.get('Title', None)}")
#         if 'tags' in s:
#           desc = str(s.get('Tags', None))
#           print(f"Desc    {desc[:80] + ('...' if len(desc) > 80 else '')}")
#         if 'price' in s:
#           print(f"Labels   {s['Tags']}")
#         print(f"ID      {s.get('ImageID', None)}")
#         print(f"feature      {s.get('FeatureVector', None)}")
#         print(f"Score   {hit.get('_score', None)}")
#         display(Image(s.get("OriginalURL"), width=128))
#         print("")




# def search_by_image_query(image_id=None, feature_vector=None,size=5):
#     if image_id==None and feature_vector==None:
#         raise ValueError("Please enter an Image ID or a Feature Vector")
    
#     if image_id:
#         BODY = {
#         "size" : 2 ,
#         "query": {
#             "elastiknn_nearest_neighbors": {
#                 "vec": {
#                     "index": "all-images",
#                     "field": "FeatureVector",
#                     "vector": {
#                         "ImageID": image_id
#                     }
#                 },
#                 "field": "FeatureVector",
#                 "model": "lsh",
#                 "similarity": "l2",
#                 "candidates": 1
#             }
#         }
#     }
#     res = es.search(index="all-images", query=BODY, size=2)
#     display_hits(res)
# search_by_image_query(image_id="36e7ea69692324f5")