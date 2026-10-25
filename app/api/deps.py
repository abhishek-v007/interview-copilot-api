from fastapi import Depends

from app.core.config import Settings, get_settings
from app.services.interview import InterviewService
from app.services.llm import LLMProvider, get_llm_provider
from app.services.llm.service import LLMService


def get_llm(settings: Settings = Depends(get_settings)) -> LLMProvider:
    return get_llm_provider(settings)


def get_llm_service(provider: LLMProvider = Depends(get_llm)) -> LLMService:
    return LLMService(provider)


def get_interview_service(
    llm_service: LLMService = Depends(get_llm_service),
) -> InterviewService:
    return InterviewService(llm_service)
