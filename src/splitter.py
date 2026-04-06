from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_and_split(file_path, chunk_size=500, overlap=50):
    loader = PyPDFLoader(file_path)
    docs = loader.load()

    # 법률 문서 최적화: 재귀적 분할로 문단 구조 보존
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        separators=["\n\n", "\n", " ", ""]  # 문단 → 줄 → 단어 → 글자
    )
    chunks = splitter.split_documents(docs)

    print(f"Loaded {len(docs)} pages")
    print(f"Created {len(chunks)} chunks")

    for i, chunk in enumerate(chunks[:3]):
        print(f"--- Chunk {i + 1} ---")
        print(chunk.page_content[:200])
        print(f"Metadata: {chunk.metadata}")

    return chunks


if __name__ == "__main__":
    chunks = load_and_split("data/raw/전자금융거래법(법률)(제21205호)(20261217).pdf")
