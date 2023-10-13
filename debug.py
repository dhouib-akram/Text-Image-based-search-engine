from elasticsearch import Elasticsearch

es = Elasticsearch(["http://localhost:9200"])
print(type(es))