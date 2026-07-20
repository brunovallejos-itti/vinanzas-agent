from dotenv import load_dotenv

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

from langchain_openai import ChatOpenAI

from langchain.chains import RetrievalQA

load_dotenv()

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = FAISS.load_local(
    "faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)

retriever = db.as_retriever(
    search_kwargs={"k": 4}
)

llm = ChatOpenAI(
    model="gpt-5.5"
)

qa = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True
)

print("PDF Chatbot")
print("Type 'exit' to quit.\n")

while True:

    question = input("> ")

    if question.lower() == "exit":
        break

    result = qa.invoke({"query": question})

    print("\nAnswer:")
    print(result["result"])

    print("\nSources:")

    for doc in result["source_documents"]:
        print(
            f"- {doc.metadata['source']} "
            f"(page {doc.metadata.get('page', '?') + 1})"
        )

    print()
