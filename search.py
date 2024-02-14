import json
from pprint import pprint
import os
import time

from dotenv import load_dotenv
from elasticsearch import Elasticsearch

load_dotenv()


class Search:
    def __init__(self):
        self.es = Elasticsearch('http://localhost:9200')
        client_info = self.es.info()
        print('Connected to Elasticsearch!')
        pprint(client_info.body)

    ## The create_index() method first deletes an index with the name my_documents. 
    ## The ignore_unavailable=True option prevents this call from failing when the index name isn't found. 
    ## The following line in the method creates a brand new index with that same name.
    def create_index(self):
        self.es.indices.delete(index='test_index', ignore_unavailable=True)
        self.es.indices.create(index='test_index')

    ## The method accepts the Elasticsearch client and a document from the caller, and inserts the document into the my_documents index, 
    ## returning the response from the service.
    def insert_document(self, document):
        return self.es.index(index='test_index', body=document)


    ## The method accepts a list of documents. 
    ## Instead of adding each document separately, it assembles a single list called operations, and then passes the list to the bulk() method. 
    ## For each document, two entries are added to the operations list:
    ## A description of what operation to perform, set to index, with the name of the index given as an argument.
    ## The actual data of the document
    def insert_documents(self, documents):
        operations = []
        for document in documents:
            operations.append({'index': {'_index': 'test_index'}})
            operations.append(document)
        return self.es.bulk(operations=operations)


    ## Reindex method combines the create_index() and insert_documents() methods created earlier, 
    ## so that with a single call the old index can be destroyed (if it exists) and a new index built and repopulated.
    def reindex(self):
        self.create_index()
        with open('data.json', 'rt') as f:
            documents = json.loads(f.read())
        return self.insert_documents(documents)

    ## This method invokes the search() method of the Elasticsearch client with the index name. 
    ## The query_args argument captures all the keyword arguments provided to the method, and then passes-them through to the es.search() method.
    def search(self, **query_args):
        return self.es.search(index='test_index', **query_args)

    ## To render individual documents, retrieve_document() uses the get() method of the Elasticsearch client
    def retrieve_document(self, id):
        return self.es.get(index='my_documents', id=id)