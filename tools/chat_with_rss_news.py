from langchain_ollama import ChatOllama
# from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import PromptTemplate

from langchain_classic.schema.runnable import RunnableParallel, RunnablePassthrough
from langchain_classic.chains.combine_documents import create_stuff_documents_chain

from pprint import pprint

# load chat loop for query to chromadb using ollama
def run_chat_loop(ChromaDB, ollama_model: str) -> None:
    
    # initiate ollama model.
    llm = ChatOllama(
        model=ollama_model
    )
    
    retriever = ChromaDB.retrieve_documents_from_chromadb(
        review_nos=5
    )
    
    # Create RAG chain using LangChain v1.0 pattern
    # Strict prompt
    prompt_template = """
    Use the following pieces of context to answer the question at the end.
    If you don't know the answer, just say that you don't know, don't try to make up an answer.
    Use three sentences maximum and keep the answer as concise as possible.
    Always say "thanks for asking!" at the end of the answer.

    Context:
    {context}

    Question:
    {question}

    Answer:
    """

    PROMPT = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"]
    )

    # Document chain
    doc_chain = create_stuff_documents_chain(
        llm=llm,
        prompt=PROMPT
    )

    # Build RAG pipeline
    rag_chain = RunnableParallel({
        "context": retriever,
        "question": RunnablePassthrough()
    }) | doc_chain

    # run chat loop.
    while True:
        question = input("Enter your question (or type 'q' for quit): ")
        if question.lower() == 'q':
            break
        
        try:
            full_response = rag_chain.invoke(question)
            pprint(f"Full response for question - {question}:")
            print(full_response)
        except Exception as e:
            print(f"Error: {e}\n")
        
        print("-----------------------------------------------------------------\n")
    
    return
