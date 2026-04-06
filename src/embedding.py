from langchain_huggingface import HuggingFaceEmbeddings

EMBEDDING_MODEL = "jhgan/ko-sroberta-multitask"


def get_embedding_model():
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)


if __name__ == "__main__":
    import sys

    model = get_embedding_model()
    test_vector = model.embed_query("테스트 문장")
    print(f"Embedding dimension: {len(test_vector)}")
    print(f"Model loaded successfully")
