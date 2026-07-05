from pydantic import BaseModel
from typing import Optional

class SolveResponse(BaseModel):
    topic: str
    formula_used: str
    variables: list[dict]
    step_by_step_solution: list[str]
    common_ib_mistakes: list[str]
    practice_questions: list[str]
    graph_base64: Optional[str] = None
