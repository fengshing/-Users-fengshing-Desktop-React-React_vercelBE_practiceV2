from fastapi import APIRouter
from db.WorkListJson import WorkList
#python導入模塊時，是吃絕對路徑。但是吃檔案還是相對的，[.]就是[/]的意思


router = APIRouter (
    prefix='/ver1127/WorkList',
    tags=['WorkList']
)
# prefix的功用是創建路徑，好比prefix='/WorkList'代表https:.../WorkList

@router.get('/')
def get_all_Worklist():
    return WorkList
# 當我導入https:.../WorkList時，系統會觸發整個列表的傳回

@router.get('/{school}')
def get_WorkList_itsSchool(school: str ="") -> dict:
    #school: str = ""：定義了一個名為 school 的參數，其類型為 str（字符串）。
    #  = "" ：表示如果調用函數時沒有提供 school 的值，則會使用空字符串作為默認值。
    #使用-> list或-> dict這樣的語法來指定函數返回值的類型，這是類型提示（Type Hinting）的一部分。類型提示本身不會改變程式的執行行為，但它們提供了關於函數應該返回什麼類型的額外信息。這可以幫助開發者更好地理解和使用函數，也有助於靜態類型檢查工具檢查程式碼。
    try:
        return WorkList[school]
    except:
        return {}
    # try: 和 except: 是 Python 的錯誤處理機制。school有值時傳回該值，沒有則空值
# EX: /ntue

@router.get('/{school}/{semeter}')
def get_WorkList_itsSemeter(school: str = "", semester: str = "") -> list:
    try:
        return WorkList[school][semester]
    except:
        return {}
# EX: /ntue/111-2
# 補充：@router.get('/school/semeter') EX：/school/semester?school=ntue&semester=111-1


# 以下這段與期中作業的前台設計比較無關，是老師示範裡多新增了一個預覽子頁面（就點擊卡片後先呈現一些細節說明用的作品說明頁面）
@router.get('/semester')
def get_WorkList_by_semester(semester: str = "") -> list:
    """
    return homeworks by semester
    /semester?semester=111-1
    """
    try:
        ntue = WorkList["ntue"][semester]
        ntut = WorkList["ntut"][semester]
        return [*ntue, *ntut]
    except:
        return {}
    #*代表著解包，可以想像把ntue或ntut的學期都攤開來