import os
import re
import fitz  # PyMuPDF
import pytesseract
import requests
import magic
from pdf2image import convert_from_path
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from langdetect import detect, DetectorFactory
from nltk.tokenize import sent_tokenize
from PIL import Image, ImageFilter
from sentence_transformers import SentenceTransformer, util
from haystack import Document
from haystack.document_stores import ElasticsearchDocumentStore
from haystack.nodes import EmbeddingRetriever, SentenceTransformersRanker
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
import nltk

nltk.download("punkt")

# === Configs
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
poppler_path = r"C:\Users\Eya_\Downloads\Release-24.08.0-0\poppler-24.08.0\Library\bin"
DetectorFactory.seed = 0
model = SentenceTransformer("intfloat/multilingual-e5-large")

PDF_TEMP_DIR = "temp_pdfs"
os.makedirs(PDF_TEMP_DIR, exist_ok=True)

BCT_PAGES = [

    "https://www.bct.gov.tn/bct/siteprod/page.jsp?id=229",

]

# === PDF Collector
def find_all_pdfs():
    pdf_links = []
    for page_url in BCT_PAGES:
        try:
            res = requests.get(page_url, timeout=10)
            res.raise_for_status()
            soup = BeautifulSoup(res.content, "html.parser")
            for link in soup.find_all("a", href=True):
                href = link["href"]
                if href.lower().endswith(".pdf") and "404" not in href.lower():
                    pdf_links.append(urljoin(page_url, href))
        except Exception as e:
            print(f"❌ Failed to fetch from {page_url}: {e}")
    return list(set(pdf_links))

def download_pdf(url, save_dir=PDF_TEMP_DIR):
    os.makedirs(save_dir, exist_ok=True)
    filename = os.path.basename(url.split("?")[0])
    file_path = os.path.join(save_dir, filename)
    try:
        response = requests.get(url, timeout=60)
        response.raise_for_status()
        if "application/pdf" not in response.headers.get("Content-Type", ""):
            print(f"⚠️ Not a PDF: {url}")
            return None
        if magic.from_buffer(response.content, mime=True) != "application/pdf":
            print(f"⚠️ Invalid PDF content: {url}")
            return None
        if len(response.content) < 10_000:
            print(f"⚠️ File too small: {url}")
            return None
        with open(file_path, "wb") as f:
            f.write(response.content)
        return file_path
    except Exception as e:
        print(f"❌ Error downloading {url}: {e}")
        return None

# === OCR / Language Detection / Chunking
def preprocess_image_for_ocr(image):
    image = image.convert("L").resize((image.width * 2, image.height * 2), Image.LANCZOS)
    image = image.filter(ImageFilter.MedianFilter(size=3)).filter(ImageFilter.SHARPEN)
    return image.point(lambda x: 0 if x < 190 else 255, '1')

def detect_lang_fallback(text):
    if re.search(r'[\u0600-\u06FF]', text): return "ara"
    try: return "fra" if detect(text) == "fr" else "ara"
    except: return "ara"

def clean_text(text, lang="fra"):
    text = re.sub(r"[^\w\s.,;:!?%\u20ac$()\-\u2013\u2014]", " ", text)
    text = re.sub(r"\s{2,}", " ", text)
    if lang == "fra":
        text = re.sub(r"\b[\u0600-\u06FF]+\b", "", text)
        text = re.sub(r"[علقا]{1,2}", "", text)
    return text.strip()

def extract_text_from_pdf(path):
    doc = fitz.open(path)
    documents = []

    for i, page in enumerate(doc, start=1):
        text = page.get_text("text").strip()
        mode = "📟 Lecture directe" if text else "🔎 OCR"

        if not text or len(text) < 100:
            try:
                image = convert_from_path(
                    path,
                    poppler_path=poppler_path,
                    first_page=i,
                    last_page=i,
                    dpi=150
                )[0]
                image = preprocess_image_for_ocr(image)
                text = pytesseract.image_to_string(image, config="--oem 3 --psm 1 -l fra").strip()
                if len(text) < 100:
                    text = pytesseract.image_to_string(image, config="--oem 3 --psm 1 -l ara").strip()
                mode = "🔎 OCR (fallback)"
            except Exception as e:
                print(f"❌ Erreur OCR page {i} du fichier {path}: {e}")
                continue

        lang = detect_lang_fallback(text)
        text = clean_text(text, lang)
        aperçu = text[:300].replace("\n", " ")
        print(f"\n📄 Page {i} — {mode}")
        print(f"🔍 Aperçu : {aperçu}")
        print(f"🌍 Langue détectée : {lang}")
        print("-" * 80)

        if len(text) < 150 or lang not in ["fra", "ara"]:
            continue

        documents.append(Document(
            content=text,
            meta={"source": Path(path).name, "page": str(i), "lang": lang}
        ))

    return documents

def semantic_chunking(text, model=model, chunk_size=500, similarity_threshold=0.7, min_chunk_size=200, max_chunk_size=1000):
    sentences = sent_tokenize(text)
    embeddings = [model.encode(s, convert_to_tensor=True) for s in sentences]
    chunks, visited = [], set()
    for i, emb_i in enumerate(embeddings):
        if i in visited: continue
        similar_sentences, visited = [sentences[i]], visited | {i}
        for j, emb_j in enumerate(embeddings):
            if j not in visited and util.cos_sim(emb_i, emb_j).item() >= similarity_threshold:
                similar_sentences.append(sentences[j])
                visited.add(j)
        chunk_text = " ".join(similar_sentences)
        if len(chunk_text) > max_chunk_size:
            chunks.extend([chunk_text[i:i+chunk_size] for i in range(0, len(chunk_text), chunk_size)])
        elif len(chunk_text) >= min_chunk_size:
            chunks.append(chunk_text.strip())
    return chunks

def process_doc(doc):
    chunks = semantic_chunking(doc.content)
    return [Document(content=chunk, meta=doc.meta) for chunk in chunks]

def semantic_process_all(documents):
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(tqdm(executor.map(process_doc, documents), total=len(documents), desc="Chunking"))
    return [doc for chunk_list in results for doc in chunk_list if len(doc.content.strip()) > 10]

def index_all_online():
    all_docs = []
    for url in find_all_pdfs():
        print(f"📥 Downloading : {url}")
        pdf_path = download_pdf(url)
        if pdf_path:
            try:
                all_docs.extend(extract_text_from_pdf(pdf_path))
            finally:
                os.remove(pdf_path)  # ✅ suppression immédiate

    if not all_docs:
        print("❌ Aucun document n'a été extrait.")
        return

    semantic_docs = semantic_process_all(all_docs)

    store = ElasticsearchDocumentStore(
        host="localhost",
        port=9200,
        index="bct",
        embedding_dim=1024
    )

    retriever = EmbeddingRetriever(
        document_store=store,
        embedding_model="intfloat/multilingual-e5-large",
        model_format="sentence_transformers",  # ✅ important
        use_gpu=True,  # ✅ recommandé pour ce modèle
        scale_score=True
    )

    reranker = SentenceTransformersRanker(model_name_or_path="cross-encoder/ms-marco-MiniLM-L-6-v2")

    print("🧹 Suppression des anciens documents...")
    store.delete_documents()

    print("💾 Écriture des nouveaux documents...")
    store.write_documents(semantic_docs)

    print("🧠 Génération des embeddings...")
    store.update_embeddings(retriever)

    print(f"\n✅ {len(semantic_docs)} documents indexés avec succès.")



if __name__ == "__main__":
    index_all_online()
