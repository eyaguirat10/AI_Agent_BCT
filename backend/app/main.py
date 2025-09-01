from fastapi import FastAPI
from pydantic import BaseModel
from app.search import get_search_component, generate_answer_with_ollama
from starlette.middleware.sessions import SessionMiddleware
from auth import router as auth_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = [
    "http://localhost:8081",  # your frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  # ✅ this is critical
    allow_methods=["*"],
    allow_headers=["*"],
)


# Initialise Haystack components
document_store, retriever, reranker = get_search_component()

# Add session middleware

app.add_middleware(SessionMiddleware, secret_key="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")
app.include_router(auth_router)

class Question(BaseModel):
    query: str

@app.post("/ask")
def ask_question(question: Question):
    formatted_query = "query: " + question.query.lower()

    # 🔍 Étape 1 : recherche par embeddings
    query_vec = retriever.embed_queries([formatted_query])[0]
    result = retriever.document_store.query_by_embedding(
        query_vec,
        top_k=10,
        return_embedding=False,
        filters=None,
    )

    # 🔄 Étape 2 : reranking
    reranked = reranker.predict(query=question.query, documents=result)

    if not reranked:
        # Aucun document : on répond proprement
        return {
            "query": question.query,
            "answer": (
                "Je n’ai pas trouvé de contenu pertinent dans les documents indexés "
                "pour répondre précisément à cette question. "
                "Veuillez reformuler ou vérifier que les documents BCT correspondants sont bien indexés."
            ),
            "sources": [],
        }

    # 🧪 Debug console – tu gardes tout ça
    print("🔍 Top documents :")
    for doc in reranked[:5]:
        src = doc.meta.get("source")
        page = doc.meta.get("page")
        date = doc.meta.get("date")
        score = getattr(doc, "score", None)
        print(f"\n📄 Source: {src} | Page: {page} | Date: {date}")
        if score is not None:
            print(f"✅ Score: {score:.3f}")
        preview = (doc.content or "")[:300].replace("\n", " ")
        print(f"🧠 Aperçu: {preview}...\n{'-'*60}")

    # 🧠 Génération de réponse avec Ollama + passage des métadonnées du top1
    top_doc = reranked[0]
    source_name = top_doc.meta.get("source", "Inconnu")
    source_page = top_doc.meta.get("page", "Inconnue")

    answer_text = generate_answer_with_ollama(
        question.query,
        reranked[:5],
        source_name=source_name,
        source_page=source_page,
    )

    # 📎 Sources structurées (dédupliquées) depuis le Reranker
    seen = set()
    sources = []
    for d in reranked[:3]:  # tu peux ajuster à 3, 5, etc.
        doc_name = d.meta.get("source", "Inconnu")
        page = d.meta.get("page", "Inconnue")
        key = (doc_name, page)
        if key not in seen:
            seen.add(key)
            sources.append({"doc": doc_name, "page": page})

    # ✅ Réponse finale formatée pour le frontend
    return {
        "query": question.query,
        "answer": answer_text,   # texte libre du LLM
        "sources": sources,      # liste déterministe des sources
    }
