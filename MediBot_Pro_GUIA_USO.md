# MediBot — Guía de uso

## 1. Descripción

Este documento explica cómo utilizar las dos formas de ejecución que aparecen en los archivos del proyecto:

```text
A. Versión de nube / Google Colab
B. Versión local
```

Es importante distinguir las dos etapas:

- `StreamLit_ProyectoFinal.ipynb` es la **demo inicial en Colab**, que utiliza Streamlit + Cloudflare Tunnel.
- `MediChat.ipynb` es la etapa de **RAG con seis especialistas**, con Ollama y Gemini.
- `medi_bot_local.py` es la **versión local avanzada**, con Chroma persistente, batch de 4000 y barra de progreso.

---

# 2. Requisitos generales del proyecto

La versión local documentada utiliza las dependencias registradas en:

```text
requeriments.txt
```

Versiones:

```text
langchain 1.1.0
langchain-classic 1.0.0
langchain-community 0.4.1
langchain-core 1.1.0
langchain-google-genai 0.0.1
langchain-ollama 1.0.0
langchain-text-splitters 1.0.0
ollama 0.6.1
chromadb 1.3.5
streamlit 1.51.0
```

`langchain-ollama` aparece dos veces en el archivo de requisitos proporcionado.

---

# 3. Opción A — Ejecutar la demo en Google Colab

## 3.1. Archivo

La etapa de Colab utiliza:

```text
StreamLit_ProyectoFinal.ipynb
```

Este notebook crea:

```text
medical_chatbot_streamlit.py
```

---

## 3.2. Instalar dependencias

En la primera celda del notebook se utiliza:

```python
!pip install streamlit pandas plotly wordcloud matplotlib transformers torch
```

Ejecuta esa celda.

---

## 3.3. Instalar Cloudflared

Después:

```python
!wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -O cloudflared
!chmod +x cloudflared
!mv cloudflared /usr/local/bin/cloudflared
```

Esto prepara el túnel que permitirá acceder a Streamlit desde fuera de Colab.

---

# 4. Dataset de la demo en Colab

La demo busca:

```text
/content/test.csv
```

El CSV debe contener una columna:

```text
Conversation
```

La aplicación lee el archivo con:

```python
pd.read_csv("/content/test.csv")
```

---

# 5. Ejecutar la aplicación de Colab

El notebook define:

```python
def run():
    !streamlit run medical_chatbot_streamlit.py &>/content/logs.txt &
    !cloudflared tunnel --url http://localhost:8501 >/content/hola.log 2>&1&
    import time
    time.sleep(5)

    with open("/content/hola.log", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if "trycloudflare" in line and "|" in line:
                print(line)
```

La función:

```python
run()
```

hace dos cosas:

1. inicia Streamlit en el puerto `8501`;
2. crea un túnel Cloudflare hacia ese puerto.

Después busca en el archivo `hola.log` la URL pública.

---

# 6. Abrir la aplicación

Después de ejecutar:

```python
run()
```

debes buscar en la salida la URL de `trycloudflare`.

Esa es la dirección pública temporal que permite abrir el MediBot desde el navegador.

---

# 7. Detener la aplicación de Colab

Para detener Streamlit se utiliza:

```python
kill()
```

La función está definida como:

```python
def kill():
    !pkill streamlit
```

Esto detiene los procesos de Streamlit iniciados por el notebook.

---

# 8. Qué ofrece esta versión de Colab

La demo inicial contiene cinco páginas:

```text
🤖 Chatbot Médico
📊 Vista de Datos
📈 Estadísticas
☁ Nube de Palabras
🏷 Clasificación de Temas
```

El chatbot de esta etapa es una **simulación**, no el RAG final.

---

# 9. Opción B — Ejecutar la versión RAG / local

## 9.1. Archivos principales

Para la versión más avanzada utiliza:

```text
medi_bot_local.py
```

y como prueba previa:

```text
test_final.py
```

El dataset utilizado por el código es:

```text
dataset_clasificado_PC.csv
```

---

# 10. Preparar Ollama

La aplicación local usa:

```text
llama3.1:8b
```

como modelo de lenguaje.

También usa:

```text
mxbai-embed-large
```

como modelo de embeddings.

El archivo de prueba `test_final.py` indica explícitamente que Ollama debe estar ejecutándose y que `llama3.1:8b` debe estar descargado.

---

# 11. Comprobar Ollama antes de ejecutar MediBot

Utiliza:

```text
test_final.py
```

La prueba verifica:

```text
1. Streamlit funciona
2. langchain-ollama se puede importar
3. Ollama responde
4. llama3.1:8b genera una respuesta
```

La prueba final envía:

```text
Responde solo con la palabra: FUNCIONA
```

Si todo es correcto, la aplicación muestra:

```text
TODO FUNCIONA! Ya puedes usar el MediBot completo
```

---

# 12. Ejecutar MediBot local

Una vez que Ollama funciona, ejecuta:

```bash
streamlit run medi_bot_local.py
```

La aplicación se abre mediante Streamlit.

---

# 13. Seleccionar el modo

La barra lateral muestra:

```text
Local (Ollama – 100% offline)
Online (Gemini – más rápido)
```

El modo local está seleccionado por defecto.

---

# 14. Usar el modo Local

Selecciona:

```text
Local (Ollama – 100% offline)
```

Este modo utiliza:

```text
LLM:
llama3.1:8b

Embeddings:
mxbai-embed-large
```

La base vectorial correspondiente es:

```text
./chroma_db_llama
```

---

# 15. Usar el modo Online

Selecciona:

```text
Online (Gemini – más rápido)
```

La aplicación solicitará:

```text
Google API Key
```

El código actual utiliza:

```text
LLM:
gemini-2.5-pro

Embeddings:
models/embedding-004
```

La base correspondiente es:

```text
./chroma_db_gemini
```

---

# 16. Primera ejecución de las bases RAG

Si las bases no existen, la aplicación comienza a construirlas.

Para cada una de las seis categorías:

```text
Symptom/Diagnosis
Treatment/Medication
Prevention/Health Advice
Test/Interpretation
Emergency/Critical
Post-surgery/Recovery
```

se crea una base especializada.

---

# 17. Qué ocurre durante la construcción

Los registros del CSV se convierten en documentos:

```text
Q: pregunta
A: respuesta
```

Después se dividen en chunks:

```text
chunk_size = 800
chunk_overlap = 100
```

Los embeddings se generan en lotes:

```text
BATCH_SIZE = 4000
```

Durante la construcción aparece una barra de progreso.

---

# 18. Barra de progreso

La barra representa el avance de los batches de cada especialista.

La intención es evitar procesar todo el corpus de una vez y facilitar el seguimiento visual del proceso.

Con un corpus de aproximadamente 100.000 registros, esta etapa puede ser la parte más pesada de la primera ejecución.

---

# 19. Evitar reconstruir las bases

Una vez creadas las bases, la aplicación comprueba si ya existe contenido en el directorio del especialista.

La aplicación entonces puede mostrar:

```text
📂 Cargando especialista: ...
```

en lugar de:

```text
🔄 (Re)generando especialista: ...
```

---

# 20. Forzar recreación de ChromaDB

En la barra lateral existe:

```text
Forzar recreación ChromaDB
```

Actívala cuando necesites reconstruir las bases.

Por ejemplo, si cambió el dataset y quieres volver a generar los embeddings.

---

# 21. Uso normal del chatbot

Después de que las bases estén disponibles:

1. escribe una pregunta en español;
2. el sistema la traduce al inglés;
3. el clasificador selecciona una categoría;
4. la interfaz muestra el especialista asignado;
5. se buscan casos similares;
6. el LLM genera la respuesta en inglés;
7. la respuesta se traduce al español;
8. se muestran las fuentes recuperadas.

---

# 22. Especialistas

El sistema utiliza seis categorías:

```text
Symptom/Diagnosis
Treatment/Medication
Prevention/Health Advice
Test/Interpretation
Emergency/Critical
Post-surgery/Recovery
```

La clasificación determina cuál RAG se utiliza.

---

# 23. Caso de emergencia

Si la pregunta se clasifica como:

```text
Emergency/Critical
```

el sistema no ejecuta el RAG normal.

Muestra directamente:

```text
¡EMERGENCIA! Llama a los servicios de urgencia de tu país ahora mismo.
```

---

# 24. Cómo funcionan las fuentes

Después de una consulta normal aparece:

```text
Fuentes (en inglés)
```

La aplicación muestra como máximo:

```text
3 fuentes
```

y limita la visualización de cada documento a aproximadamente:

```text
600 caracteres
```

---

# 25. Estructura de las bases

Modo local:

```text
chroma_db_llama/
```

Modo online:

```text
chroma_db_gemini/
```

Dentro de cada una se generan directorios correspondientes a las categorías.

---

# 26. Flujo técnico de una consulta

```text
Usuario
   │
   ▼
Pregunta en español
   │
   ▼
Traducción
ES → EN
   │
   ▼
Clasificación
   │
   ▼
Especialista
   │
   ▼
Retriever
k = 6
   │
   ▼
Contexto recuperado
   │
   ▼
Prompt RAG
   │
   ▼
LLM
   │
   ▼
Respuesta en inglés
   │
   ▼
Traducción
EN → ES
   │
   ▼
Respuesta + fuentes
```

---

# 27. Flujo específico de construcción de RAG

```text
CSV
 │
 ▼
Filtrar por categoría
 │
 ▼
Document(Q + A)
 │
 ▼
RecursiveCharacterTextSplitter
 │
 ├── chunk_size = 800
 └── overlap = 100
 │
 ▼
Batches de 4000
 │
 ▼
Embeddings
 │
 ▼
Chroma persistente
```

---

# 28. Diferencia entre usar la demo de Colab y la versión local

## Colab

La versión:

```text
StreamLit_ProyectoFinal.ipynb
```

es la primera demo del proyecto.

Su objetivo principal era demostrar:

- funcionamiento de Streamlit;
- carga de datos;
- visualización;
- estadísticas;
- nube de palabras;
- clasificación de temas;
- acceso externo mediante Cloudflare Tunnel.

El chatbot de esa etapa usa respuestas simuladas.

---

## RAG / local

La versión:

```text
medi_bot_local.py
```

es la versión avanzada.

Incluye:

- seis RAG;
- Chroma;
- Ollama;
- Gemini;
- clasificación;
- traducción;
- recuperación de casos;
- fuentes;
- persistencia;
- batch de 4000;
- barra de progreso.

---

# 29. Flujo recomendado para una instalación local

```text
1. Instalar las dependencias del requirements
        ↓
2. Instalar/configurar Ollama
        ↓
3. Tener disponible llama3.1:8b
        ↓
4. Ejecutar test_final.py
        ↓
5. Confirmar que Ollama responde
        ↓
6. Ejecutar medi_bot_local.py
        ↓
7. Elegir Local u Online
        ↓
8. Crear/cargar las bases Chroma
        ↓
9. Realizar consultas
```

---

# 30. Flujo recomendado en Google Colab

```text
1. Abrir StreamLit_ProyectoFinal.ipynb
        ↓
2. Instalar dependencias
        ↓
3. Instalar cloudflared
        ↓
4. Tener /content/test.csv
        ↓
5. Ejecutar las celdas para crear medical_chatbot_streamlit.py
        ↓
6. Ejecutar run()
        ↓
7. Abrir la URL trycloudflare
        ↓
8. Usar la demo
        ↓
9. Ejecutar kill() al terminar
```

---

# 31. Archivos y función de cada uno

| Archivo | Uso |
|---|---|
| `StreamLit_ProyectoFinal.ipynb` | Demo inicial en Colab |
| `MediChat.ipynb` | Desarrollo de RAG con 6 especialistas |
| `medi_bot_local.py` | Aplicación local avanzada |
| `test_final.py` | Prueba de Ollama antes de ejecutar MediBot |
| `requeriments.txt` | Dependencias del entorno |

---

# 32. Datos necesarios

Para la versión RAG debe estar disponible:

```text
dataset_clasificado_PC.csv
```

con:

```text
Pregunta
Respuesta
Categoria
```

La versión local actual utiliza la ruta fija definida dentro de `medi_bot_local.py`.

Si el archivo se encuentra en otra ubicación, la ruta del código tendrá que corresponder con esa ubicación.

---

# 33. Modificación del dataset

El sistema espera que las categorías coincidan con exactamente estos nombres:

```text
Symptom/Diagnosis
Treatment/Medication
Prevention/Health Advice
Test/Interpretation
Emergency/Critical
Post-surgery/Recovery
```

Además, para crear los documentos se necesitan:

```text
Pregunta
Respuesta
```

---

# 34. Qué hacer si la base necesita reconstruirse

En la aplicación local:

```text
Forzar recreación ChromaDB
```

Luego vuelve a cargar la aplicación.

El sistema borra/recrea los directorios de cada especialista y vuelve a construir sus embeddings.

---

# 35. Qué hacer si Ollama no responde

Antes de probar el MediBot completo, ejecuta:

```text
test_final.py
```

La propia prueba indica:

```text
Asegúrate de que 'ollama serve' esté corriendo y llama3.1:8b descargado
```

Si la prueba no logra comunicarse con Ollama, la aplicación completa tampoco podrá utilizar el LLM local.

---

# 36. Cuándo utilizar cada versión

### Usa Colab cuando:

quieras utilizar la demo inicial y exponer temporalmente Streamlit mediante un túnel de Cloudflare.

### Usa la versión local cuando:

quieras utilizar la arquitectura RAG de seis especialistas, bases Chroma persistentes y Ollama local.

### Usa el modo Online dentro de la versión local cuando:

quieras utilizar el flujo de Gemini configurado en `medi_bot_local.py` y tengas una Google API Key.

---

# 37. Nota sobre las distintas versiones de Gemini

Durante el desarrollo aparecen dos configuraciones diferentes.

En `MediChat.ipynb`:

```text
gemini-2.5-flash
```

En `medi_bot_local.py`:

```text
gemini-2.5-pro
```

La configuración de `medi_bot_local.py` debe considerarse la de la versión local actual documentada.

---

# 38. Nota sobre los embeddings de Gemini

En `MediChat.ipynb` aparece:

```text
models/text-embedding-004
```

Mientras que `medi_bot_local.py` utiliza:

```text
models/embedding-004
```

Son configuraciones de etapas diferentes del proyecto y no deben mezclarse al reproducir una versión específica.

---

# 39. Resultado esperado

En la versión local, una consulta normal debe seguir aproximadamente este flujo visible:

```text
Traduciendo...
        ↓
Clasificando...
        ↓
Especialista asignado: <categoría>
        ↓
Buscando casos similares...
        ↓
Respuesta en español
        ↓
Fuentes (en inglés)
```

---

# 40. Resumen operativo

## Versión Colab

```text
Google Colab
↓
Streamlit
↓
Cloudflared
↓
URL pública temporal
↓
Demo médica + visualización
```

## Versión local

```text
PC
↓
Ollama / Gemini
↓
Streamlit
↓
Clasificador
↓
RAG especialista
↓
Chroma
↓
LLM
↓
Respuesta
```

---

# 41. Estructura recomendada del repositorio

La estructura exacta del repositorio completo no está completamente presente en los archivos proporcionados, pero, con base en los archivos disponibles, la parte del proyecto documentada puede organizarse así:

```text
/
├── README.md
├── medi_bot_local.py
├── test_final.py
├── requeriments.txt
├── MediChat.ipynb
├── StreamLit_ProyectoFinal.ipynb
├── dataset_clasificado_PC.csv
│
├── chroma_db_llama/
└── chroma_db_gemini/
```

Las carpetas `chroma_db_*` son bases generadas por la ejecución local y no se presentan aquí como archivos que necesariamente deban versionarse en GitHub.

---

# 42. Consideración sobre el uso del sistema

MediBot es un proyecto académico de PLN/RAG orientado a trabajar con conversaciones médicas. La aplicación contiene una categoría de emergencia, pero el código documentado no sustituye la valoración de un profesional sanitario.

