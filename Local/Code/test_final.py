# test_final.py  ← GUARDA CON ESTE NOMBRE
import streamlit as st
st.set_page_config(page_title="TEST", layout="wide")

st.title("PASO 1 → Streamlit funciona")

try:
    from langchain_ollama import ChatOllama
    st.success("PASO 2 → langchain-ollama importado")
except Exception as e:
    st.error(f"Error importando langchain-ollama: {e}")
    st.stop()

try:
    llm = ChatOllama(model="llama3.1:8b", temperature=0.0, request_timeout=120)
    st.success("PASO 3 → Conexión con Ollama OK")
except Exception as e:
    st.error(f"Ollama no responde: {e}")
    st.info("Asegúrate de que 'ollama serve' esté corriendo y llama3.1:8b descargado")
    st.stop()

try:
    respuesta = llm.invoke("Responde solo con la palabra: FUNCIONA")
    st.success(f"PASO 4 → Ollama responde: {respuesta.content}")
except Exception as e:
    st.error(f"Error al hablar con Ollama: {e}")
    st.stop()

st.balloons()
st.write("¡TODO FUNCIONA! Ya puedes usar el MediBot completo")