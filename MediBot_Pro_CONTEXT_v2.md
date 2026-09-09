# MediBot Pro — Contexto y evolución completa del proyecto

## 1. Propósito de este documento

Este documento reúne el contexto del proyecto **MediBot / MediBot Pro** a partir de:

- `MediChat.ipynb`
- `StreamLit_ProyectoFinal.ipynb`
- `medi_bot_local.py`
- `test_final.py`
- `requeriments.txt`
- información técnica registrada durante las conversaciones del desarrollo.

No se incorporan tecnologías, métricas, resultados ni características que no estén respaldadas por esos archivos o por el contexto registrado. Cuando una parte corresponde a una etapa inicial, una demo o una prueba y no a la versión final, se especifica.

---

# 2. Idea general del proyecto

MediBot es un proyecto de **Procesamiento de Lenguaje Natural (PLN/NLP)** orientado a construir un chatbot médico.

La evolución registrada muestra tres etapas principales:

```text
1. Demo inicial en Google Colab
        ↓
2. Desarrollo de MediBot con RAG y 6 especialistas
        ↓
3. Implementación local con Ollama + Chroma + Streamlit
```

Además, el sistema conserva una arquitectura dual:

```text
                 MediBot
                    │
          ┌─────────┴─────────┐
          │                   │
        Local               Online
          │                   │
       Ollama              Gemini
```

---

# 3. Desarrollo inicial en Google Colab

## 3.1. Primer notebook: `StreamLit_ProyectoFinal.ipynb`

El notebook `StreamLit_ProyectoFinal.ipynb` muestra una etapa inicial en Google Colab orientada a construir una demo web con Streamlit y exponerla hacia Internet mediante Cloudflare Tunnel.

### Instalaciones

La primera celda instala:

```bash
pip install streamlit pandas plotly wordcloud matplotlib transformers torch
```

Después se instala `cloudflared`:

```bash
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -O cloudflared
chmod +x cloudflared
mv cloudflared /usr/local/bin/cloudflared
```

La finalidad era poder ejecutar Streamlit dentro del entorno de Colab y crear un túnel accesible externamente.

---

## 3.2. Aplicación inicial

El archivo generado en esa etapa se llama:

```text
medical_chatbot_streamlit.py
```

La aplicación usa:

```python
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
import re
import io
import torch
from transformers import pipeline
```

La interfaz se presenta como:

```text
🩺 MediBot: Visualización de Datos y Chatbot Médico
```

---

# 4. Dataset de la etapa inicial

En `StreamLit_ProyectoFinal.ipynb`, el dataset se carga desde:

```text
/content/test.csv
```

La función:

```python
def cargar_datos():
```

utiliza:

```python
df = pd.read_csv("/content/test.csv")
```

La aplicación comprueba la existencia de la columna:

```text
Conversation
```

y muestra error si no está disponible.

---

# 5. Procesamiento inicial del dataset

En la demo de Colab se calcularon tres características principales de cada conversación:

```python
df_proc["longitud"]
df_proc["palabras"]
df_proc["oraciones"]
```

Concretamente:

- longitud en caracteres;
- número de palabras;
- número de oraciones.

Las funciones usadas fueron:

```python
len(str(x))
len(str(x).split())
len(re.split(r'[.!?]+', str(x))) - 1
```

---

# 6. Funcionalidades de la primera demo

`StreamLit_ProyectoFinal.ipynb` presenta cinco secciones:

```text
🤖 Chatbot Médico
📊 Vista de Datos
📈 Estadísticas
☁ Nube de Palabras
🏷 Clasificación de Temas
```

---

## 6.1. Chatbot inicial

La primera versión no utilizaba todavía el RAG definitivo.

Usaba respuestas simuladas almacenadas en un diccionario:

```python
respuestas = {
    "dolor de cabeza": "...",
    "fiebre": "...",
    "tos": "...",
    "default": "..."
}
```

La aplicación buscaba palabras clave dentro de la pregunta y seleccionaba una respuesta predefinida.

Por tanto, esta parte corresponde a una **demo inicial**, no al RAG final.

---

## 6.2. Vista de datos

La aplicación permitía mostrar ejemplos aleatorios del dataset.

Incluía un slider para seleccionar entre:

```text
1 a 20 ejemplos
```

y utilizaba:

```python
df["Conversation"].sample(
    n_mostrar,
    random_state=42
)
```

---

## 6.3. Estadísticas

La página de estadísticas mostraba:

```text
Total Conversaciones
Promedio Longitud
Promedio Palabras
Promedio Oraciones
```

También se generaban histogramas mediante Plotly.

---

## 6.4. Nube de palabras

La demo juntaba las conversaciones en un único texto y calculaba las palabras más frecuentes.

Se utilizaba:

```python
Counter
WordCloud
matplotlib
```

---

## 6.5. Clasificación inicial de temas

Se cargaba un pipeline de Hugging Face:

```python
pipeline(
    "text-classification",
    model="facebook/opt-350m",
    return_all_scores=True
)
```

Esta clasificación era una demo de temas, no el clasificador final de seis especialistas.

---

# 7. Exposición de Streamlit desde Colab

`StreamLit_ProyectoFinal.ipynb` incluye:

```python
!streamlit run medical_chatbot_streamlit.py &>/content/logs.txt &
```

y:

```python
!cloudflared tunnel --url http://localhost:8501 >/content/hola.log 2>&1&
```

Después espera unos segundos y busca en el log una línea que contenga:

```text
trycloudflare
```

Con esto se obtenía una URL pública temporal.

También existe:

```python
def kill():
    !pkill streamlit
```

para detener la instancia de Streamlit.

---

# 8. Evolución hacia el RAG: `MediChat.ipynb`

El notebook `MediChat.ipynb` representa una etapa posterior y mucho más cercana al sistema definitivo.

El encabezado de la aplicación es:

```text
MediBot – 6 Especialistas RAG (Local + Gemini)
```

y el sistema ya utiliza:

- Chroma;
- RecursiveCharacterTextSplitter;
- RetrievalQA;
- documentos LangChain;
- prompts;
- embeddings;
- Ollama;
- Gemini;
- clasificación;
- traducción;
- seis categorías médicas.

---

# 9. Dependencias iniciales del notebook `MediChat.ipynb`

En la primera celda aparecen instrucciones para instalar:

```bash
pip install streamlit pandas langchain langchain-community langchain-google-genai google-generativeai chromadb langchain-ollama ollama python-dotenv
```

También aparece:

```bash
ollama serve
```

Esto muestra que la ejecución local con Ollama era parte de esta etapa del desarrollo.

---

# 10. Dataset de la versión RAG

`MediChat.ipynb` usa como dataset:

```text
C:\Users\jelop\OneDrive\Documentos\U\2025-2\Pyoyecto_PLN_Local\DataSet\dataset_clasificado_PC\dataset_clasificado_PC.csv
```

El notebook comprueba que existan las columnas:

```text
Pregunta
Respuesta
Categoria
```

También muestra:

```python
len(df)
```

y una cuenta de categorías:

```python
df["Categoria"].value_counts()
```

---

# 11. Seis especialistas médicos

Las categorías utilizadas por la arquitectura RAG son:

```python
CATEGORIAS = [
    "Symptom/Diagnosis",
    "Treatment/Medication",
    "Prevention/Health Advice",
    "Test/Interpretation",
    "Emergency/Critical",
    "Post-surgery/Recovery"
]
```

Estas categorías se mantienen en la versión local posterior.

---

# 12. Primer diseño de RAG

En `MediChat.ipynb`, cada categoría se filtra:

```python
subdf = _df[_df["Categoria"] == cat]
```

Después se generan documentos:

```python
Document(
    page_content=f"Q: {r.Pregunta}\nA: {r.Respuesta}",
    metadata={"cat": cat}
)
```

---

# 13. Fragmentación de documentos

El notebook utiliza:

```python
RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=100
)
```

Esto se mantiene posteriormente en `medi_bot_local.py`.

---

# 14. Chroma en la etapa RAG

La implementación del notebook crea la base con:

```python
Chroma.from_documents(
    chunks,
    embeddings,
    collection_name=f"medi_{...}",
    persist_directory="./chroma_local"
)
```

Los retrievers utilizan:

```python
search_kwargs={"k": 6}
```

Por tanto, el primer diseño registrado ya trabajaba con recuperación de:

```text
k = 6
```

documentos/casos similares.

---

# 15. Modo online inicial: Gemini

En `MediChat.ipynb`, el modo online originalmente estaba definido como:

```text
Online (Gemini 2.5 Flash)
```

El modelo era:

```python
ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=api_key,
    temperature=0.3
)
```

Los embeddings eran:

```python
GoogleGenerativeAIEmbeddings(
    model="models/text-embedding-004",
    google_api_key=api_key
)
```

Esto corresponde a la etapa del notebook y no debe confundirse con la configuración posterior de `medi_bot_local.py`.

---

# 16. Modo local inicial: Ollama

El notebook utilizaba:

```python
ChatOllama(
    model="llama3.1:8b",
    temperature=0.3
)
```

y:

```python
OllamaEmbeddings(
    model="mxbai-embed-large:latest"
)
```

Por tanto, `llama3.1:8b` aparece de forma consistente como el modelo LLM local del proyecto.

---

# 17. Flujo de interacción en `MediChat.ipynb`

La versión RAG del notebook implementa:

```text
Pregunta del usuario
       ↓
Traducción
       ↓
Clasificación
       ↓
Selección del especialista
       ↓
Retriever
       ↓
RetrievalQA
       ↓
Respuesta en inglés
       ↓
Traducción al español
```

Si la categoría es:

```text
Emergency/Critical
```

se muestra un flujo de emergencia diferente.

---

# 18. Prompt del RAG en `MediChat.ipynb`

En esa etapa el prompt era:

```text
You are a highly specialized doctor in {categoria}.
Answer empathetically and precisely in English, using only real similar cases.

Context: {context}
Question: {question}
Answer:
```

Posteriormente el prompt fue ajustado en `medi_bot_local.py`.

---

# 19. Prompt actual del RAG

La versión local actual utiliza:

```text
You are a medical expert. Use ONLY the context below.
If no relevant info, say: "No similar cases found, but here's general advice:"

Context:
{context}

Question: {question}
Answer in English:
```

El objetivo registrado en el desarrollo fue reforzar que la generación utilice únicamente el contexto recuperado y mantenga la respuesta en inglés antes de traducirla.

---

# 20. Prompt actual del clasificador

El clasificador actual utiliza:

```text
You are a medical triage assistant.
Classify the following patient question into ONE of the categories below:

{CATEGORIAS}

Question:
{pregunta_en}

Respond ONLY with the category name.
```

La función intenta identificar posteriormente cuál de las categorías válidas aparece en la respuesta.

---

# 21. Prompt actual de traducción

La versión local utiliza:

```text
Translate to English (only text, no quotes):

{texto}
```

o:

```text
Translate to Spanish (only text, no quotes):

{texto}
```

El propósito es pedir solamente el texto traducido.

---

# 22. Versión local: `medi_bot_local.py`

El archivo `medi_bot_local.py` es la evolución local del proyecto.

Su título es:

```text
medi_bot_local.py – RAGs con 6 especialistas + recreación segura Chroma
```

La interfaz se configura como:

```text
MediBot Pro – 6 Especialistas RAG
```

y muestra:

```text
Modo Dual: Local (Ollama) ↔ Online (Gemini 2.5 Pro)
```

---

# 23. Modos actuales del archivo local

La barra lateral permite seleccionar:

```text
Local (Ollama – 100% offline)
Online (Gemini – más rápido)
```

El modo local aparece seleccionado por defecto.

---

# 24. Configuración actual de Gemini

En `medi_bot_local.py`, el modo online utiliza:

```python
ChatGoogleGenerativeAI(
    model="gemini-2.5-pro",
    google_api_key=api_key
)
```

y:

```python
GoogleGenerativeAIEmbeddings(
    model="models/embedding-004",
    google_api_key=api_key
)
```

Esta es la configuración actual del archivo local compartido.

---

# 25. Configuración actual de Ollama

La versión local utiliza:

```python
ChatOllama(
    model="llama3.1:8b",
    temperature=0.3
)
```

y:

```python
OllamaEmbeddings(
    model="mxbai-embed-large"
)
```

---

# 26. Prueba de conexión con Ollama: `test_final.py`

Antes de ejecutar el MediBot completo se creó un archivo de prueba:

```text
test_final.py
```

Este archivo comprueba cuatro pasos.

### Paso 1

Verifica que Streamlit funciona.

### Paso 2

Intenta importar:

```python
from langchain_ollama import ChatOllama
```

### Paso 3

Intenta crear:

```python
ChatOllama(
    model="llama3.1:8b",
    temperature=0.0,
    request_timeout=120
)
```

### Paso 4

Ejecuta:

```python
llm.invoke(
    "Responde solo con la palabra: FUNCIONA"
)
```

Si todo sale bien, muestra:

```text
¡TODO FUNCIONA! Ya puedes usar el MediBot completo
```

También indica explícitamente que `ollama serve` debe estar corriendo y que `llama3.1:8b` debe estar descargado.

---

# 27. Dependencias actuales registradas

El archivo `requeriments.txt` contiene:

```text
langchain 1.1.0
langchain-classic 1.0.0
langchain-community 0.4.1
langchain-core 1.1.0
langchain-google-genai 0.0.1
langchain-ollama 1.0.0
langchain-text-splitters 1.0.0
langchain-ollama 1.0.0
ollama 0.6.1
chromadb 1.3.5
streamlit 1.51.0
```

Se observa que `langchain-ollama` aparece dos veces en el archivo.

---

# 28. Dataset de la versión local actual

`medi_bot_local.py` carga:

```text
dataset_clasificado_PC.csv
```

desde una ruta fija de Windows:

```text
C:\Users\jelop\OneDrive\Documentos\U\2025-2\Pyoyecto_PLN_Local\DataSet\dataset_clasificado_PC\dataset_clasificado_PC.csv
```

La lectura se hace mediante:

```python
pd.read_csv(
    ruta,
    on_bad_lines="skip",
    engine="python"
)
```

---

# 29. Tamaño del corpus

Durante el desarrollo se indicó que el dataset utilizado en el proyecto es de aproximadamente:

```text
100.000 registros
```

El volumen del corpus fue relevante porque la construcción de embeddings en una sola operación podía producir un consumo elevado de memoria.

---

# 30. Solución de batching

La versión local actual utiliza:

```python
BATCH_SIZE = 4000
```

Los chunks se insertan mediante:

```python
db.add_documents(batch)
```

en lugar de intentar introducir todos los documentos en una sola llamada.

---

# 31. Barra de progreso de construcción

Durante la generación de cada especialista se utiliza:

```python
st.progress(...)
```

La cantidad de batches se calcula y la barra se actualiza después de cada batch.

Esto hace visible el avance de la creación de cada base vectorial.

---

# 32. Estructura de almacenamiento Chroma actual

En la versión local:

```python
base = "./chroma_db_gemini" if "Online" in _modo else "./chroma_db_llama"
```

Por tanto existen dos raíces:

```text
./chroma_db_llama
./chroma_db_gemini
```

La separación corresponde a los dos sistemas de embeddings diferentes.

---

# 33. Bases por especialista

Dentro de cada raíz se crea un directorio por categoría.

El nombre se obtiene con:

```python
cat.lower().replace("/", "_").replace(" ", "_")
```

Conceptualmente la estructura es:

```text
chroma_db_llama/
    symptom_diagnosis/
    treatment_medication/
    prevention_health_advice/
    test_interpretation/
    emergency_critical/
    ...

chroma_db_gemini/
    symptom_diagnosis/
    treatment_medication/
    prevention_health_advice/
    test_interpretation/
    emergency_critical/
    ...
```

---

# 34. Recreación de ChromaDB

La interfaz contiene:

```text
Forzar recreación ChromaDB
```

Cuando se activa, cada especialista puede ser reconstruido.

El código también tiene funciones para cerrar/resetear un cliente Chroma y eliminar el directorio de forma segura, reintentando ante `PermissionError`.

---

# 35. Retriever actual

La versión local crea:

```python
retriever = db.as_retriever(
    search_kwargs={"k": 6}
)
```

Por tanto:

```text
6
```

es el número de documentos recuperados en la configuración actual.

---

# 36. RetrievalQA actual

La aplicación crea:

```python
RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type_kwargs={"prompt": prompt},
    return_source_documents=True
)
```

La opción:

```python
return_source_documents=True
```

permite mostrar las fuentes recuperadas.

---

# 37. Flujo actual de la pregunta

Cuando el usuario escribe una pregunta:

```text
1. Pregunta en español
2. Traducción ES → EN
3. Clasificación
4. Especialista asignado
5. Recuperación de casos similares
6. Generación del resultado en inglés
7. Traducción EN → ES
8. Respuesta al usuario
9. Visualización de fuentes
```

---

# 38. Flujo para `Emergency/Critical`

Si la clasificación produce:

```text
Emergency/Critical
```

el sistema no continúa con el RAG normal.

Muestra:

```text
¡EMERGENCIA! Llama a los servicios de urgencia de tu país ahora mismo.
```

---

# 39. Fuentes mostradas

La interfaz muestra un expander:

```text
Fuentes (en inglés)
```

y enseña como máximo las tres primeras fuentes:

```python
result["source_documents"][:3]
```

El texto de cada fuente se limita a aproximadamente:

```text
600 caracteres
```

para su visualización.

---

# 40. Historial de conversación

La aplicación utiliza:

```python
st.session_state.messages
```

para conservar la conversación durante la sesión de Streamlit.

El flujo muestra cada mensaje con:

```python
st.chat_message(...)
```

y la entrada se realiza mediante:

```python
st.chat_input(...)
```

---

# 41. Caché de Streamlit

Se utiliza:

```python
@st.cache_resource
```

para:

```text
cargar_modelos()
crear_rags_especializados()
```

La finalidad es reutilizar recursos y evitar reconstrucciones innecesarias dentro de la ejecución de Streamlit.

---

# 42. Estructura lógica del proyecto actual

```text
MediBot
│
├── Etapa Colab inicial
│   ├── StreamLit_ProyectoFinal.ipynb
│   ├── medical_chatbot_streamlit.py
│   └── cloudflared
│
├── Etapa RAG
│   └── MediChat.ipynb
│
├── Versión local
│   ├── medi_bot_local.py
│   ├── test_final.py
│   └── requeriments.txt
│
└── Bases persistentes generadas
    ├── chroma_db_llama/
    └── chroma_db_gemini/
```

---

# 43. Diferencias entre las etapas

| Elemento | `StreamLit_ProyectoFinal.ipynb` | `MediChat.ipynb` | `medi_bot_local.py` |
|---|---|---|---|
| Entorno registrado | Google Colab | Desarrollo de MediChat | Local |
| Streamlit | Sí | Sí | Sí |
| Cloudflared | Sí | No | No |
| Chatbot | Demo | RAG | RAG |
| Chroma | No | Sí | Sí |
| Seis especialistas | No | Sí | Sí |
| Ollama | No en la app demo | Sí | Sí |
| Gemini | No en la app demo | Gemini 2.5 Flash | Gemini 2.5 Pro |
| Clasificación | HF demo | Sí | Sí |
| Traducción | No | Sí | Sí |
| Batch 4000 | No | No | Sí |
| Barra por batch | No | No | Sí |
| Persistencia separada por modo | No | No, una ruta `./chroma_local` | Sí |

---

# 44. Parámetros actuales importantes

La configuración registrada en `medi_bot_local.py` es:

```text
Dataset:             dataset_clasificado_PC.csv
Registros:           ~100.000
Categorías:          6
Chunk size:          800
Chunk overlap:       100
Retriever k:         6
Batch size:          4000
LLM local:           llama3.1:8b
Temperatura local:   0.3
Embeddings locales:  mxbai-embed-large
LLM online:          gemini-2.5-pro
Embeddings online:   models/embedding-004
```

---

# 45. Decisiones importantes del desarrollo

## 45.1. Separar por especialistas

En lugar de utilizar una sola base vectorial para todo el corpus, el proyecto divide los casos por categoría.

La pregunta se clasifica primero y después se utiliza el RAG correspondiente.

## 45.2. Trabajar en inglés en la capa RAG

Las conversaciones médicas y el proceso de recuperación/generación se manejan en inglés.

El usuario, sin embargo, interactúa en español.

## 45.3. Utilizar Chroma persistente

La intención es no reconstruir todas las bases cada vez que se inicia la aplicación.

## 45.4. Separar embeddings local y online

Se mantienen diferentes directorios porque los embeddings se producen con modelos distintos.

## 45.5. Procesar grandes volúmenes por lotes

El batch de 4000 se incorporó específicamente para evitar saturar la memoria durante la construcción.

---

# 46. Problemas técnicos registrados durante el desarrollo

Se documentaron problemas relacionados con:

- consumo de memoria durante la creación de RAG;
- Chroma/SQLite;
- permisos o bloqueo de directorios de Chroma;
- problemas de importación de `sentence-transformers`;
- problemas de conexión/ejecución de Ollama durante las pruebas.

Para Chroma se creó una estrategia de cierre/reset antes de eliminar directorios.

Para Ollama se creó `test_final.py` como prueba independiente.

---

# 47. Elementos que pertenecen a etapas anteriores y no a la versión final

Hay características de las primeras demos que no deben interpretarse como componentes del MediBot RAG actual:

```text
facebook/opt-350m
```

como clasificador de temas de la demo inicial;

respuestas manuales para:

```text
dolor de cabeza
fiebre
tos
```

y la estructura de cinco páginas de la demo inicial.

Estas características pertenecen a `StreamLit_ProyectoFinal.ipynb`.

---

# 48. Elementos que fueron cambiando de nombre/configuración

Durante la evolución hubo cambios claros:

### Gemini

```text
Etapa MediChat.ipynb:
gemini-2.5-flash
```

posteriormente:

```text
Versión local:
gemini-2.5-pro
```

### Embeddings Gemini

En el notebook:

```text
models/text-embedding-004
```

En la versión local:

```text
models/embedding-004
```

### Embeddings Ollama

Notebook:

```text
mxbai-embed-large:latest
```

Versión local:

```text
mxbai-embed-large
```

---

# 49. Archivo de prueba

El archivo:

```text
test_final.py
```

se diseñó como diagnóstico antes de ejecutar el sistema completo.

Comprueba:

```text
Streamlit
↓
langchain-ollama
↓
conexión con Ollama
↓
respuesta de llama3.1:8b
```

---

# 50. Estado documentado del proyecto

La versión más avanzada entregada en los archivos es `medi_bot_local.py`.

Esta versión reúne:

```text
Streamlit
+
Ollama
+
Gemini
+
Chroma
+
RetrievalQA
+
6 especialistas
+
Traducción
+
Clasificación
+
Fuentes
+
Persistencia
+
Batch de 4000
+
Barra de progreso
```

El proyecto, por tanto, pasó de una demo de chatbot médico ejecutada en Colab a una arquitectura RAG especializada con ejecución local y una alternativa online.

---

# 51. Resumen de evolución

```text
                    PROYECTO MEDIBOT
                           │
                           ▼
                 Dataset de conversaciones
                           │
                           ▼
              ┌──────────────────────────┐
              │ Demo inicial en Colab    │
              │ Streamlit + visualización│
              │ + chatbot simulado       │
              └────────────┬─────────────┘
                           │
                           ▼
              ┌──────────────────────────┐
              │ MediChat.ipynb            │
              │ RAG + Chroma + 6 áreas   │
              │ Ollama + Gemini           │
              └────────────┬─────────────┘
                           │
                           ▼
              ┌──────────────────────────┐
              │ medi_bot_local.py        │
              │ Versión local avanzada   │
              │                           │
              │ Batch = 4000             │
              │ Progreso por batch       │
              │ Chroma persistente       │
              │ Ollama + Gemini 2.5 Pro  │
              └──────────────────────────┘
```

---

# 52. Archivos principales

```text
MediChat.ipynb
```

Notebook de la etapa RAG local + Gemini.

```text
StreamLit_ProyectoFinal.ipynb
```

Notebook de la demo inicial en Colab con Streamlit y Cloudflare Tunnel.

```text
medi_bot_local.py
```

Aplicación local avanzada del MediBot.

```text
test_final.py
```

Prueba de Streamlit + `langchain-ollama` + Ollama + `llama3.1:8b`.

```text
requeriments.txt
```

Dependencias y versiones registradas para el entorno actual documentado.

---

# 53. Nota sobre reproducibilidad

La ruta del dataset que aparece en los notebooks y en `medi_bot_local.py` es una ruta absoluta de Windows:

```text
C:\Users\jelop\OneDrive\Documentos\U\2025-2\...
```

Por lo tanto, para ejecutar el proyecto en otra máquina esa ruta debe apuntar al lugar donde realmente se encuentre el dataset.

Además, la parte local depende de que Ollama esté instalado y de que el modelo:

```text
llama3.1:8b
```

esté disponible.

La parte online depende de una Google API Key.

---

# 54. Conclusión

MediBot comenzó como una demo de chatbot y visualización de conversaciones en Google Colab. Posteriormente se incorporó una arquitectura RAG con seis categorías médicas, Chroma, recuperación de casos similares, traducción y clasificación.

La versión local `medi_bot_local.py` representa la evolución más avanzada disponible en los archivos proporcionados. Esta versión añade persistencia separada para los modos local/online y procesamiento por batches de 4000 con barra de progreso para abordar el tamaño del corpus, indicado durante el desarrollo como aproximadamente 100.000 registros.

La arquitectura final registrada puede resumirse como:

```text
Usuario
  ↓
Pregunta en español
  ↓
Traducción ES → EN
  ↓
Clasificación médica
  ↓
Uno de 6 especialistas
  ↓
Chroma
  ↓
6 casos recuperados
  ↓
LLM
  ↓
Respuesta en inglés
  ↓
Traducción EN → ES
  ↓
Respuesta + fuentes
```
