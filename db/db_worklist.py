# 1203新增 用來宣告如何讀寫表格資料的文件
from fastapi import HTTPException, status
from sqlalchemy.orm.session import Session
from .models import DbWorklist
from .OneTableWorkList import WorkList
#ast，一種py的內建模塊。這在處理從資料庫或其他來源獲取的數據時非常有用，特別是當這些數據以非標準格式存儲時。例如，將字符串形式的列表 "[1, 2, 3]" 轉換為真正的列表 [1, 2, 3]。
import ast


# 以下的值與命名邏輯需要參照database.py以及models.py才行。

# 初始化資料庫。從預先定義的資料集合（OneTableWorkList中的WorkList）中讀取資料，並將這些資料寫入到DbWorklist模型對應的資料庫表中。先清空表中現有資料，再添加新資料。
def db_feed(db: Session):
    new_WorkList = [DbWorklist(
        school=worklist["school"],
        semester=worklist["semester"],
        workName=worklist["workName"],
        githubUrl=worklist["githubUrl"],
        websiteUrl=worklist["websiteUrl"],
        pptUrl=worklist["pptUrl"],
        imgUrl=worklist["imgUrl"],
        skill=worklist["skill"],
        name=worklist["name"]
    ) for worklist in WorkList]
    db.query(DbWorklist).delete()
    db.commit()
    db.add_all(new_WorkList)
    db.commit()
    db_items = db.query(DbWorklist).all()
    return db_items

# 創建新的資料庫記錄。根據從外部請求接收到的資料，創建一個新的DbWorklist記錄並將其添加到資料庫中。
def create(db: Session, request):
    new_worklist = DbWorklist(
        school=request.school,
        semester=request.semester,
        workName=request.workName,
        githubUrl=request.githubUrl,
        websiteUrl=request.websiteUrl,
        pptUrl=request.pptUrl,
        imgUrl=request.imgUrl,
        skill=request.skill,
        name=request.name
    )
    db.add(new_worklist)
    db.commit()
    db.refresh(new_worklist)
    return new_worklist

# 從資料庫中檢索所有DbWorklist記錄。如果沒有找到任何記錄，則引發HTTP 404錯誤。
def get_all(db: Session):
    worklist = db.query(DbWorklist).all()
    if not worklist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'worklist not found')
    return worklist

# 從資料庫中讀取特定學期的worklist記錄。如果沒有找到符合指定學期的紀錄，會引發HTTP 404異常，否則返回這些紀錄。
def get_worklist_by_semester(semester: str, db: Session):
    #從資料庫中查詢所有學期等於（==）指定semester值的worklist記錄。
    worklist = db.query(DbWorklist).filter(DbWorklist.semester == semester).all()
    if not worklist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'worklist with semester = {semester} not found')
    return worklist

# 從資料庫中讀取特定學校的worklist記錄。如果沒有找到符合指定學校的紀錄，會引發HTTP 404異常，否則返回這些紀錄。
def get_homework_by_school(school: str, db: Session):
    #從資料庫中查詢所有學校等於（==）指定school值的worklist記錄。
    worklist = db.query(DbWorklist).filter(DbWorklist.school == school).all()
    if not worklist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'worklist with school = {school} not found')
    return worklist

# 優化UX，製作一個先學校後學期的模式
def get_worklist_by_school_and_semester(school: str, semester: str, db: Session):
    worklist = db.query(DbWorklist).filter(DbWorklist.school == school, DbWorklist.semester == semester).all()
    if not worklist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'worklist for school {school} and semester {semester} not found')
    return worklist


# 優化資料空值的處理，還有將資料轉換成列表
def str2List(worklist_records: list):
    for record in worklist_records:
        if record.skill:  # 確保 skill 字段不是空的
            # 將 skill 字串轉換回列表
            record.skill = ast.literal_eval(record.skill)
        if record.name:  # 確保 name 字段不是空的
            # 將 name 字串轉換回列表
            record.name = ast.literal_eval(record.name)

    return worklist_records