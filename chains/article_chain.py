##from langchain.chat_models import ChatGoogleGemini
from langchain_google_genai import ChatGoogleGenerativeAI

from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0)

# 建立 LLM，model 名稱依官方定義，並且要設定你自己的 GOOGLE_API_KEY 環境變數
##lm = ChatGoogleGemini(model="gemini-pro", temperature=0)

template = """
Write a high-quality English short essay (no more than {word_limit} words) about the following topic:

Topic: {topic}

Essay:
"""

prompt = PromptTemplate.from_template(template)
essay_chain = LLMChain(llm=llm, prompt=prompt)