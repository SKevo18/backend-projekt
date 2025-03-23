import fastapi as fa
from fastapi.middleware.cors import CORSMiddleware
from router.page_crud import PAGE_CRUD_ROUTER
from router import ALL_ROUTERS
from dotenv import load_dotenv
import os

load_dotenv()

API = fa.FastAPI(title="API", version="0.1.0")

API.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for router in ALL_ROUTERS:
    API.include_router(router)

# uvicorn main:API --reload --env-file .env
