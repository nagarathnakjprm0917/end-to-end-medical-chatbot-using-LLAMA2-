from flask import Flask, render_template, request

from dotenv import load_dotenv
import os

from src.helper import download_hugging_face_embeddings
from src.prompt import *

from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore

from langchain.prompts import PromptTemplate
from langchain_community.llms import CTransformers
from langchain.chains import RetrievalQA

app = Flask(__name__)

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

# Create Pinecone client
pc = Pinecone(api_key=PINECONE_API_KEY)

index_name = "medical-chatbot"

# Embedding model
embeddings = download_hugging_face_embeddings()

# Load existing Pinecone index
docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)

PROMPT = PromptTemplate(
    template=prompt_template,
    input_variables=["context", "question"]
)

chain_type_kwargs = {
    "prompt": PROMPT
}

# Load LLM
llm = CTransformers(
    model="model/llama-2-7b-chat.ggmlv3.q3_K_S.bin",
    model_type="llama",
    config={
        "max_new_tokens": 512,
        "temperature": 0.8
    }
)

qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=docsearch.as_retriever(search_kwargs={"k": 2}),
    return_source_documents=True,
    chain_type_kwargs=chain_type_kwargs
)

@app.route("/")
def index():
    return render_template("chat.html")

@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]

    result = qa.invoke({"query": msg})

    print(result["result"])

    return result["result"]



if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
