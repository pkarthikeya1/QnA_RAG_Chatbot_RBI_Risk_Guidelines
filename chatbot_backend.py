# -*- coding: utf-8 -*-
"""
Created on Sun Feb 09 12:50:43 2025

@author: Karthikeya Pervela
"""

import os
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore

def get_answer(question: str) -> str:
    # Define the base URL for your Ollama server
    base_url = "127.0.0.1:11434"
    
    # Initialize embeddings using the specified model and base URL
    embeddings = OllamaEmbeddings(model='nomic-embed-text', base_url=base_url)
    
    # Load the vector store (FAISS) from a local database
    db_name = r"financial_operations_risk_guidelines"
    vector_store = FAISS.load_local(db_name, embeddings=embeddings, allow_dangerous_deserialization=True)
    
    # Define the prompt template for the chain
    prompt_template = """
                        You are an assistant for question-answering tasks on Reserve Bank of India Financial and Operations Risk Guidelines.
                        Use the following pieces of retrieved context to answer the question.
                        If you don't know the answer, just say that you don't know.
                        Answer in bullet points. Make sure your answer is relevant to the question and it is answered from context only.
                        Question: {question} 
                        Context: {context} 
                        Answer:"""
    
    prompt = ChatPromptTemplate.from_template(prompt_template)
    
    # Initialize the language model (llama) for chat
    llm = ChatOllama(model="llama3.2:latest", base_url=base_url)
    
    # Function to format retrieved documents into a single context string
    def format_docs(docs):
        return "\n\n".join([doc.page_content for doc in docs])
    
    # Create a retriever from the vector store with a specified number of similar documents to retrieve
    retriever = vector_store.as_retriever(search_type="similarity",
                                          search_kwargs={'k': 5})
    
    # Build the RAG chain. Here, the input dictionary contains two keys:
    # - "context": obtained by passing the input through the retriever and then formatting the docs.
    # - "question": passed through unchanged.
    
    rag_chain = (
        {'context': retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    # Invoke the chain with the question and return the generated response
    response = rag_chain.invoke(question)
    return response

# Example usage:
if __name__ == '__main__':
    question = "how to avoid risk in operations?"
    answer = get_answer(question)
    print(answer)
