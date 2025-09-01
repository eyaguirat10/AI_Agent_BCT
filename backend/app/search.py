from haystack.document_stores import ElasticsearchDocumentStore
from haystack.nodes import EmbeddingRetriever, SentenceTransformersRanker
from langdetect import detect
import requests

def get_search_component():
    document_store = ElasticsearchDocumentStore(
        host="localhost",
        port=9200,
        index="bct",
        embedding_dim=1024
    )

    retriever = EmbeddingRetriever(
        document_store=document_store,
        embedding_model="intfloat/multilingual-e5-large",
        use_gpu=False,
        scale_score=True
    )

    reranker = SentenceTransformersRanker(model_name_or_path="cross-encoder/ms-marco-MiniLM-L-6-v2")

    return document_store, retriever, reranker

def generate_answer_with_ollama(question, top_docs, source_name="Inconnu", source_page="Inconnue"):

    context = "\n\n".join(
    f"[Document : {doc.meta.get('source', 'inconnu')} | Page : {doc.meta.get('page', 'inconnue')}]\n{doc.content}"
    for doc in top_docs
)

    lang = detect(question)

    if lang == "ar":
        prompt = f"""هذا مقتطف من وثائق رسمية للبنك المركزي التونسي:\n\n{context}\n\nأجب عن السؤال التالي بشكل واضح ومنظم: {question}"""
    else:
        prompt = f"""Tu es un assistant juridique intelligent spécialisé dans les lois et régulations de la Banque Centrale de Tunisie (BCT).\n\nVoici un extrait des documents indexés :\n\n{context}\n\nÀ partir des informations ci-dessus seulement, réponds à la question suivante de manière claire, concise et structurée :\n➡️ {question}\n\nTa réponse doit être :\n- Structurée, claire et fiable.\n- Fondée uniquement sur le contenu ci-dessus.\n\nSi aucune information directe ne permet de répondre, indique clairement qu’il faut consulter la BCT ou les textes officiels concernés."""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False
            }
        )
        response.raise_for_status()
        data = response.json()
        return data.get("response", "Réponse non disponible.")
    except Exception as e:
        return f"Erreur lors de la génération de réponse: {str(e)}"