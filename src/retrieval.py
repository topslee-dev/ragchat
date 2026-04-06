from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

EMBEDDING_MODEL = "jhgan/ko-sroberta-multitask"


def get_embedding_model():
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)


def load_vectorstore(persist_directory="data/chroma_db"):
    embedding_model = get_embedding_model()
    vectorstore = Chroma(
        persist_directory=persist_directory, embedding_function=embedding_model
    )
    return vectorstore


def retrieve_documents(query, vectorstore, k=3):
    results = vectorstore.similarity_search(query, k=k)
    return results


if __name__ == "__main__":
    print("Loading vector store...")
    vectorstore = load_vectorstore()
    print(f"Total documents: {vectorstore._collection.count()}")

    query = "전자금융거래란 무엇인가?"
    print(f"\nQuery: {query}")

    results = retrieve_documents(query, vectorstore, k=3)

    print(f"\n=== Top 3 Results ===")
    for i, doc in enumerate(results):
        print(f"\n--- Result {i + 1} ---")
        print(doc.page_content[:300])
        print(f"Metadata: {doc.metadata}")
