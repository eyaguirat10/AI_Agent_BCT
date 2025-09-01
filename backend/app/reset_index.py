from haystack.document_stores import ElasticsearchDocumentStore

# Supprime l'index bct à la main
document_store = ElasticsearchDocumentStore(host="localhost", port=9200)
document_store.delete_index("bct")
print("✅ Index 'bct' supprimé proprement.")
