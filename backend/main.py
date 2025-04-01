import fastapi as fa
from fastapi.middleware.cors import CORSMiddleware
from router import ALL_ROUTERS
from router.email import EMAIL_ROUTER

from fastapi.middleware.cors import CORSMiddleware
from router import authentication


API = fa.FastAPI(title="API", version="0.1.0", root_path="/api")
API.include_router(EMAIL_ROUTER)

API.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for router in ALL_ROUTERS:
    API.include_router(router)


origins = [
    "http://localhost:5173",
]

API.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # adress frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@API.get("/")
async def root():
    return {"message": "API is working"}

API.include_router(authentication.AUTH_ROUTER)
