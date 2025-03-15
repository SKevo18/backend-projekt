import fastapi as fa
from router import ALL_ROUTERS

API = fa.FastAPI(title="API", version="0.1.0", root_path="/api")

for router in ALL_ROUTERS:
    API.include_router(router)

# uvicorn main:API --reload --env-file .env
