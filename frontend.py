import streamlit as st
from chatbot_backend import get_answer  # Make sure this module is in your PYTHONPATH or the same directory

def main():
    st.title("Financial and Operational Risk Guidelines QA")
    st.write("Ask any question about RBI Financial & Operations Risk Guidelines.")
    
    question = st.text_input("Enter your question:")
    
    if st.button("Get Answer"):
        if not question:
            st.error("Please enter a question.")
        else:
            with st.spinner("Processing your question..."):
                answer = get_answer(question)
            st.subheader("Answer:")
            st.write(answer)

if __name__ == "__main__":
    main()
