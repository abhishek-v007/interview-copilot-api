import logging
import time

from fastapi import APIRouter, Depends

from app.api.deps import get_interview_service
from app.schemas.interview import InterviewAnswerRequest, InterviewAnswerResponse
from app.services.interview import InterviewService

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/answer", response_model=InterviewAnswerResponse)
async def create_answer(
    payload: InterviewAnswerRequest,
    service: InterviewService = Depends(get_interview_service),
) -> InterviewAnswerResponse:
    started = time.perf_counter()
    logger.info(
        "Generating answer question_length=%s has_role=%s",
        len(payload.question),
        bool(payload.role),
    )
    result = await service.answer(payload.question, payload.role)
    latency_ms = (time.perf_counter() - started) * 1000
    logger.info(
        "Generated answer key_points=%s latency_ms=%.1f",
        len(result.key_points),
        latency_ms,
    )
    return result
