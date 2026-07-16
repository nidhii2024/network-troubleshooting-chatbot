"""
ingest.py

Step 1:
Load all Cisco PDF documents.
"""

import os
from pathlib import Path
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader

# --------------------------------------------------
# Load Environment Variables
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY not found.")

print("✅ OpenAI API Key loaded.")

# --------------------------------------------------
# Project Paths
# --------------------------------------------------

CISCO_DIR = BASE_DIR / "knowledge_base" / "cisco_docs"

# --------------------------------------------------
# Load Cisco PDFs
# --------------------------------------------------

documents = []

print("\nLoading Cisco PDFs...\n")

pdf_files = list(CISCO_DIR.glob("*.pdf"))

if not pdf_files:
    print("❌ No PDF files found.")
else:
    print(f"Found {len(pdf_files)} PDF(s).\n")

for pdf in pdf_files:
    print(f"Loading: {pdf.name}")

    loader = PyPDFLoader(str(pdf))
    docs = loader.load()

    documents.extend(docs)

print("\n--------------------------------")
print(f"Total pages loaded: {len(documents)}")
print("--------------------------------")

# --------------------------------------------------
# Load Q&A JSON
# --------------------------------------------------

import json
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
#print(f"Total LangChain Documents: {len(documents)}")

QNA_FILE = BASE_DIR / "knowledge_base" / "qna_pairs.json"

print("\nLoading Q&A pairs...")

with open(QNA_FILE, "r", encoding="utf-8") as f:
    qna_data = json.load(f)

for item in qna_data:
    documents.append(
        Document(
            page_content=f"Question: {item['question']}\nAnswer: {item['answer']}",
            metadata={
                "source": "qna_pairs.json",
                "type": "qa"
            }
        )
    )

print(f"Loaded {len(qna_data)} Q&A pairs.")

print("\n--------------------------------")
print(f"Total LangChain Documents: {len(documents)}")
print("--------------------------------")
from langchain_text_splitters import RecursiveCharacterTextSplitter
# --------------------------------------------------
# Split Documents into Chunks
# --------------------------------------------------

print("\nSplitting documents into chunks...")

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=150,
)

chunks = text_splitter.split_documents(documents)

print(f"Created {len(chunks)} chunks.")

# Preview the first chunk
print("\nFirst Chunk Preview:")
print("-" * 50)
print(chunks[0].page_content[:500])
print("-" * 50)
# --------------------------------------------------
# Create OpenAI Embeddings
# --------------------------------------------------

print("\nGenerating embeddings...")

print("\nLoading Hugging Face embedding model...")

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# --------------------------------------------------
# Store in ChromaDB
# --------------------------------------------------

print("Creating Chroma database...")

CHROMA_DIR = BASE_DIR / "chroma_db"

vector_store = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory=str(CHROMA_DIR),
)

print("\n✅ ChromaDB created successfully!")
print(f"Database saved to: {CHROMA_DIR}")