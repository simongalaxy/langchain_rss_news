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
    
    
    # template = """Answer the question based only on the following reviews: {reviews}

    # Question: {question}
    # """
    # prompt = ChatPromptTemplate.from_template(template)
    # chain = prompt | llm
    
    # Create RAG chain using LangChain v1.0 pattern
    # Strict prompt
    prompt_template = """
    You are a retrieval-based assistant.
    Use ONLY the provided context to answer.
    If the context does not contain the answer, say "I don’t know."

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
            # reviews = retriever.invoke(question)
            # full_response = chain.invoke(
            #     {
            #         "reviews": reviews,
            #         "question": question
            #     }
            # )
            full_response = rag_chain.invoke(question)
            # pprint(f"Retrieved Reviews: {reviews}\n")
            pprint(f"Full response for question - {question}:")
            print(full_response)
        except Exception as e:
            print(f"Error: {e}\n")
        
        print("-----------------------------------------------------------------\n")
    
    return
