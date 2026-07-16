from pathlib import Path

# Root of the project
ROOT = Path(".")

# Directories to create
directories = [
    "backend",
    "frontend",
    "knowledge_base",
    "knowledge_base/cisco_docs",
    "knowledge_base/rfcs",
    "chroma_db",
    "scripts",
]

# Files to create
files = [
    "backend/main.py",
    "backend/rag_pipeline.py",
    "backend/prompts.py",
    "backend/ingest.py",
    "backend/utils.py",

    "frontend/app.py",

    "knowledge_base/qna_pairs.json",

    "scripts/start.sh",

    ".env",
    ".gitignore",
    "requirements.txt",
    "README.md",
    "LICENSE",
]

# Create directories
for directory in directories:
    (ROOT / directory).mkdir(parents=True, exist_ok=True)

# Create files
for file in files:
    path = ROOT / file
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch(exist_ok=True)

print("\n✅ Project structure created successfully!\n")

print("Project tree:")
for path in sorted(ROOT.rglob("*")):
    print(path)