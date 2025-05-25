import fastapi as fa
import os
from controllers import ALL_CONTROLLERS
from fastapi.middleware.cors import CORSMiddleware
from utils.relative_redirect import RelativeRedirectMiddleware

API = fa.FastAPI(title="API", version="0.1.0", root_path="/api")

API.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL", "http://localhost:5173")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API.add_middleware(RelativeRedirectMiddleware)

for router in ALL_CONTROLLERS:
    API.include_router(router)
