##from langchain.chat_models import ChatGoogleGemini
import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate


##from langchain.chains import LLMChain //舊版，改用PromptValue
from langchain.schema import PromptValue

# 載入 .env 檔的內容到系統環境變數
load_dotenv()

# 從環境變數讀取 API Key
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not set in environment variables")


llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",   # 改成目前可用模型
    temperature=0,
    google_api_key=api_key  # 明確傳入 API Key
    )

# 建立 LLM，model 名稱依官方定義，並且要設定你自己的 GOOGLE_API_KEY 環境變數
##lm = ChatGoogleGemini(model="gemini-pro", temperature=0)

template = """
Write a high-quality English short essay (no more than {word_limit} words) about the following topic:

Topic: {topic}

Essay:
"""

prompt = PromptTemplate.from_template(template)

async def generate_essay(topic: str, word_limit: int = 100) -> str:
    """
    非同步生成短文（新版 LangChain）
    """
    # 先把參數包成 dict
    inputs = {"topic": topic, "word_limit": word_limit}
    # 非同步呼叫管線
    result = await (prompt | llm).ainvoke(inputs)

    # 如果是 AIMessage，取 content
    essay_text = result.content if hasattr(result, "content") else str(result)

    return essay_text.strip()


