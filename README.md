# RBI Financial & Operations Risk Guidelines Chatbot

This project implements a **Retrieval-Augmented Generation (RAG)** chatbot that answers questions related to the Reserve Bank of India (RBI) Financial and Operations Risk Guidelines. The system uses a FAISS vector store to retrieve context from ingested documents and leverages an Ollama-backed language model (via LangChain) to generate concise, bullet-pointed responses. A Streamlit frontend provides a user-friendly web interface.


## Features

- **Retrieval-Augmented Generation (RAG):**  
  Combines document retrieval (via FAISS) with language generation for accurate, context-based responses.

- **Customizable Document Chunking:**  
  Supports tuning chunk sizes and overlaps to best capture context from financial guidelines.

- **Streamlit Frontend:**  
  An easy-to-use web interface for querying the chatbot.

- **Modular Design:**  
  The core QA logic is encapsulated in a `get_answer` function (in a separate module), which is imported into the Streamlit app.

## Project Structure

```
.
├── frontend.py             # Streamlit frontend for the chatbot
├── chatbot_backend.py      # Contains the get_answer() function and RAG pipeline logic
├── RAG-Project.ipynb   
├── README.md              # This file
└── requirements.txt   # Python dependencies
```

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/rbi-risk-chatbot.git
   cd rbi-risk-chatbot
   ```

2. **Create a Virtual Environment (Recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate      # On Windows: venv\Scripts\activate
   ```

3. **Install the Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

   > **Note:** Ensure you have Python 3.7 or higher installed.

4. **Additional Setup:**
   - **Ollama Server:** Make sure your Ollama server is running at `127.0.0.1:11434` (or update the base URL in the code accordingly).
   - **Vector Store:** The FAISS vector store is loaded from a local directory named `financial_operations_risk_guidelines`. Ensure this database exists or follow your ingestion pipeline to create it.

## Usage

### Running the Chatbot (Streamlit Frontend)

To start the chatbot interface, run:

```bash
streamlit run frontend.py
```

This will launch the Streamlit app in your browser. You can enter your question in the text input field, and upon clicking "Get Answer," the chatbot will retrieve the relevant context and display an answer in bullet points.

### Tuning the Document Chunking Size

The quality of the retrieved context depends on how your documents are split into chunks. You can experiment with different chunk sizes and overlaps using a script similar to the example below:

```python
# chunk_tuning.py

from langchain.text_splitter import CharacterTextSplitter

# Sample document (replace with your actual document content)
document_text = """
The Reserve Bank of India (RBI) has established comprehensive financial and operations risk guidelines to ensure the stability of the financial system.
These guidelines cover topics including risk management practices, capital adequacy, stress testing, and contingency planning.
They are designed to help banks identify, measure, monitor, and control their risks.
...
"""

# Experiment with different chunk sizes and overlaps
chunk_sizes = [100, 200, 300]
chunk_overlap = 50  # Adjust overlap as needed

for chunk_size in chunk_sizes:
    print(f"\n{'='*40}\nUsing chunk size: {chunk_size} with overlap: {chunk_overlap}\n{'='*40}")
    text_splitter = CharacterTextSplitter(
        separator="\n\n",
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    
    chunks = text_splitter.split_text(document_text)
    
    print(f"Number of chunks: {len(chunks)}\n")
    for i, chunk in enumerate(chunks):
        print(f"Chunk {i+1}:\n{chunk}\n{'-'*40}")
```

Run the script with:

```bash
python chunk_tuning.py
```

Review the output to determine which settings best preserve context without exceeding the language model’s token limits.

## Evaluation

To evaluate the chatbot:
- **Automated Metrics:**  
  Use retrieval metrics (e.g., Recall@k) if you have a set of benchmark questions with known relevant context.
  
- **Human Evaluation:**  
  Have domain experts review a sample of responses for correctness, clarity, and relevance.

- **Performance Testing:**  
  Monitor response latency and scalability under load.

## Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes and push the branch.
4. Open a Pull Request with a description of your changes.

## License

This project is licensed under the [MIT License](LICENSE).
