"""Assistant router for Ask AVA chat and status."""
from __future__ import annotations

import uuid
from typing import Dict, Any
from fastapi import APIRouter, Depends, Header, HTTPException, Request

from ava.config import get_settings
from ava.storage.base import Repository
from api.assistant.gemini_client import ask_ava
from api.deps import get_niche_context, get_repo
from api.schemas import AskQuestionRequest, AskQuestionResponse, AssistantStatusResponse

router = APIRouter(prefix="/assistant", tags=["Assistant"])


@router.get("/status", response_model=AssistantStatusResponse)
def get_assistant_status() -> AssistantStatusResponse:
    settings = get_settings()
    has_key = bool(settings.GEMINI_API_KEY)
    mode = settings.ASK_AVA_MODE.lower()
    if not has_key and mode == "gemini":
        mode = "demo"

    return AssistantStatusResponse(
        mode=mode,
        gemini_available=has_key,
        model=settings.GEMINI_MODEL,
        sample_questions=[
            "What is the median price for Kurtas?",
            "Which price band is most populated?",
            "What are the top market opportunities?",
            "What share of listings offer sizes 3XL and larger?",
            "Which colours and materials have the highest review counts?",
        ],
    )


@router.post("/ask", response_model=AskQuestionResponse)
async def ask_question(
    payload: AskQuestionRequest,
    repo: Repository = Depends(get_repo),
) -> AskQuestionResponse:
    # Resolve niche
    niche_filter = None
    niche_name = "All Listings"
    if payload.niche_id and payload.niche_id not in ("all", "default", "none"):
        n_record = repo.get_niche_by_id(payload.niche_id)
        if n_record:
            niche_filter = n_record.get("filters")
            niche_name = n_record.get("name", "Saved Niche")

    session_id = payload.session_id or f"sess_{uuid.uuid4().hex[:8]}"

    response = await ask_ava(
        question=payload.question,
        repo=repo,
        niche_filter=niche_filter,
        niche_name=niche_name,
        category="Women's Kurtas & Kurtis",
        session_id=session_id,
    )

    # Log query to chat_logs (no personal data stored)
    try:
        repo.save_chat_log({
            "id": f"log_{uuid.uuid4().hex[:8]}",
            "session_id": session_id,
            "niche_id": payload.niche_id,
            "question": payload.question,
            "answer": response.answer,
            "tools_used": [e.source_tool for e in response.evidence],
            "mode": response.mode,
        })
    except Exception:
        pass

    return response
