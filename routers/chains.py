from fastapi import APIRouter, Query
from chains.article_chain import essay_chain

router = APIRouter()

@router.get("/essay")
async def generate_essay(
    topic: str = Query(..., description="Essay topic"),
    word_limit: int = Query(500, ge=100, le=1000, description="Max words in essay")
):
    essay = essay_chain.run(topic=topic, word_limit=word_limit)
    return {
        "topic": topic,
        "essay": essay.strip()
    }