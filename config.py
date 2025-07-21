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