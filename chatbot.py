import os
import streamlit as st #type: ignore
from dotenv import load_dotenv #type: ignore
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader #type: ignore
from langchain_google_genai import ChatGoogleGenerativeAI #type: ignore
from langchain_core.prompts import ChatPromptTemplate #type: ignore
from langchain_core.output_parsers import StrOutputParser #type: ignore

# 1. Load Environment Variables
load_dotenv()

# Anchor PDF_FOLDER to the exact folder where app.py lives
BASE_DIR = Path(__file__).resolve().parent
PDF_FOLDER = BASE_DIR / "pdfs"

st.set_page_config(page_title="PDF Assistant", page_icon="📄")
st.title("📄 Local PDF Assistant")

# 2. Function to load all PDFs recursively from the 'pdfs' directory
@st.cache_data
def load_all_pdfs_from_folder(folder_input: str | Path) -> tuple[str, list[str]]:
    """Recursively scans for valid .pdf / .PDF files, filtering out temporary or unreadable files."""
    folder_path = Path(folder_input)
    folder_path.mkdir(parents=True, exist_ok=True)

    # Search case-insensitively for .pdf and .PDF files at any subfolder depth
    raw_pdf_files = [p for p in folder_path.rglob("*") if p.suffix.lower() == ".pdf"]

    combined_text = []
    loaded_filenames = []

    for pdf_path in raw_pdf_files:
        # Skip temporary or hidden files (like ~$doc.pdf)
        if pdf_path.name.startswith("~$") or pdf_path.name.startswith("."):
            continue

        # Ensure the path is valid and exists on disk
        resolved_str_path = os.path.abspath(str(pdf_path))
        if not os.path.isfile(resolved_str_path):
            continue

        try:
            # Relative path preserves subfolder structure (e.g. "HR Policies/Handbook.pdf")
            relative_path = str(pdf_path.relative_to(folder_path))
            
            # Pass normalized absolute string path to PyPDFLoader
            loader = PyPDFLoader(resolved_str_path)
            pages = loader.load()

            file_text = f"--- Document: {relative_path} ---\n"
            file_text += "\n".join([p.page_content for p in pages])

            combined_text.append(file_text)
            loaded_filenames.append(relative_path)
            
        except Exception as e:
            # Skip corrupted/unreadable PDFs gracefully without crashing the server
            st.warning(f"Skipped unreadable file '{pdf_path.name}': {e}")
            continue

    full_context = "\n\n".join(combined_text)
    return full_context, loaded_filenames

# Load PDF contents immediately on app startup
pdf_context, loaded_files = load_all_pdfs_from_folder(PDF_FOLDER)

# 3. Handle status display
if not loaded_files:
    st.warning(f"No PDFs found in `{PDF_FOLDER}`. Drop some PDF files into the `pdfs/` directory and refresh this page!")
    st.stop()
else:
    st.success(f"Loaded {len(loaded_files)} document(s) from `{PDF_FOLDER.name}/`!")

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