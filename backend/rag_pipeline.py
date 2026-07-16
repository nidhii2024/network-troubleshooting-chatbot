"""
rag_pipeline.py

Loads the vector database, embedding model, retriever,
and Llama 3.2 to answer networking questions using RAG.
"""

from pathlib import Path

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from backend.prompts import SYSTEM_PROMPT


# ==========================================================
# Project Paths
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent
CHROMA_DIR = BASE_DIR / "chroma_db"


# ==========================================================
# Load Embedding Model
# ==========================================================

print("Loading embedding model...")

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

print("Embedding model loaded.")


# ==========================================================
# Load ChromaDB
# ==========================================================

print("Loading Chroma database...")

vector_store = Chroma(
    persist_directory=str(CHROMA_DIR),
    embedding_function=embeddings,
)

print("✅ ChromaDB loaded successfully.")


# ==========================================================
# Create Retriever
# ==========================================================

retriever = vector_store.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 6,
        "fetch_k": 20,
        "lambda_mult": 0.7,
    },
)

print("✅ Retriever created.")


# ==========================================================
# Load Llama 3.2
# ==========================================================

print("Loading Llama 3.2...")

llm = ChatOllama(
    model="llama3.2",
    temperature=0.2,
)

print("✅ Llama 3.2 loaded.")


# ==========================================================
# Prompt Template
# ==========================================================

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        (
            "human",
            """
Answer the user's question using the Cisco documentation below.

If the documentation completely answers the question,
use it as the primary source.

If the documentation is incomplete,
combine it with your networking knowledge,
but clearly distinguish documented facts from general networking knowledge.

Cisco Documentation
-------------------
{context}

User Question
-------------
{question}

Always answer in Markdown.
""",
        ),
    ]
)

chain = prompt | llm | StrOutputParser()


# ==========================================================
# Main RAG Function
# ==========================================================

# ==========================================================
# Helper Function
# ==========================================================

def _build_context(question: str) -> str:
    """
    Retrieve relevant Cisco documents and
    combine them into one context string.
    """

    documents = retriever.invoke(question)

    context = ""

    for doc in documents:
        context += doc.page_content + "\n\n"

    return context


# ==========================================================
# Normal (Non-streaming) Function
# ==========================================================

def ask_network_question(question: str) -> str:
    """
    Returns the complete answer.
    """

    context = _build_context(question)

    answer = chain.invoke(
        {
            "context": context,
            "question": question,
        }
    )

    return answer


# ==========================================================
# Streaming Function
# ==========================================================

def ask_network_question_stream(question: str):
    """
    Streams the answer token-by-token.
    """

    context = _build_context(question)

    messages = prompt.format_messages(
        context=context,
        question=question,
    )

    for chunk in llm.stream(messages):

        if hasattr(chunk, "content") and chunk.content:
            yield chunk.content

# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    question = "I cannot ping another subnet."

    print("=" * 80)
    print("Question:")
    print(question)

    print("=" * 80)
    print("Answer:")
    print(ask_network_question(question))