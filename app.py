# 第一版本：這段代碼是用來創建一個基本的Web服務器，使用 FastAPI 框架，並利用 Uvicorn 作為 ASGI 服務器來運行它。
# 第二迭代：導入WorkList，然後定義路由器做更動
# 第三迭代：導入CORSMiddleware以及相關指令，處理CORS議題
import uvicorn
from fastapi import FastAPI
from WorkList import WorkList
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

# 定義路由處理器，用來讓app.py能顯示WorkList的內容
@app.get("/")
def read_root():
    return WorkList

# 定義路由處理器，讓前端能夠吃到網址：http://127.0.0.1:5000/WorkList
@app.get("/WorkList")
def root():
    return WorkList

# 運行伺服器
if __name__ == "__main__":
    uvicorn.run("app:app", port=5000, reload=True)
# if __name__ == "__main__" 這行是一個標準的 Python 條件語句，用來檢查該模組（文件）是否作為主要程序運行。
# reload=True 是一個開發方便的選項，它會讓服務器在檢測到代碼變動時自動重啟。這對於開發過程中的即時反饋非常有用。這也造就了後台的實時更新
# uvicorn那段app:app就是說，去運轉當前檔名為app裡，應用實例又剛好叫做app的地方。具體來說就是運轉剛剛定義好的fastapi。

