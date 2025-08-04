from dotenv import load_dotenv
from pathlib import Path
import os


# 找到專案根目錄的 .env 路徑
##env_path = Path(__file__).resolve().parent.parent / ".env"
env_path = Path(__file__).resolve().parent / ".env"

load_dotenv(dotenv_path=env_path)
# load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))


# config.py
from fastapi.middleware.cors import CORSMiddleware

def setup_cors(app):
    origins = [
        "http://localhost",
        "http://localhost:8080",
        "http://127.0.0.1:8080",
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
