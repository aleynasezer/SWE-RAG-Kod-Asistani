# -*- coding: utf-8 -*-
import os
import uuid
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from datasets import load_dataset

# Haystack bileşenleri
from haystack import Pipeline
from haystack.dataclasses import Document
from haystack.components.embedders import (
    SentenceTransformersDocumentEmbedder,
    SentenceTransformersTextEmbedder,
)
from haystack.components.retrievers.in_memory import InMemoryEmbeddingRetriever
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack.components.builders import ChatPromptBuilder
from haystack.components.writers import DocumentWriter
from haystack_integrations.components.generators.google_genai import GoogleGenAIChatGenerator

# ------------------------------------------------------------
# Ortam değişkenleri
# ------------------------------------------------------------
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")
# Modeli .env'den oku; yoksa güvenli varsayılan kullan
MODEL_NAME = os.getenv("GENAI_MODEL", "gemini-2.5-flash")

# ------------------------------------------------------------
# Yardımcı: SWE‑ReBench satırından içerik oluştur
# ------------------------------------------------------------
PRIMARY_FIELDS = ["problem_statement", "hints_text"]        # Soru/açıklama
ANSWER_FIELDS  = ["patch", "test_patch"]                    # Çözüm/kod/diff

def build_content_from_row(row: dict) -> str:
    parts = []
    for k in PRIMARY_FIELDS:
        v = row.get(k)
        if isinstance(v, str) and v.strip():
            parts.append(f"{k.replace('_',' ').title()}:\n{v.strip()}")
    for k in ANSWER_FIELDS:
        v = row.get(k)
        if isinstance(v, str) and v.strip():
            parts.append(f"{k.replace('_',' ').title()}:\n{v.strip()}")
    return "\n\n".join(parts).strip()

# ------------------------------------------------------------
# Veri Yükleme ve Hazırlama
# ------------------------------------------------------------
@st.cache_resource
def load_and_prepare_data():
    st.info("💡 SWE-ReBench veri seti yükleniyor...")
    try:
        ds = load_dataset("nebius/SWE-rebench", split="test", token=HF_TOKEN)
        df = pd.DataFrame(ds)

        if df.empty:
            st.warning("⚠️ Veri seti boş geldi.")
            return []

        documents = []
        for _, row in df.iterrows():
            rowd = row.to_dict()
            content = build_content_from_row(rowd)
            if not content:
                continue

            meta = {
                "instance_id": str(rowd.get("instance_id", "")),
                "repo":        str(rowd.get("repo", "")),
                "created_at":  str(rowd.get("created_at", "")),
                "license":     str(rowd.get("license_name", "")),
            }
            documents.append(
                Document(content=content, meta=meta, id=str(uuid.uuid4()))
            )

        st.success(f"✅ {len(documents)} belge yüklendi.")
        return documents

    except Exception as e:
        st.error(f"Veri yüklenirken hata oluştu: {e}")
        return []

# ------------------------------------------------------------
# Vektör Veritabanı (Embedding + Indexleme)
# ------------------------------------------------------------
@st.cache_resource
def create_vector_db(documents):
    if not documents:
        st.warning("⚠️ Belgeler bulunamadı.")
        return None

    st.info("🧠 Embedding işlemi yapılıyor...")
    try:
        document_store = InMemoryDocumentStore()
        # TR/EN için çok dilli model
        embedder = SentenceTransformersDocumentEmbedder(
            model="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        )

        indexing = Pipeline()
        indexing.add_component("embedder", embedder)
        indexing.add_component("writer", DocumentWriter(document_store=document_store))
        indexing.connect("embedder.documents", "writer.documents")

        indexing.run({"embedder": {"documents": documents}})

        st.success("✅ Vektör veritabanı başarıyla oluşturuldu!")
        return document_store

    except Exception as e:
        st.error(f"Vektör veritabanı oluşturulurken hata oluştu: {e}")
        return None

# ------------------------------------------------------------
# RAG Pipeline Kurulumu
# ------------------------------------------------------------
@st.cache_resource
def build_rag_pipeline(_document_store):
    try:
        text_embedder = SentenceTransformersTextEmbedder(
            model="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        )
        retriever = InMemoryEmbeddingRetriever(
            document_store=_document_store, top_k=8
        )

        template = """
        {% message role="system" %}
        Aşağıdaki "Bağlam" içindeki parçaları ÖNCELİKLE kullanarak kısa, net ve doğru bir yanıt ver.
        Bağlam azsa da soruyu yanıtlamaya çalış; varsayım yaparsan belirt.
        Yanıt dili: Türkçe.
        Sonunda "Kaynaklar:" başlığıyla kullandığın parçalardan kısaca liste ver (varsa).
        {% endmessage %}

        {% message role="user" %}
        Soru: {{ question }}

        Bağlam ({{ documents|length }} parça):
        {% for d in documents %}
        - {{ d.content }}
        {% endfor %}
        {% endmessage %}
        """

        chat_prompt = ChatPromptBuilder(
            template=template,
            required_variables=["question", "documents"]
        )

        # ÖNEMLİ: model adını .env'den aldık; başında "models/" yok
        generator = GoogleGenAIChatGenerator(
            model=MODEL_NAME
        )

        pipe = Pipeline()
        pipe.add_component("text_embedder", text_embedder)
        pipe.add_component("retriever", retriever)
        pipe.add_component("chat_prompt", chat_prompt)
        pipe.add_component("generator", generator)

        # Akış: embedder → retriever → chat_prompt → generator
        pipe.connect("text_embedder.embedding", "retriever.query_embedding")
        pipe.connect("retriever.documents", "chat_prompt.documents")
        pipe.connect("chat_prompt.prompt", "generator.messages")

        st.success("✅ RAG pipeline başarıyla oluşturuldu!")
        return pipe

    except Exception as e:
        st.error(f"RAG pipeline oluşturulamadı: {e}")
        return None

# ------------------------------------------------------------
# Streamlit Arayüzü
# ------------------------------------------------------------
def main():
    st.set_page_config(page_title="💡 SWE-RAG Kod Asistanı", page_icon="🤖")
    st.title("💡 SWE-RAG Kod Asistanı")
    st.caption("SWE-ReBench veri seti üzerinde kod tabanlı RAG soru-cevap sistemi.")
    # UI'da hangi modelin kullanıldığını göster
    has_key = bool(os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY"))
    st.caption(f"Model: {MODEL_NAME}  |  API key set: {'YES' if has_key else 'NO'}")

    documents = load_and_prepare_data()
    document_store = create_vector_db(documents)
    rag_pipeline = build_rag_pipeline(document_store)

    if not rag_pipeline:
        st.stop()

    st.divider()
    st.subheader("🧩 Kodla ilgili sorular sorabilirsiniz:")

    show_sources = st.checkbox("🔍 İlk 3 kaynağı göster (debug)")

    if prompt := st.chat_input("Örn: Python'da two pointers tekniği nedir?"):
        st.chat_message("user").markdown(prompt)

        with st.spinner("Model yanıt oluşturuyor..."):
            try:
                result = rag_pipeline.run({
                    "text_embedder": {"text": prompt},
                    "chat_prompt": {"question": prompt}
                })

                # Yanıt
                replies = result.get("generator", {}).get("replies", [])
                if replies:
                    msg = replies[0]
                    answer = getattr(msg, "text", str(msg))
                else:
                    answer = "Yanıt alınamadı."

                # Kaynakları göster (opsiyonel)
                if show_sources:
                    docs = result.get("retriever", {}).get("documents", [])
                    with st.expander("🔎 Kullanılan/çıkarılan ilk 3 parça"):
                        if not docs:
                            st.write("_Retriever belge döndürmedi._")
                        else:
                            for i, d in enumerate(docs[:3], start=1):
                                st.markdown(f"**Kaynak {i}:**  \nmeta: {d.meta}")
                                st.code((d.content or "")[:1500])

            except Exception as e:
                answer = f"Hata: {e}"

        st.chat_message("assistant").markdown(answer)

# ------------------------------------------------------------
if __name__ == "__main__":
    main()
