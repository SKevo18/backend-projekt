import fastapi as fa

from router import ALL_ROUTERS

API = fa.FastAPI()

for router in ALL_ROUTERS:
    API.include_router(router)

if __name__ == "__main__":
    try:
        import uvicorn
    except ImportError:
        print("uvicorn nie je nainštalovaný, skús: `pip install uvicorn` (ak je aktivované .venv)")
        exit(1)

    uvicorn.run(API, host="0.0.0.0", port=8000)
