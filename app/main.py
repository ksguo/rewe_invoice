from fastapi import FastAPI
from app.ocr_service.router import router as ocr_router
from app.file_management.router import router as file_management_router
from app.user_management.router import router as user_management_router
from app.ai_service.router import router as ai_service_router

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


# api router for user_management
app.include_router(user_management_router)

# api router for file management
app.include_router(file_management_router)

# api router for ocr_service
app.include_router(ocr_router)

# api router for ai_service
app.include_router(ai_service_router)
