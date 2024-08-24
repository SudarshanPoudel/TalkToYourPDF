from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from typing import List, BinaryIO, Union
import chromadb

# Function to read pdf
def read_pdf(pdf_file: Union[BinaryIO, str]) -> str:
    loader = PyPDFLoader(pdf_file)
    documents = loader.load()
    text = "\n".join(doc.page_content for doc in documents)
    return text


# Function to convert content to chunks
def content_to_chunks(content: str, chunk_size: int = 2000, overlap: int = 200) -> List[str]:
    separators = ['\n\n', '.', '?', '!']

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        separators=separators
    )
    chunks = text_splitter.split_text(content)
    return chunks


# Default configurations
DEFAULT_MODEL_NAME = 'all-MiniLM-L6-v2'
DEFAULT_COLLECTION_NAME = 'all_notes'

def initialize_chroma_client() -> chromadb.HttpClient:
    return chromadb.HttpClient()



# Function to store text chunks in Chroma database, replacing any existing data
def store_chunks(text_chunks: List[str]):
    client = initialize_chroma_client()
    
    model = SentenceTransformer(DEFAULT_MODEL_NAME)
    
    embeddings = model.encode(text_chunks)
    collection = client.get_or_create_collection(name=DEFAULT_COLLECTION_NAME)

    collection.add(
        ids=['id' + str(i) for i in range(len(text_chunks))],
        embeddings=embeddings,
        metadatas=[{'content': c} for c in text_chunks]
    )


# Function that returns top_n chunks similar to query
def query_chunks(query: str, top_n: int = 3) -> List[str]:
    client = initialize_chroma_client()
    model = SentenceTransformer(DEFAULT_MODEL_NAME)
    
    query_embedding = model.encode([query])[0]
    query_embedding_list = query_embedding.tolist()  # Convert to list

    collection = client.get_collection(name=DEFAULT_COLLECTION_NAME)
    results = collection.query(query_embedding_list, n_results=top_n)
    
    content = []
    for data in results['metadatas'][0]:
        content.append(data['content'])

    return content