from fastapi import APIRouter, HTTPException, Depends
from models.practicetarget import PracticeTarget
from managers.practiceTargetManager import PracticeTargetManager
from redisClient import get_redis_client

router = APIRouter()


@router.get("/practice-target", response_model=PracticeTarget)
async def get_practice_target(redis_client = Depends(get_redis_client)):
    practice_target_manager = PracticeTargetManager(redis_client)
    practice_target = practice_target_manager.get_practice_target()
    if not practice_target:
        raise HTTPException(status_code=404, detail="Practice targets not found")
    return practice_target