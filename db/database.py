# 1203新增，導入sqlalchemy後，直接複製講義的代碼，用來宣告SQLite資料庫形式
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "postgresql://default:wDt8BaKp1fWm@ep-blue-union-72271377.us-east-1.postgres.vercel-storage.com:5432/verceldb"
SQLALCHEMY_DATABASE_URL = "sqlite:///./mydatabase.db"
#這個要用相對路徑，因為engine在app.py內被實作，所以資料庫檔案會建立在與app.py同⼀層的專案根⽬錄位置

# engine = create_engine(SQLALCHEMY_DATABASE_URL)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}  # 這對於 SQLite 是必要的，特別是在多線程環境中(GPT這樣說)
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# , connect_args={"check_same_thread": False}