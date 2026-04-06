from langchain_community.document_loaders import PyPDFLoader


def load_pdf(file_path):
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    print(f"Loaded {len(docs)} pages")
    for i, doc in enumerate(docs[:3]):
        print(f"--- Page {i + 1} ---")
        print(doc.page_content[:300])
    return docs


if __name__ == "__main__":
    docs = load_pdf("data/raw/전자금융거래법(법률)(제21205호)(20261217).pdf")
