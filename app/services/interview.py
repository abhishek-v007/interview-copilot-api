from app.schemas.interview import InterviewAnswerResponse
from app.services.llm.service import LLMService

_PROMPT_PREAMBLE = (
    "You are an interview copilot. Given an interview question, produce a "
    "concise, high-quality spoken-style answer the candidate can deliver. "
    "Be specific, structured, and avoid filler."
)

_JSON_INSTRUCTIONS = (
    "Respond with JSON only, with no markdown fences. Schema:\n"
    '{"answer": "spoken-style answer", "key_points": ["point 1", "point 2"]}'
)


class InterviewService:
    """Orchestrates question → prompt → LLM service → answer."""

    def __init__(self, llm_service: LLMService) -> None:
        self._llm_service = llm_service

    async def answer(self, question: str, role: str | None) -> InterviewAnswerResponse:
        prompt = self._build_prompt(question, role)
        result = await self._llm_service.generate(prompt)
        return InterviewAnswerResponse(answer=result.answer, key_points=result.key_points)

    @staticmethod
    def _build_prompt(question: str, role: str | None) -> str:
        sections = [_PROMPT_PREAMBLE, "", f"Question:\n{question}"]
        if role:
            sections.extend(["", f"Target role:\n{role}"])
        sections.extend(["", _JSON_INSTRUCTIONS])
        return "\n".join(sections)
