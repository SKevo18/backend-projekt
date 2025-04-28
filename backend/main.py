import fastapi as fa
from fastapi.middleware.cors import CORSMiddleware
from router import ALL_CONTROLLERS, permission_router  # Добавляем импорт permission_router здесь

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


API.include_router(permission_router.PERMISSION_ROUTER)

@API.get("/")
async def root():
    return {"message": "API is working"}