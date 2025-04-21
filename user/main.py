from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from .api import router

app = FastAPI()

app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, log_level="info", host="0.0.0.0")