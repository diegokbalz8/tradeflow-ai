# TradeFlow AI

TradeFlow AI is an AI-powered Retrieval-Augmented Generation (RAG) assistant designed to answer questions about Costa Rican customs procedures and regulations using official sources.

The long-term goal is to develop a reliable AI customs consulting assistant capable of retrieving, interpreting, and citing relevant Costa Rican customs information while minimizing unsupported or fabricated answers.

## Project Status

**Active development**

TradeFlow currently includes a working RAG pipeline and an automated update system for the Costa Rican **Ley General de Aduanas (Ley N.º 7557)** through the Sistema Costarricense de Información Jurídica (SCIJ).

## Current Features

- Semantic search using OpenAI embeddings
- Retrieval using cosine similarity
- Markdown document chunking based on document structure
- Retrieval from multiple customs knowledge sources
- Source and document metadata
- Relevance validation before answer generation
- Grounded AI-generated answers
- Article-number-aware retrieval for legal queries
- Automated SCIJ version checking
- Download and parsing of updated legal text
- Structural validation of downloaded legislation
- Automatic backup of previous legal versions
- Safe temporary index generation and validation
- Atomic replacement of the production RAG index

## Knowledge Base

TradeFlow currently works with sources including:

- **Ley General de Aduanas — Ley N.º 7557**
- **Manual de Procedimientos Aduaneros**
- Customs entry and exit procedures
- Multimodal customs procedure documentation

The project is being designed around authoritative Costa Rican customs and legal sources rather than unrestricted web-generated information.

## Architecture

```text
Official Source
      ↓
Download / Update
      ↓
Markdown
      ↓
Document Cleaning
      ↓
Structural Chunking
      ↓
Embeddings
      ↓
Vector Index
      ↓
Semantic Retrieval
      ↓
Relevance Validation
      ↓
Grounded Answer
```

For supported SCIJ legislation, TradeFlow also includes an update pipeline:

```text
SCIJ
 ↓
Check Latest Version
 ↓
Download Updated Law
 ↓
Validate Document Structure
 ↓
Backup Previous Version
 ↓
Replace Legal Document
 ↓
Build Temporary Index
 ↓
Validate New Index
 ↓
Replace Production Index
 ↓
Update Version Metadata
```

## Technology

- Python
- OpenAI API
- OpenAI embeddings
- NumPy
- Beautiful Soup
- Requests
- Markdown-based knowledge base
- Git / GitHub

## Project Structure

```text
tradeflow-ai/
│
├── app/
│   ├── chunking.py
│   ├── document_metadata.py
│   ├── embeddings.py
│   ├── generation.py
│   ├── indexer.py
│   ├── relevance.py
│   ├── retrieval.py
│   ├── scij.py
│   ├── scij_parser.py
│   ├── scij_updater.py
│   └── source_selection.py
│
├── knowledge_base/
│   ├── IngresoSalida.md
│   ├── IngresoSalidaMultimodal.md
│   ├── Ley_General_Aduanas.md
│   └── ...
│
├── requirements.txt
├── .gitignore
└── README.md
```

## SCIJ Legal Update System

TradeFlow can check SCIJ for a newer version of the Ley General de Aduanas.

When an update is detected, the updater is designed to:

1. Download the new legal text.
2. Convert it into structured Markdown.
3. Validate the document before accepting it.
4. Back up the previous legal version.
5. Replace the current legal document.
6. Generate a new RAG index in a temporary file.
7. Validate the new index.
8. Replace the production index only after successful validation.
9. Update the stored SCIJ version metadata.

This helps prevent a failed download or embedding operation from directly overwriting the existing production index.

## Running TradeFlow

Create and activate a Python virtual environment and install the dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Create a `.env` file containing the required OpenAI API credentials.

The `.env` file is intentionally excluded from Git.

Build the knowledge index:

```powershell
python -m app.indexer
```

Run TradeFlow:

```powershell
python -m app.main
```

Check SCIJ for legal updates:

```powershell
python -m app.scij_updater
```

## Security

API keys and local credentials must never be committed to the repository.

The project `.gitignore` excludes:

- `.env`
- Python virtual environments
- local credential files
- generated vector indexes
- temporary SCIJ files
- local legal-document backups

## Development Roadmap

Planned improvements include:

- Improved source attribution
- Better ranking across laws, manuals, and procedural documents
- More precise legal citation
- Retrieval deduplication
- Expanded Costa Rican customs knowledge sources
- Improved document update pipelines
- Evaluation datasets for retrieval quality
- Automated RAG testing
- User interface / API layer
- Deployment

## Disclaimer

TradeFlow AI is an experimental software project and is not a substitute for professional legal or customs advice.

Regulatory information should be verified against the applicable official Costa Rican sources before being used for legal, customs, or commercial decisions.