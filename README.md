# RBI Financial & Operations Risk Guidelines — RAG Chatbot

A retrieval-augmented generation (RAG) system that answers questions about the Reserve Bank of India's Financial and Operations Risk guidelines. Questions are answered from the source documents rather than from model memory: relevant passages are retrieved from a FAISS vector index and passed to a locally hosted LLM, which generates a grounded, bullet-pointed answer.

Built with LangChain, FAISS, Ollama, and Streamlit.

---

## System Architecture

<p align="center">
  <img src="System_Arc.png" alt="System architecture" width="500" />
</p>

<p align="center">
  <img src="RBI_Risk_Chatbot.svg" alt="Retrieval and generation flow" width="500" />
</p>

The pipeline has four stages:

1. **Ingestion** — RBI guideline documents are loaded and split into overlapping chunks.
2. **Indexing** — Chunks are embedded with `<EMBEDDING_MODEL>` and stored in a local FAISS index.
3. **Retrieval** — An incoming question is embedded and matched against the index to pull the top-k most similar chunks.
4. **Generation** — The retrieved chunks are supplied as context to `<OLLAMA_MODEL>` via Ollama, which produces the answer.

---

## Why retrieval rather than a fine-tuned or general-purpose model

Regulatory guidance is long, frequently revised, and only useful when tied back to the text it came from. Retrieval keeps answers anchored to the current source documents, and makes it possible to update the corpus without retraining anything.

---

## Project Structure

```
.
├── frontend.py            # Streamlit interface
├── chatbot_backend.py     # get_answer() — retrieval + generation pipeline
├── RAG-Project.ipynb      # Ingestion, chunking, and index construction
├── requirements.txt       # Python dependencies
└── README.md
```

---

## Setup

**1. Clone and enter the repository**

```bash
git clone https://github.com/pkarthikeya1/<REPO_NAME>.git
cd <REPO_NAME>
```

**2. Create a virtual environment** (Python 3.9+)

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Start Ollama**

The backend expects an Ollama server at `127.0.0.1:11434`. Update the base URL in `chatbot_backend.py` if yours differs.

```bash
ollama serve
ollama pull <OLLAMA_MODEL>
```

**5. Build the vector index**

The FAISS index is read from a local directory named `financial_operations_risk_guidelines`. If it isn't present, run the ingestion cells in `RAG-Project.ipynb` to build it from the source documents.

---

## Running the chatbot

```bash
streamlit run frontend.py
```

Enter a question, click **Get Answer**, and the system retrieves the relevant guideline passages and returns an answer in bullet points.

---

## Design notes

**Chunking.** Retrieval quality is bounded by how the source documents are split. Chunks that are too small lose the surrounding clause context; chunks that are too large dilute the embedding and crowd the model's context window. The current implementation uses character-based splitting with configurable size and overlap.

**Retrieval depth.** The number of chunks passed to the model (`k`) trades recall against context noise — a higher `k` is more likely to contain the correct passage but gives the model more irrelevant text to reason around.

---

## Roadmap

Work in progress, in priority order:

- **Evaluation harness** — a labelled set of benchmark questions paired with their correct source clauses, scored on Recall@k and MRR, so retrieval changes can be measured rather than eyeballed.
- **Source citations** — return the originating section number and document alongside each answer, so responses can be traced back to the guideline text.
- **Structure-aware chunking** — split on the numbered clause hierarchy of RBI master directions instead of on character counts, carrying section identifiers as chunk metadata.
- **Hybrid retrieval** — combine lexical (BM25) and dense retrieval, since regulatory text depends heavily on exact terminology and circular references.
- **Standalone ingestion script** — extract index construction from the notebook into a reproducible CLI entry point.

---

## License

MIT — see [LICENSE](LICENSE).
