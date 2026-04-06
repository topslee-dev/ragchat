from src.chain import create_qa_chain, ask_question


def main():
    print("=" * 60)
    print("전자금융거래법 RAG 챗봇")
    print("=" * 60)
    print("\nRAG 체인 로딩 중...")

    chain = create_qa_chain()

    print("\n" + "=" * 60)
    print("RAG bots 준비 완료!")
    print("=" * 60)
    print("종료하려면 'quit'를 입력하세요.\n")

    while True:
        query = input("질문: ")
        if query.lower() == "quit":
            print("감사합니다. 종료합니다.")
            break

        if not query.strip():
            continue

        try:
            answer, elapsed = ask_question(chain, query)
            print(f"\n답변: {answer}")
            print(f"(응답 시간: {elapsed:.2f}초)\n")
        except Exception as e:
            print(f"\n오류가 발생했습니다: {e}\n")


if __name__ == "__main__":
    main()
