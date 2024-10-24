from fastapi import FastAPI
from routers import chooseTanks

app = FastAPI()

app.include_router(chooseTanks.router)

# muzes nastavit spolecny prerix pro vsechny routy v routeru
#app.include_router(user_router, prefix="/api/v1")
