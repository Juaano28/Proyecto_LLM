# MediBot Pro — Contexto del proyecto

## Descripción

MediBot Pro es un proyecto de Procesamiento de Lenguaje Natural (PLN/NLP) orientado a construir un chatbot médico mediante RAG (Retrieval-Augmented Generation).

El proyecto evolucionó desde una primera etapa desarrollada en Google Colab hasta una implementación local con Ollama, ChromaDB y Streamlit. También se conserva un modo online basado en Gemini.

Flujo general del sistema:

Pregunta en español
↓
Traducción ES → EN
↓
Clasificación médica
↓
Selección de especialista
↓
Recuperación de casos similares
↓
Generación mediante LLM
↓
Respuesta en inglés
↓
Traducción EN → ES
↓
Respuesta al usuario + fuentes


## Evolución del proyecto

### 1. Primera etapa — Google Colab

Archivo:

`StreamLit_ProyectoFinal.ipynb`

En esta etapa se desarrolló una primera aplicación de Streamlit ejecutada dentro de Google Colab.

Para poder acceder a la aplicación desde fuera de Colab se utilizó Cloudflare Tunnel mediante `cloudflared`.

La demo incluía:

- Chatbot médico inicial.
- Visualización del dataset.
- Estadísticas.
- Nube de palabras.
- Clasificación de temas.

El chatbot de esta primera versión utilizaba respuestas simuladas mediante palabras clave, por lo que todavía no correspondía al sistema RAG final.


### 2. Segunda etapa — Desarrollo del RAG

Archivo:

`MediChat.ipynb`

En esta etapa se incorporó la arquitectura RAG.

Se añadieron:

- ChromaDB.
- `RetrievalQA`.
- Embeddings.
- Ollama.
- Gemini.
- Traducción.
- Clasificación.
- Seis especialistas médicos.

El dataset utilizado contiene las columnas:

`Pregunta`
`Respuesta`
`Categoria`


### 3. Tercera etapa — Versión local

Archivo principal:

`medi_bot_local.py`

Esta es la versión más avanzada disponible.

La aplicación utiliza Streamlit y permite seleccionar entre:

- Local con Ollama.
- Online con Gemini.

Además incorpora:

- Seis RAG especializados.
- ChromaDB persistente.
- Traducción.
- Clasificación.
- Recuperación de fuentes.
- Batch de 4000 para la creación de embeddings.
- Barra de progreso por cada batch.


## Dataset

El proyecto trabaja con un dataset clasificado de aproximadamente 100.000 registros.

Archivo:

`dataset_clasificado_PC.csv`

Columnas utilizadas:

- `Pregunta`
- `Respuesta`
- `Categoria`

La ruta utilizada actualmente en `medi_bot_local.py` es:

`C:\Users\jelop\OneDrive\Documentos\U\2025-2\Pyoyecto_PLN_Local\DataSet\dataset_clasificado_PC\dataset_clasificado_PC.csv`


## Seis especialistas

El sistema divide los registros en seis categorías:

1. `Symptom/Diagnosis`
2. `Treatment/Medication`
3. `Prevention/Health Advice`
4. `Test/Interpretation`
5. `Emergency/Critical`
6. `Post-surgery/Recovery`

La pregunta del usuario se clasifica primero y posteriormente se utiliza el RAG correspondiente.


## Modelos

### Modo local

LLM:

`llama3.1:8b`

Embeddings:

`mxbai-embed-large`

El LLM local utiliza una temperatura de:

`0.3`


### Modo online

Configuración actual de `medi_bot_local.py`:

LLM:

`gemini-2.5-pro`

Embeddings:

`models/embedding-004`

En una etapa anterior de `MediChat.ipynb` se utilizó:

LLM:

`gemini-2.5-flash`

Embeddings:

`models/text-embedding-004`


## Configuración del RAG

Cada registro válido se convierte en un documento con la estructura:

`Q: pregunta`
`A: respuesta`

Los documentos se dividen utilizando:

`chunk_size = 800`
`chunk_overlap = 100`

El retriever utiliza:

`k = 6`

Las bases de Chroma se separan según el modo:

`./chroma_db_llama`

`./chroma_db_gemini`

Dentro de cada base se generan los especialistas correspondientes a las categorías.


## Procesamiento por batches

Debido al tamaño aproximado del dataset, cercano a 100.000 registros, la versión local utiliza:

`BATCH_SIZE = 4000`

Los documentos se añaden a Chroma mediante:

`db.add_documents(batch)`

La aplicación también utiliza una barra de progreso de Streamlit que se actualiza después de cada batch procesado.

Esto permite evitar la creación de toda la base de embeddings en una única operación y visualizar el avance de construcción de cada especialista.


## Prompts

### Prompt del RAG

You are a medical expert. Use ONLY the context below.
If no relevant info, say: "No similar cases found, but here's general advice:"

Context:
{context}

Question: {question}
Answer in English:


### Prompt del clasificador

You are a medical triage assistant.
Classify the following patient question into ONE of the categories below:

{CATEGORIAS}

Question:
{pregunta_en}

Respond ONLY with the category name.


### Prompt de traducción

Para inglés:

Translate to English (only text, no quotes):

{texto}

Para español:

Translate to Spanish (only text, no quotes):

{texto}


## Flujo de una consulta

1. El usuario escribe una pregunta en español.
2. La pregunta se traduce al inglés.
3. El clasificador determina una de las seis categorías.
4. Se selecciona el RAG correspondiente.
5. Chroma recupera los casos más relevantes.
6. Se entregan los casos recuperados como contexto al LLM.
7. El LLM genera la respuesta en inglés.
8. La respuesta se traduce al español.
9. Se muestra la respuesta al usuario.
10. Se muestran hasta tres fuentes recuperadas.


## Categoría de emergencia

Cuando la clasificación devuelve:

`Emergency/Critical`

el flujo normal del RAG no se ejecuta.

La aplicación muestra:

`¡EMERGENCIA! Llama a los servicios de urgencia de tu país ahora mismo.`


## ChromaDB

La aplicación contiene dos raíces independientes:

`./chroma_db_llama`

para el modo local.

`./chroma_db_gemini`

para el modo online.

La separación permite mantener independientes las bases creadas utilizando diferentes modelos de embeddings.


## Persistencia y recreación

La aplicación comprueba si las bases de cada especialista ya existen.

Si existen, se cargan.

Si no existen, se crean.

También existe una opción en Streamlit:

`Forzar recreación ChromaDB`

que permite reconstruir las bases.

El código incluye funciones para cerrar/resetear el cliente de Chroma y eliminar los directorios antes de reconstruirlos.


## Prueba de Ollama

Archivo:

`test_final.py`

Este archivo se creó para comprobar que el entorno local funciona antes de ejecutar MediBot.

La prueba verifica:

1. Que Streamlit funciona.
2. Que `langchain-ollama` puede importarse.
3. Que Ollama responde.
4. Que `llama3.1:8b` puede generar una respuesta.

La consulta de prueba es:

`Responde solo con la palabra: FUNCIONA`

El archivo también indica que `ollama serve` debe estar ejecutándose y que `llama3.1:8b` debe estar disponible.


## Dependencias

Las versiones registradas en `requeriments.txt` son:

`langchain 1.1.0`
`langchain-classic 1.0.0`
`langchain-community 0.4.1`
`langchain-core 1.1.0`
`langchain-google-genai 0.0.1`
`langchain-ollama 1.0.0`
`langchain-text-splitters 1.0.0`
`ollama 0.6.1`
`chromadb 1.3.5`
`streamlit 1.51.0`

`langchain-ollama` aparece dos veces en el archivo de requisitos original.


## Archivos principales

`StreamLit_ProyectoFinal.ipynb`

Primera demo desarrollada en Google Colab con Streamlit, visualización y Cloudflare Tunnel.

`MediChat.ipynb`

Etapa de desarrollo de la arquitectura RAG con seis especialistas.

`medi_bot_local.py`

Versión local avanzada del sistema.

`test_final.py`

Prueba de funcionamiento de Streamlit, Ollama y `llama3.1:8b`.

`requeriments.txt`

Dependencias del proyecto.


## Arquitectura actual

Dataset médico (~100k registros)
↓
Clasificación por categorías
↓
6 especialistas
↓
Documentos Q + A
↓
Text splitting
↓
Embeddings
↓
ChromaDB
↓
Clasificación de la pregunta
↓
Retriever k=6
↓
Contexto recuperado
↓
Ollama o Gemini
↓
Respuesta en inglés
↓
Traducción al español
↓
Respuesta + fuentes


## Resumen

MediBot comenzó como una aplicación experimental de chatbot y visualización en Google Colab.

Posteriormente evolucionó hacia una arquitectura RAG especializada utilizando conversaciones médicas clasificadas.

La versión local actual utiliza:

- Streamlit como interfaz.
- Ollama como alternativa local.
- `llama3.1:8b` como LLM local.
- `mxbai-embed-large` para embeddings locales.
- Gemini 2.5 Pro como opción online.
- ChromaDB como base vectorial.
- Seis especialistas médicos.
- Traducción ES ↔ EN.
- Clasificación automática.
- Recuperación de 6 casos.
- Procesamiento por batches de 4000.
- Barra de progreso durante la creación de los RAG.