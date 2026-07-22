# Agente Vinanzas

Agente conversacional de inteligencia artificial diseñado para ayudar a consultar información contenida en documentos PDF de la empresa de forma rápida, sencilla y centralizada. El bot permite hacer preguntas en lenguaje natural sobre políticas internas, procedimientos, procesos operativos y otras guías documentadas, facilitando el acceso a información clave sin necesidad de revisar manualmente cada archivo.

## ¿Qué hace este proyecto?

Este proyecto convierte una carpeta de documentos PDF en una herramienta de búsqueda y consulta inteligente. Al cargar los archivos, el agente puede responder preguntas basadas en el contenido de los documentos disponibles, lo que lo convierte en un asistente útil para consultar información corporativa, políticas y procedimientos.

## Funcionalidades principales

- Lectura automática de archivos PDF almacenados en la carpeta de documentos.
- Búsqueda de información a partir de preguntas en lenguaje natural.
- Respuesta basada en el contenido de los archivos cargados.
- Interfaz sencilla para interactuar con el asistente desde el navegador.

## Tecnologías utilizadas

- Python
- Streamlit
- LangChain
- Google Gemini
- PyPDF

## Requisitos

Para ejecutar el proyecto es necesario contar con:

- Python 3.10 o superior.
- Las dependencias listadas en el archivo **requirements.txt**.
- Una clave de API de Google Gemini configurada como variable de entorno:

> GOOGLE_API_KEY=*tu_api_key*

## Instalación

Desde el entorno donde se ejecutará el proyecto, instala las dependencias con:

```bash
pip install -r requirements.txt
```

## Uso

Ejecuta la aplicación con:

```bash
streamlit run chatbot.py
```

Se abrirá una URL en el navegador donde podrás interactuar con el agente. Para consultar información, coloca los archivos PDF dentro de la carpeta **pdfs** y realiza tus preguntas desde la interfaz.
 