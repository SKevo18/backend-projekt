import fastapi as fa
from fastapi.middleware.cors import CORSMiddleware
from router import ALL_CONTROLLERS

API = fa.FastAPI(title="API", version="0.1.0", root_path="/api")

API.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], # TODO: z env
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for router in ALL_CONTROLLERS:
    API.include_router(router)


@API.get("/")
async def root():
    return {"message": "API is working"}
