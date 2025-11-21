from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

class LangChainChromaHandler:
    def __init__(self, persist_directory: str, ollama_embedding_model: str):
        """
        Setup ChromaDB with Ollama embeddings and persistence.
        """
        self.persist_directory = persist_directory

        # Ollama embeddings
        self.embeddings = OllamaEmbeddings(model=ollama_embedding_model)

        # Initialize Chroma vector store
        self.vectorstore = Chroma(
            collection_name="documents",
            embedding_function=self.embeddings,
            persist_directory=self.persist_directory,
        )

        # Text splitter for long docs
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )

    def add_text(self, text: str, metadata: dict, doc_id: str):
        """
        Split text, embed, and save with metadata.
        """
        chunks = self.splitter.split_text(text)
        self.vectorstore.add_texts(
            texts=chunks,
            metadatas=[metadata] * len(chunks),
            ids=[f"{doc_id}_{i}" for i in range(len(chunks))]
        )
        print(f"Document '{doc_id}' added with {len(chunks)} chunks.")

    def query(self, query_text: str, n_results: int = 3):
        """
        Retrieve documents relevant to the query.
        """
        results = self.vectorstore.similarity_search(query_text, k=n_results)
        return results
