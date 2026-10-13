from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class ChatRequest(BaseModel):
    message: str
    context_type: Optional[str] = "market"  # "market" or "product"
    product_id: Optional[str] = None
    active_niche: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    reply: str
    grounded_evidence: List[str]
    suggested_actions: List[str]
    mode: str  # "gemini_ai" or "deterministic_analyst"
