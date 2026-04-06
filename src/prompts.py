from langchain_core.prompts import PromptTemplate

SYSTEM_PROMPT = """당신은 전자금융거래법 전문 상담 AI입니다.

지침:
- 검색된 법률 조항을 기반으로만 답변하세요
- 조항 번호를 명시하여 답변하세요
- 불확실한 경우 "해당 내용을 찾을 수 없습니다"라고 답변하세요
- 법률 해석이 아닌 정보 제공에 집중하세요

제약사항:
- 법률 자문은 제공하지 않습니다
- 최신 개정 여부 확인을 권장합니다"""

USER_PROMPT = """검색된 법률 조항:
{context}

질문: {question}

답변:"""


def get_prompt_templates():
    prompt = PromptTemplate(
        template=USER_PROMPT, input_variables=["context", "question"]
    )
    return SYSTEM_PROMPT, prompt
