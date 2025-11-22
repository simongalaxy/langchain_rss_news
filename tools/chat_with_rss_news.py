from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

from pprint import pprint

# load chat loop for query to chromadb using ollama
def run_chat_loop(ChromaDB, ollama_model: str) -> None:
    
    # initiate ollama model.
    llm = ChatOllama(
        model=ollama_model,
        disable_streaming=False
    )
    
    retriever = ChromaDB.retrieve_documents_from_chromadb(
        review_nos=10
    )
    
    # Create RAG chain using LangChain v1.0 pattern
    template = """Answer the question based only on the following reviews: {reviews}

    Question: {question}
    """
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | llm
    
    # run chat loop.
    while True:
        question = input("Enter your question (or type 'q' for quit): ")
        if question.lower() == 'q':
            break
        
        try:
            reviews = retriever.invoke(question)
            full_response = chain.invoke(
                {
                    "reviews": reviews,
                    "question": question
                }
            )
            pprint(f"Full response: {full_response.content}\n")
        except Exception as e:
            print(f"Error: {e}\n")
        
        print("-----------------------------------------------------------------\n")
    
    return
