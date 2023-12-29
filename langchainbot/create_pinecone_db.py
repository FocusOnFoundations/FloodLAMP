import os
import pinecone
import sys

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Pinecone
from langchain.document_loaders import ObsidianLoader

# Set OpenAI API key
# os.environ["OPENAI_API_KEY"] = 

# Specify Pinecone API key and environment
# PINECONE_API_KEY = 
PINECONE_ENV = "gcp-starter"

# Set local path to Obsidian vault
obsidian_path = "data/training_new17_md"

# Set Pinecone database name
index_name = "floodlamp"

# Initialize Pinecone
pinecone.init(
    api_key=PINECONE_API_KEY,  
    environment=PINECONE_ENV,  
)

if index_name in pinecone.list_indexes():
    print(f"ERROR: Index {index_name} already exists. If you wish to overwrite it, please delete it first via the Pinecone online console.")
    sys.exit(1)

if not os.path.exists(obsidian_path):
    print(f"ERROR: Path does not exist: {obsidian_path}. Please enter a valid path and run again.")
    sys.exit(1)
    
# Load documents
loader = ObsidianLoader(obsidian_path)
docs = loader.load()
print(f"SUCCESS: Loaded {len(docs)} documents from {obsidian_path}")

# Split documents
target_chunk_size = 1000
text_splitter = RecursiveCharacterTextSplitter(chunk_size=target_chunk_size, chunk_overlap=0)
all_splits = text_splitter.split_documents(docs)
print(f"SUCCESS: Split {len(docs)} documents into {len(all_splits)} splits with a target chunk size of {target_chunk_size}")
    
print(f"PROCESS: Creating index {index_name}")
pinecone.create_index(name=index_name, metric="cosine", dimension=1536) # dimension for OpenAI embeddings

print("PROCESS: Populating vector store in Pinecone cloud database.")
Pinecone.from_documents(documents=all_splits, embedding=OpenAIEmbeddings(), index_name=index_name)

print(f"SUCCESS: Populated and saved vector store in Pinecone cloud database.")
