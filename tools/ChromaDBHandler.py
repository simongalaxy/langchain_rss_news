from langchain_chroma import Chroma
# from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings

from pprint import pprint

class ChromaDBHandler:
    def __init__(self, persist_directory: str, embedding_model: str):
        """
        Setup ChromaDB with Ollama embeddings and persistence.
        """
        self.persist_directory = persist_directory

        # # Ollama embeddings
        # self.embeddings = OllamaEmbeddings(model=ollama_embedding_model)

        # Embeddings 
        self.embeddings = HuggingFaceEmbeddings(model_name=embedding_model)

        # Initialize Chroma vector store
        self.vectorstore = Chroma(
            collection_name="rss_news",
            embedding_function=self.embeddings,
            persist_directory=self.persist_directory,
        )

        # Text splitter for long docs
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )

    # generate documents.
    def add_feeds_to_chromadb(self, feeds: list[dict]) -> None:
        
        # prepare documents.
        documents = []
        ids = []
        
        # existing ids.
        existing = self.vectorstore.get(include=["metadatas"])
        # print(existing["ids"])
        
        for feed in feeds:
            # to avoid added duplicated feeds to chromadb.
            
            if feed["Id"] not in existing["ids"]:
                document = Document(
                    page_content=feed["Title"] + " " + feed["Content"],
                    metadata=feed["Metadata"],
                    id=feed["Id"]
                )
                ids.append(feed["Id"])
                documents.append(document)
        
        print(f"Total no. of new feeds: {len(documents)}")
        
        # load the documents to the ChromaDB.
        if documents:
            self.vectorstore.add_documents(
                documents=documents,
                ids=ids,
            )
            print(f"Total {len(documents)} added to ChromaDB successfully.\n")
        
        return
    
    # set up the retriever for query chromadb.
    def retrieve_documents_from_chromadb(self, review_nos: int):
        
        retreiever = self.vectorstore.as_retriever(
            search_kwargs={
                "k": review_nos,
            }
        )
        
        return retreiever