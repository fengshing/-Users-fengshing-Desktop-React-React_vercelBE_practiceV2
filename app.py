# 把舊的db載入改成router在跑
import uvicorn
from fastapi import FastAPI
# from api.WorkList import WorkList
from router import WorkList
from fastapi.middleware.cors import CORSMiddleware

# 創建 FastAPI 應用實例
app = FastAPI()

# 定義允許訪問您應用的來源列表，有本地測試用的網址，以及來自所有來源的請求
origins = [
    'http://localhost:5173',
    "*"
]

# 應用FastApi的套件，處理CORS議題的運轉機制
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # 允許來源列表中的來源
    allow_credentials=True,
    allow_methods=["*"], # 允許所有常用的 HTTP 方法
    allow_headers=['*'] # 允許所有標準的 HTTP 頭部
)


# 用router的呼叫，使雲端上吃得到資料
app.include_router(WorkList.router)
# 這行代碼將 WorkList 路由器添加到的 FastAPI 應用中。這意味着 WorkList 中定義的所有路徑（或端點）現在都是 FastAPI 應用的一部分。

#方便監聽而使用




# 本地運轉監看用，用來本地app.py能顯示WorkList的內容
@app.get("/")
def read_root():
    return {"message": "Welcome to student WorkList API!"}

# 本地運轉監看用，在"本地網址/WorkList"打印資料
@app.get("/WorkList")
def root():
    return WorkList

# 運行伺服器
if __name__ == "__main__":
    uvicorn.run("app:app", port=5000, reload=True)
# if __name__ == "__main__" 這行是一個標準的 Python 條件語句，用來檢查該模組（文件）是否作為主要程序運行。
# reload=True 是一個開發方便的選項，它會讓服務器在檢測到代碼變動時自動重啟。這對於開發過程中的即時反饋非常有用。這也造就了後台的實時更新
# uvicorn那段app:app就是說，去運轉當前檔名為app裡，應用實例又剛好叫做app的地方。具體來說就是運轉剛剛定義好的fastapi。

