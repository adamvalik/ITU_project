from fastapi import APIRouter

router = APIRouter()

@router.get("/users/")
async def read_users():
    return [{"name": "Alice"}, {"name": "Bob"}]

@router.get("/users/{user_id}")
async def read_user(user_id: int):
    return {"name": "Alice", "user_id": user_id}
