from fastapi import APIRouter
from db.WorkListJson import WorkList
#python導入模塊時，是吃絕對路徑。但是吃檔案還是相對的，[.]就是[/]的意思


router = APIRouter (
    prefix='/WorkList',
    tag=['WorkList']
)

# prefix的功用是創建路徑，好比prefix='/WorkList'代表https:.../WorkList

@router.get('/')
def get_all_Worklist():
    return WorkList
# 當我導入https:.../WorkList時，系統會觸發整個列表的傳回

