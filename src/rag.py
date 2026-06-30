import uuid

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


class RAGPipeline:

    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        self.collection_name = None
        self.vectorstore = None


    def process_pdf(self, pdf_path):

        # Load PDF
        loader = PyPDFLoader(pdf_path)
        docs = loader.load()

        # Split into chunks
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

        chunks = splitter.split_documents(docs)

        # Create unique collection
        self.collection_name = f"quiz_{uuid.uuid4().hex}"

        # Create Chroma collection
        self.vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            collection_name=self.collection_name,
            persist_directory="chroma_db"
        )

        # Return only collection name
        return self.collection_name

    def load_collection(self, collection_name):

        self.vectorstore = Chroma(
            collection_name=collection_name,
            embedding_function=self.embeddings,
            persist_directory="chroma_db"
        )

        return self.vectorstore

    def get_retriever(self, collection_name):

        db = self.load_collection(collection_name)
        return db.as_retriever(search_kwargs={"k": 5})

    def delete_collection(self):
        if self.vectorstore:
            self.vectorstore.delete_collection()