from langchain_classic.chains import RetrievalQA
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import time

SYSTEM_PROMPT = """당신은 전자금융거래법 전문 상담 AI입니다.

지침:
- 검색된 법률 조항을 기반으로만 답변하세요
- 조항 번호를 명시하여 답변하세요
- 불확실한 경우 "해당 내용을 찾을 수 없습니다"라고 답변하세요
- 법률 해석이 아닌 정보 제공에 집중하세요
- 한국어로 대답하세요

제약사항:
- 법률 자문은 제공하지 않습니다
- 최신 개정 여부 확인을 권장합니다"""

USER_PROMPT = """검색된 법률 조항:
{context}

질문: {question}

답변:"""

LLM_MODEL = "mistral:latest"
EMBEDDING_MODEL = "jhgan/ko-sroberta-multitask"


def get_embedding_model():
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)


def load_vectorstore(persist_directory="data/chroma_db"):
    embedding_model = get_embedding_model()
    vectorstore = Chroma(
        persist_directory=persist_directory, embedding_function=embedding_model
    )
    return vectorstore


def create_qa_chain(vectorstore=None, llm_model=LLM_MODEL):
    if vectorstore is None:
        print("Loading vector store...")
        vectorstore = load_vectorstore()

    print(f"Loading LLM: {llm_model}...")
    llm = ChatOllama(model=llm_model, temperature=0, base_url="http://localhost:11434")

    prompt = PromptTemplate(
        template=USER_PROMPT, input_variables=["context", "question"]
    )

    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
        chain_type_kwargs={"prompt": prompt},
    )

    return chain


def ask_question(chain, query):
    start = time.time()
    result = chain.invoke(query)
    elapsed = time.time() - start
    return result["result"], elapsed


if __name__ == "__main__":
    chain = create_qa_chain()

    test_questions = [
        "전자금융거래란 무엇인가요?",
        "전자지급수단의 종류는 무엇이 있나요?",
        "전자금융업의 등록 요건은?",
        "전자금융거래 위반 시 처벌은?",
    ]

    print("\n" + "=" * 60)
    print("Phase 6: 테스트 및 평가")
    print("=" * 60)

    total_time = 0
    for q in test_questions:
        print(f"\n{'=' * 50}")
        print(f"질문: {q}")
        print(f"{'=' * 50}")
        answer, elapsed = ask_question(chain, q)
        total_time += elapsed
        print(f"답변: {answer}")
        print(f"응답 시간: {elapsed:.2f}초")

    print(f"\n{'=' * 50}")
    print(f"평균 응답 시간: {total_time / len(test_questions):.2f}초")
    print(f"{'=' * 50}")
