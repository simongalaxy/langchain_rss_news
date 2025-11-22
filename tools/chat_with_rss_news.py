from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough


# load chat loop for query to chromadb using ollama
def run_chat_loop(persist_directory: str, ollama_model: str, ollama_embedding_model: str) -> None:
    
    # initiate ollama model.
    llm = ChatOllama(
        model=ollama_model,
        disable_streaming=False
    )
    
    embeddings = OllamaEmbeddings(model=ollama_embedding_model)
    
    # initiate chroma vector store.
    vectorstore = Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings
    )
    
    retriever = vectorstore.as_retriever(search_type="mmr", kwargs={})
    
    # Create RAG chain using LangChain v1.0 pattern
    template = """Answer the question based only on the following context:
{context}

Question: {question}
"""
    prompt = ChatPromptTemplate.from_template(template)
    
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)
    
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    # run chat loop.
    while True:
        question = input("Enter your question (or type 'q' for quit): ")
        if question.lower() == 'q':
            break
        
        try:
            full_response = rag_chain.invoke(question)
            print(f"Full response: {full_response}\n")
        except Exception as e:
            print(f"Error: {e}\n")
        
        print("-----------------------------------------------------------------\n")
    
    return
