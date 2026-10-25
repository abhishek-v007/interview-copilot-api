from pydantic import BaseModel, Field, field_validator


class InterviewAnswerRequest(BaseModel):
    question: str = Field(..., min_length=1)
    role: str | None = None

    @field_validator("question")
    @classmethod
    def question_must_not_be_blank(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            raise ValueError("question must not be empty")
        return stripped

    @field_validator("role")
    @classmethod
    def empty_role_to_none(cls, value: str | None) -> str | None:
        if value is None:
            return None
        stripped = value.strip()
        return stripped or None


class InterviewAnswerResponse(BaseModel):
    answer: str
    key_points: list[str] = Field(default_factory=list)
