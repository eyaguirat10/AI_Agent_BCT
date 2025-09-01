from haystack.document_stores import ElasticsearchDocumentStore

store = ElasticsearchDocumentStore(host="localhost", port=9200, index="bct")
print("📦 Nombre de documents indexés :", len(store.get_all_documents()))
