from typing import Optional

from pydantic import BaseModel

class SimilarityRequest(BaseModel):
    name: str
    n_similar_skills: Optional[int] = 5
    dataset: Optional[str]