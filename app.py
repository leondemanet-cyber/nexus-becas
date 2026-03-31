import streamlit as st
from pypdf import PdfWriter, PdfReader
import io

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Nexus | Fusión Documental", layout="centered", page_icon="⚡")

# --- 2. DISEÑO FUTURISTA (Inyección de CSS) ---
st.markdown("""
    <style>
    /* Fondo oscuro y texto claro */
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    /* Estilo del botón principal de fusión */
    .stButton>button {
        border-radius: 8px;
        background-color: #1E3A8A;
        border: 1px solid #3B82F6;
        color: white;
        transition: all 0.3s ease-in-out;
        width: 100%;
        font-weight: bold;
    }
    .stButton>button:hover {
        box-shadow: 0 0 15px #3B82F6;
        border-color: #60A5FA;
    }
    /* Estilo del botón de descarga (Verde éxito) */
    .stDownloadButton>button {
        border-radius: 8px;
        background-color: #059669;
        border: 1px solid #10B981;
        color: white;
        width: 100%;
        font-weight: bold;
        margin-top: 15px;
    }
    .stDownloadButton>button:hover {
        box-shadow: 0 0 15px #10B981;
        border-color: #34D399;
    }
    /* Ocultar elementos por defecto de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 3. INTERFAZ DE USUARIO ---
st.title("⚡ Sistema Nexus: Fusión de Antecedentes")
st.markdown("Carga los documentos PDF de la postulación para generar un archivo maestro consolidado y listo para la auditoría.")

st.divider()

# --- 4. LÓGICA DE SUBIDA Y FUSIÓN ---
# Widget para subir múltiples archivos
archivos_subidos = st.file_uploader(
    "Arrastra o selecciona los PDFs a evaluar", 
    type="pdf", 
    accept_multiple_files=True
)

if archivos_subidos:
    st.success(f"Se han cargado {len(archivos_subidos)} documentos correctamente en la bandeja.")
    
    # Botón de acción
    if st.button("Fusionar Documentos Ahora"):
        with st.spinner("Procesando y alineando archivos..."):
            merger = PdfWriter()
            
            try:
                # Iterar sobre cada archivo subido y agregarlo al unificador
                for pdf in archivos_subidos:
                    reader = PdfReader(pdf)
                    merger.append(reader)
                
                # Guardar el resultado en la memoria temporal (BytesIO)
                pdf_bytes = io.BytesIO()
                merger.write(pdf_bytes)
                pdf_bytes.seek(0)
                
                st.success("¡Fusión completada con éxito!")
                
                # Mostrar botón para descargar el archivo final
                st.download_button(
                    label="⬇️ Descargar Archivo Maestro",
                    data=pdf_bytes,
                    file_name="antecedentes_consolidados.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"Ocurrió un error al procesar los archivos: {e}")
else:
    st.info("Esperando archivos... Por favor, sube al menos un PDF para comenzar el proceso.")