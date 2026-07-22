# Agente Vinanzas

Acceso público del proyecto: http://157.151.140.108:8501/

Agente conversacional de inteligencia artificial diseñado para consultar información contenida en documentos PDF de forma rápida, clara y centralizada. El proyecto permite hacer preguntas en lenguaje natural sobre políticas internas, procedimientos, procesos operativos y otras guías documentadas, facilitando el acceso a información clave sin necesidad de revisar manualmente cada archivo.

## Descripción general del proyecto

Este proyecto transforma una carpeta de documentos PDF en una herramienta de consulta inteligente. Al cargar los archivos, el agente puede responder preguntas basadas en el contenido disponible, lo que lo convierte en un asistente útil para consultar información corporativa, políticas y procedimientos.

## Arquitectura de la solución implementada

La solución está compuesta por los siguientes componentes:

1. Carga de documentos PDF
   - Se recorren automáticamente los archivos ubicados en la carpeta de documentos.
   - Cada PDF se lee y se convierte en texto para su posterior análisis.

2. Motor de conversación
   - El usuario escribe una pregunta en lenguaje natural desde una interfaz web.
   - El sistema envía el contexto y la pregunta al modelo de IA.

3. Modelo de lenguaje
   - Se utiliza Google Gemini para generar respuestas basadas en el contenido de los documentos cargados.

4. Interfaz de usuario
   - Streamlit ofrece una experiencia simple y rápida para interactuar con el agente desde el navegador.

### Vista general de la arquitectura

```text
Usuario -> Streamlit -> Prompt + contexto PDF -> Gemini -> Respuesta
``` 

## Tecnologías y herramientas utilizadas

- Python
- Streamlit
- LangChain
- LangChain Community
- Google Gemini
- PyPDF
- python-dotenv

## Requisitos

Para ejecutar el proyecto es necesario contar con:

- Python 3.10 o superior.
- Las dependencias listadas en el archivo requirements.txt.
- Una clave de API de Google Gemini configurada como variable de entorno:

```bash
GOOGLE_API_KEY=tu_api_key
```

## Instrucciones para ejecutar el proyecto

1. Instala las dependencias:

```bash
pip install -r requirements.txt
```

2. Configura la variable de entorno con tu clave de Google Gemini.

3. Coloca los archivos PDF en la carpeta pdfs.

4. Ejecuta la aplicación:

```bash
streamlit run chatbot.py
```

5. Abre la URL que aparece en el navegador y comienza a hacer preguntas.

## Ejemplos de preguntas que el agente puede responder

- ¿Cuál es el procedimiento para realizar una solicitud de judicialización?
- ¿Qué se debe hacer en caso de una pérdida operacional?
- ¿Cuál es el proceso de reclutamiento y selección de colaboradores?
- ¿Qué indica el documento sobre control de accesos y administración de identidades?
- ¿Qué pasos se deben seguir para gestionar cobranzas?

## Ejemplos de respuestas generadas por el agente

Ejemplo de respuesta esperada:

```text
Según el documento cargado, el procedimiento indica que se debe seguir una serie de pasos definidos para validar la solicitud, registrar la información correspondiente y dar seguimiento hasta su cierre.
```

Otro ejemplo:

```text
No encontré esa información en los documentos cargados. Podría compartir el nombre del procedimiento o el documento al que se refiere para ayudarme a ubicar la respuesta.
```

 