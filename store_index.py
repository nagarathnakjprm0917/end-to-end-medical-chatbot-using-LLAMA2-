...
from src.helper import load_pdf, text_split, download_hugging_face_embeddings
import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from langchain_community.embeddings import HuggingFaceEmbeddings


load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

# Create Pinecone client
pc = Pinecone(api_key=PINECONE_API_KEY)

index_name = "medical-chatbot"

# Create index only if it doesn't already exist
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=384,          # all-MiniLM-L6-v2 embedding dimension
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )

# Load and split documents
extracted_data = load_pdf("data/")
text_chunks = text_split(extracted_data)

# Load embedding model
embeddings = download_hugging_face_embeddings()

# Store documents in Pinecone
docsearch = PineconeVectorStore.from_texts(
    texts=[t.page_content for t in text_chunks],
    embedding=embeddings,
    index_name=index_name
)

print("Documents uploaded successfully!")