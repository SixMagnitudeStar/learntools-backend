from sqlalchemy import create_engine, text

# 你的連線字串
DATABASE_URL = "sqlite:///./app.db"
engine = create_engine(DATABASE_URL, echo=True)

with engine.connect() as conn:
    # 新增 nickname 欄位
    conn.execute(text("ALTER TABLE users ADD COLUMN nickname VARCHAR(50)"))
    conn.commit()

print("nickname 欄位已新增")