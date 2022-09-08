from os import name
from typing import Optional
from fastapi import APIRouter
import logging

from .models import SimilarityRequest
from .errors import UnicornException

router = APIRouter(prefix="/fast-api")


@router.get("/{skill}")
async def get_skill_similarity(skill: str, limit: Optional[int] = 5, dataset: Optional[str] = None):

    logger = logging.getLogger("app")
    logger.info("INFO")
    logger.error("ERROR")

    return "hey"

@router.post("")
async def post_skill_similarity(req: SimilarityRequest):
    if req.name == "unicorn":
        raise UnicornException(name = req.name)

    print(req.name)
    print(req.n_similar_skills)
    return "hey"
