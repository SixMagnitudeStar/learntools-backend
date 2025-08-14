from fastapi import APIRouter, Query
from chains.article_chain import generate_essay  # 新版函式

router = APIRouter()

@router.get("/essay")
async def essay_endpoint(
    topic: str = Query(..., description="Essay topic"),
    word_limit: int = Query(500, ge=100, le=1000, description="Max words in essay")
):
    # 呼叫新版函式
    essay = await generate_essay(topic=topic, word_limit=word_limit)
    return {
        "topic": topic,
        "essay": essay.strip()
    }