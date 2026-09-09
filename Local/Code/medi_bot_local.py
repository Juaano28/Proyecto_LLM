# medi_bot_local.py – RAGs con 6 especialistas + recreación segura Chroma
import streamlit as st
import pandas as pd
import os
import time
import shutil
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_core.documents import Document
from langchain.prompts import PromptTemplate

# ========== CONFIG ==========
st.set_page_config(page_title="MediBot Pro", page_icon="🩺", layout="wide")
st.title("MediBot Pro – 6 Especialistas RAG")
st.markdown("### Modo Dual: Local (Ollama) ↔ Online (Gemini 2.5 Pro)")

# ========== MODO ==========
modo = st.sidebar.radio(
    "Seleccionar modo",
    ["Local (Ollama – 100% offline)", "Online (Gemini – más rápido)"],
    index=0
)

force_recreate = st.sidebar.checkbox("Forzar recreación ChromaDB", value=False)

api_key = None
if "Online" in modo:
    api_key = st.sidebar.text_input("Google API Key", type="password")
    if not api_key:
        st.warning("Se requiere API Key para modo Online")
        st.stop()
    st.sidebar.success("Gemini activado 🔥")
else:
    st.sidebar.success("Modo Local activado 🦙")

# ========== Modelos ==========
@st.cache_resource
def cargar_modelos():
    if "Online" in modo:
        from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
        llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", google_api_key=api_key)
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-004", google_api_key=api_key)
    else:
        from langchain_ollama import ChatOllama, OllamaEmbeddings
        llm = ChatOllama(model="llama3.1:8b", temperature=0.3)
        embeddings = OllamaEmbeddings(model="mxbai-embed-large")
    return llm, embeddings

llm, embeddings = cargar_modelos()

# ========== Dataset ==========
ruta = r"C:\Users\jelop\OneDrive\Documentos\U\2025-2\Pyoyecto_PLN_Local\DataSet\dataset_clasificado_PC\dataset_clasificado_PC.csv"
df = pd.read_csv(ruta, on_bad_lines="skip", engine="python")

CATEGORIAS = [
    "Symptom/Diagnosis", "Treatment/Medication",
    "Prevention/Health Advice", "Test/Interpretation",
    "Emergency/Critical", "Post-surgery/Recovery"
]

# ========== Funciones soporte ==========
def cerrar_chroma(db):
    try: db._client.reset()
    except: pass

def borrar_directorio(p):
    if not os.path.exists(p): return
    cerrar_chroma(Chroma(persist_directory=p, embedding_function=embeddings))
    for _ in range(3):
        try:
            shutil.rmtree(p)
            return
        except PermissionError:
            time.sleep(1)
    st.error(f"No se pudo borrar: {p}")

# ========== Crear/cargar RAGs ==========
BATCH_SIZE = 4000

@st.cache_resource(show_spinner="Construyendo especialistas...")
def crear_rags_especializados(_df, _modo, force_recreate=False):
    base = "./chroma_db_gemini" if "Online" in _modo else "./chroma_db_llama"
    os.makedirs(base, exist_ok=True)

    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    rags = {}

    for cat in CATEGORIAS:
        subdf = _df[_df["Categoria"] == cat]
        cat_dir = os.path.join(base, cat.lower().replace("/", "_").replace(" ", "_"))

        debe_crear = force_recreate or not (os.path.exists(cat_dir) and os.listdir(cat_dir))

        if debe_crear:
            st.write(f"🔄 (Re)generando especialista: {cat}")
            borrar_directorio(cat_dir)

            docs = [
                Document(page_content=f"Q: {r.Pregunta}\nA: {r.Respuesta}", metadata={"cat": cat})
                for _, r in subdf.iterrows()
                if pd.notna(r.Pregunta) and pd.notna(r.Respuesta)
            ]
            chunks = splitter.split_documents(docs)

            total_batches = (len(chunks) // BATCH_SIZE) + 1
            progress = st.progress(0, text=f"Cargando embeddings para {cat}...")

            db = Chroma(persist_directory=cat_dir, embedding_function=embeddings)

            for i in range(total_batches):
                start = i * BATCH_SIZE
                end = min((i + 1) * BATCH_SIZE, len(chunks))
                batch = chunks[start:end]
                if len(batch) > 0:
                    db.add_documents(batch)
                progress.progress((i + 1) / total_batches)

            db.persist()
            progress.empty()

        else:
            st.write(f"📂 Cargando especialista: {cat}")
            db = Chroma(persist_directory=cat_dir, embedding_function=embeddings)

        retriever = db.as_retriever(search_kwargs={"k": 6})

        prompt = PromptTemplate(
            template="""
You are a medical expert. Use ONLY the context below.
If no relevant info, say: "No similar cases found, but here's general advice:"

Context:
{context}

Question: {question}
Answer in English:
""",
            input_variables=["context", "question"]
        )

        qa = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=retriever,
            chain_type_kwargs={"prompt": prompt},
            return_source_documents=True
        )
        rags[cat] = qa
    return rags

rags = crear_rags_especializados(df, modo, force_recreate)

# ===================== TRADUCCIÓN =====================
def traducir(texto, a="en"):
    prompt = f"Translate to {'English' if a=='en' else 'Spanish'} (only text, no quotes):\n\n{texto}"
    try:
        return llm.invoke([{"role": "user", "content": prompt}]).content.strip()
    except:
        return texto

# ===================== CLASIFICADOR =====================
def clasificar_pregunta(pregunta_en):
    prompt = f"""
You are a medical triage assistant.
Classify the following patient question into ONE of the categories below:

{CATEGORIAS}

Question:
{pregunta_en}

Respond ONLY with the category name.
"""
    try:
        resp = llm.invoke([{"role": "user", "content": prompt}]).content.strip()
        for c in CATEGORIAS:
            if c.lower() in resp.lower():
                return c
        return "Unclassified"
    except:
        return "Unclassified"

# ===================== CHAT =====================
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": f"¡Hola! Modo: **{modo.split('(')[1].split(')')[0]}**\nPregunta en español, respondo con casos reales."}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("¿En qué te ayudo hoy?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Traduciendo..."):
            pregunta_en = traducir(prompt, "en")
        with st.spinner("Clasificando..."):
            categoria = clasificar_pregunta(pregunta_en)
            st.info(f"Especialista asignado: **{categoria}**")

        if categoria == "Emergency/Critical":
            respuesta = "¡EMERGENCIA! Llama a los servicios de urgencia de tu país ahora mismo."
            st.error(respuesta)
        else:
            with st.spinner("Buscando casos similares..."):
                result = rags.get(categoria, rags["Symptom/Diagnosis"])({"query": pregunta_en})
                respuesta_en = result["result"]
                respuesta = traducir(respuesta_en, "es")
                st.write(respuesta)

                with st.expander("Fuentes (en inglés)"):
                    for i, doc in enumerate(result["source_documents"][:3], 1):
                        st.caption(f"Fuente {i}: {doc.page_content[:600]}...")

        st.session_state.messages.append({"role": "assistant", "content": respuesta})

st.caption(f"Bases persistidas en: { './chroma_db_llama' if 'Local' in modo else './chroma_db_gemini' }")
