import os
import glob
import streamlit as st
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 1. Load Environment Variables
load_dotenv()

PDF_FOLDER = "pdfs"

st.set_page_config(page_title="PDF Assistant", page_icon="📄")
st.title("📄 Local PDF Assistant")

# 2. Function to load all PDFs from the 'pdfs' directory automatically
@st.cache_data
def load_all_pdfs_from_folder(folder_path: str) -> tuple[str, list[str]]:
    """Scans the specified folder and extracts text from all PDF files."""
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        return "", []

    # Find all .pdf files in the folder
    pdf_files = glob.glob(os.path.join(folder_path, "*.pdf"))
    
    if not pdf_files:
        return "", []

    combined_text = []
    loaded_filenames = []

    for pdf_path in pdf_files:
        filename = os.path.basename(pdf_path)
        loader = PyPDFLoader(pdf_path)
        pages = loader.load()
        
        # Merge text content for this file
        file_text = f"--- Document: {filename} ---\n"
        file_text += "\n".join([p.page_content for p in pages])
        
        combined_text.append(file_text)
        loaded_filenames.append(filename)

    full_context = "\n\n".join(combined_text)
    return full_context, loaded_filenames

# Load PDF contents immediately on app startup
pdf_context, loaded_files = load_all_pdfs_from_folder(PDF_FOLDER)

# 3. Handle status display
if not loaded_files:
    st.warning(f"No PDFs found in the `{PDF_FOLDER}/` folder. Drop some PDF files into `{PDF_FOLDER}/` and refresh this page!")
    st.stop()
else:
    st.success(f"Loaded {len(loaded_files)} document(s): {', '.join(loaded_files)}")

# 4. Initialize Gemini Model
@st.cache_resource
def get_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-flash-latest",
        temperature=0.2
    )

llm = get_llm()

# 5. Maintain Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 6. Chat Input & Processing
if user_question := st.chat_input("Ask anything about your loaded PDFs..."):
    # Render user prompt
    st.session_state.messages.append({"role": "user", "content": user_question})
    with st.chat_message("user"):
        st.markdown(user_question)

    # Define LCEL Prompt Chain
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a helpful assistant answering questions based on the local documents provided below.
If the requested answer isn't present in the documents, state that you couldn't find it in the provided files.

LOADED DOCUMENTS:
{context}"""),
        ("human", "{question}")
    ])

    chain = prompt | llm | StrOutputParser()

    # Generate answer
    with st.chat_message("assistant"):
        # Truncate total text to fit within model context limits if necessary
        response = chain.invoke({
            "context": pdf_context[:150000],
            "question": user_question
        })
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})