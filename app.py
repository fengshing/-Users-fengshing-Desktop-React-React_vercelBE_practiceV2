import uvicorn
from fastapi import FastAPI
# 1202更動 把舊的db載入改成router在跑
# from db.WorkListJson import WorkList
# 1203更動 再把db改成database再跑
from db import models
from db.database import engine
from router import WorkListRouter
# from fastapi.middleware.cors import CORSMiddleware


# 創建 FastAPI 應用實例
app = FastAPI(
    title = "Student WorkList API",
    description = "處理大二學生的網頁作品資料，會包含如校名、學期、技能等等",
    version="1207.Ver2版",
    terms_of_service="http://localhost:5000",
)
# 用router的呼叫，使雲端上吃得到資料
app.include_router(WorkListRouter.router)
# 這行代碼將 WorkListRouter 路由器添加到的 FastAPI 應用中。這意味着 WorkList 中定義的所有路徑（或端點）現在都是 FastAPI 應用的一部分。


# 應用FastApi的套件，處理CORS議題的運轉機制；先放這，目前進入Ver2版後感覺用不到
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins, # 允許來源列表中的來源
#     allow_credentials=True,
#     allow_methods=["*"], # 允許所有常用的 HTTP 方法
#     allow_headers=['*'] # 允許所有標準的 HTTP 頭部
# )


@app.get("/")
def read_root():
    return {"message": "Welcome to student WorkList API! 請在本網址後輸入/docs查閱API資料"}


# 運行伺服器，但由一個
if __name__ == "__main__":
    uvicorn.run("app:app", port=5000, reload=True)
# if __name__ == "__main__" 這行是一個標準的 Python 條件語句，用來檢查該模組（文件）是否作為主要程序運行。
# reload=True 是一個開發方便的選項，它會讓服務器在檢測到代碼變動時自動重啟。這對於開發過程中的即時反饋非常有用。這也造就了後台的實時更新
# uvicorn那段app:app就是說，去運轉當前檔名為app裡，應用實例又剛好叫做app的地方。具體來說就是運轉剛剛定義好的fastapi。


models.Base.metadata.create_all(engine)
# 在資料庫中創建所有由 SQLAlchemy ORM 模型定義的表格。
# 'Base' 包含了所有模型類的元數據，'create_all' 函數使用這些元數據來創建表格。
# 如果表格已經存在於資料庫中，則不會重複創建。