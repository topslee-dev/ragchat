from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

EMBEDDING_MODEL = "jhgan/ko-sroberta-multitask"


def load_pdf(file_path):
    loader = PyPDFLoader(file_path)
    return loader.load()


def split_documents(documents, chunk_size=500, overlap=50):
    # 법률 문서 최적화: 재귀적 분할로 문단 구조 보존
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        separators=["\n\n", "\n", " ", ""]  # 문단 → 줄 → 단어 → 글자
    )
    return splitter.split_documents(documents)


def get_embedding_model():
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)


def create_vectorstore(file_path, persist_directory="data/chroma_db"):
    print("Loading documents...")
    docs = load_pdf(file_path)
    print(f"Loaded {len(docs)} pages")

    print("Splitting documents...")
    chunks = split_documents(docs)
    print(f"Created {len(chunks)} chunks")

    print("Loading embedding model...")
    embedding_model = get_embedding_model()

    print("Creating vector store...")
    vectorstore = Chroma.from_documents(
        documents=chunks, embedding=embedding_model, persist_directory=persist_directory
    )

    print(f"Vector store created with {vectorstore._collection.count()} documents")
    return vectorstore


if __name__ == "__main__":
    create_vectorstore("data/raw/전자금융거래법(법률)(제21205호)(20261217).pdf")
