from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Dict, Any
from database import get_db
from auth import get_current_teacher

router = APIRouter(prefix="/teacher", tags=["教师端 (Teacher)"])

# ==================== Pydantic Models ====================

class ClassInfo(BaseModel):
    class_id: str
    class_name: str

class Statistics(BaseModel):
    avgScore: float
    maxScore: float
    passRate: float

class StudentScore(BaseModel):
    student_id: str
    student_name: str
    total_score: float
    rank: int

class ClassScoreResponse(BaseModel):
    statistics: Statistics
    students: List[StudentScore]

# ==================== API Endpoints ====================

@router.get("/classes", response_model=List[ClassInfo])
async def get_teacher_classes(
    current_user: Dict[str, Any] = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """获取教师所教班级列表"""
    
    # 获取当前教师ID
    teacher_id = current_user["user_id"]
    teacher_name = current_user.get("name", "张老师")
    
    # 模拟数据：根据教师返回其所教的班级
    mock_classes = [
        {"class_id": "class_001", "class_name": "高三(1)班"},
        {"class_id": "class_002", "class_name": "高三(2)班"},
        {"class_id": "class_003", "class_name": "高三(3)班"},
        {"class_id": "class_004", "class_name": "高三(4)班"}
    ]
    
    # 如果是不同的教师，可以返回不同的班级
    if teacher_name == "李老师":
        mock_classes = [
            {"class_id": "class_005", "class_name": "高三(5)班"},
            {"class_id": "class_006", "class_name": "高三(6)班"}
        ]
    
    return [ClassInfo(**class_data) for class_data in mock_classes]

@router.get("/classes/{class_id}/scores", response_model=ClassScoreResponse)
async def get_class_scores(
    class_id: str,
    examId: str = Query(..., description="考试ID"),
    current_user: Dict[str, Any] = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """获取班级成绩单"""
    
    # 获取当前教师ID
    teacher_id = current_user["user_id"]
    
    # 验证教师是否有权限查看该班级
    # 在实际项目中，应该从数据库查询教师与班级的关系
    allowed_classes = ["class_001", "class_002", "class_003", "class_004"]
    if class_id not in allowed_classes:
        raise HTTPException(
            status_code=403,
            detail="您没有权限查看此班级的成绩"
        )
    
    # 模拟班级成绩数据
    mock_class_scores = {
        "class_001": {
            "statistics": {
                "avgScore": 485.2,
                "maxScore": 612.5,
                "passRate": 87.5
            },
            "students": [
                {"student_id": "stu_001", "student_name": "张三", "total_score": 612.5, "rank": 1},
                {"student_id": "stu_002", "student_name": "李四", "total_score": 598.0, "rank": 2},
                {"student_id": "stu_003", "student_name": "王五", "total_score": 585.5, "rank": 3},
                {"student_id": "stu_004", "student_name": "赵六", "total_score": 572.0, "rank": 4},
                {"student_id": "stu_005", "student_name": "钱七", "total_score": 558.5, "rank": 5},
                {"student_id": "stu_006", "student_name": "孙八", "total_score": 545.0, "rank": 6},
                {"student_id": "stu_007", "student_name": "周九", "total_score": 532.5, "rank": 7},
                {"student_id": "stu_008", "student_name": "吴十", "total_score": 520.0, "rank": 8},
                {"student_id": "stu_009", "student_name": "郑十一", "total_score": 507.5, "rank": 9},
                {"student_id": "stu_010", "student_name": "王十二", "total_score": 495.0, "rank": 10},
                {"student_id": "stu_011", "student_name": "李十三", "total_score": 482.5, "rank": 11},
                {"student_id": "stu_012", "student_name": "张十四", "total_score": 470.0, "rank": 12},
                {"student_id": "stu_013", "student_name": "陈十五", "total_score": 457.5, "rank": 13},
                {"student_id": "stu_014", "student_name": "刘十六", "total_score": 445.0, "rank": 14},
                {"student_id": "stu_015", "student_name": "黄十七", "total_score": 432.5, "rank": 15},
                {"student_id": "stu_016", "student_name": "杨十八", "total_score": 420.0, "rank": 16},
                {"student_id": "stu_017", "student_name": "朱十九", "total_score": 407.5, "rank": 17},
                {"student_id": "stu_018", "student_name": "秦二十", "total_score": 395.0, "rank": 18},
                {"student_id": "stu_019", "student_name": "许二一", "total_score": 382.5, "rank": 19},
                {"student_id": "stu_020", "student_name": "何二二", "total_score": 370.0, "rank": 20},
                {"student_id": "stu_021", "student_name": "吕二三", "total_score": 357.5, "rank": 21},
                {"student_id": "stu_022", "student_name": "施二四", "total_score": 345.0, "rank": 22},
                {"student_id": "stu_023", "student_name": "张二五", "total_score": 332.5, "rank": 23},
                {"student_id": "stu_024", "student_name": "孔二六", "total_score": 320.0, "rank": 24},
                {"student_id": "stu_025", "student_name": "曹二七", "total_score": 307.5, "rank": 25},
                {"student_id": "stu_026", "student_name": "严二八", "total_score": 295.0, "rank": 26},
                {"student_id": "stu_027", "student_name": "华二九", "total_score": 282.5, "rank": 27},
                {"student_id": "stu_028", "student_name": "金三十", "total_score": 270.0, "rank": 28},
                {"student_id": "stu_029", "student_name": "魏三一", "total_score": 257.5, "rank": 29},
                {"student_id": "stu_030", "student_name": "陶三二", "total_score": 245.0, "rank": 30},
                {"student_id": "stu_031", "student_name": "姜三三", "total_score": 232.5, "rank": 31},
                {"student_id": "stu_032", "student_name": "戚三四", "total_score": 220.0, "rank": 32},
                {"student_id": "stu_033", "student_name": "谢三五", "total_score": 207.5, "rank": 33},
                {"student_id": "stu_034", "student_name": "邹三六", "total_score": 195.0, "rank": 34},
                {"student_id": "stu_035", "student_name": "喻三七", "total_score": 182.5, "rank": 35},
                {"student_id": "stu_036", "student_name": "柏三八", "total_score": 170.0, "rank": 36},
                {"student_id": "stu_037", "student_name": "水三九", "total_score": 157.5, "rank": 37},
                {"student_id": "stu_038", "student_name": "窦四十", "total_score": 145.0, "rank": 38},
                {"student_id": "stu_039", "student_name": "章四一", "total_score": 132.5, "rank": 39},
                {"student_id": "stu_040", "student_name": "云四二", "total_score": 120.0, "rank": 40}
            ]
        },
        "class_002": {
            "statistics": {
                "avgScore": 468.7,
                "maxScore": 595.0,
                "passRate": 82.1
            },
            "students": [
                {"student_id": "stu_041", "student_name": "苏一", "total_score": 595.0, "rank": 1},
                {"student_id": "stu_042", "student_name": "潘二", "total_score": 580.5, "rank": 2},
                {"student_id": "stu_043", "student_name": "葛三", "total_score": 566.0, "rank": 3},
                {"student_id": "stu_044", "student_name": "奚四", "total_score": 551.5, "rank": 4},
                {"student_id": "stu_045", "student_name": "范五", "total_score": 537.0, "rank": 5},
                {"student_id": "stu_046", "student_name": "彭六", "total_score": 522.5, "rank": 6},
                {"student_id": "stu_047", "student_name": "郎七", "total_score": 508.0, "rank": 7},
                {"student_id": "stu_048", "student_name": "鲁八", "total_score": 493.5, "rank": 8},
                {"student_id": "stu_049", "student_name": "韦九", "total_score": 479.0, "rank": 9},
                {"student_id": "stu_050", "student_name": "昌十", "total_score": 464.5, "rank": 10},
                {"student_id": "stu_051", "student_name": "马十一", "total_score": 450.0, "rank": 11},
                {"student_id": "stu_052", "student_name": "苗十二", "total_score": 435.5, "rank": 12},
                {"student_id": "stu_053", "student_name": "凤十三", "total_score": 421.0, "rank": 13},
                {"student_id": "stu_054", "student_name": "花十四", "total_score": 406.5, "rank": 14},
                {"student_id": "stu_055", "student_name": "方十五", "total_score": 392.0, "rank": 15},
                {"student_id": "stu_056", "student_name": "俞十六", "total_score": 377.5, "rank": 16},
                {"student_id": "stu_057", "student_name": "任十七", "total_score": 363.0, "rank": 17},
                {"student_id": "stu_058", "student_name": "袁十八", "total_score": 348.5, "rank": 18},
                {"student_id": "stu_059", "student_name": "柳十九", "total_score": 334.0, "rank": 19},
                {"student_id": "stu_060", "student_name": "酆二十", "total_score": 319.5, "rank": 20},
                {"student_id": "stu_061", "student_name": "鲍二一", "total_score": 305.0, "rank": 21},
                {"student_id": "stu_062", "student_name": "史二二", "total_score": 290.5, "rank": 22},
                {"student_id": "stu_063", "student_name": "唐二三", "total_score": 276.0, "rank": 23},
                {"student_id": "stu_064", "student_name": "费二四", "total_score": 261.5, "rank": 24},
                {"student_id": "stu_065", "student_name": "廉二五", "total_score": 247.0, "rank": 25},
                {"student_id": "stu_066", "student_name": "岑二六", "total_score": 232.5, "rank": 26},
                {"student_id": "stu_067", "student_name": "薛二七", "total_score": 218.0, "rank": 27},
                {"student_id": "stu_068", "student_name": "雷二八", "total_score": 203.5, "rank": 28},
                {"student_id": "stu_069", "student_name": "贺二九", "total_score": 189.0, "rank": 29},
                {"student_id": "stu_070", "student_name": "倪三十", "total_score": 174.5, "rank": 30},
                {"student_id": "stu_071", "student_name": "汤三一", "total_score": 160.0, "rank": 31},
                {"student_id": "stu_072", "student_name": "滕三二", "total_score": 145.5, "rank": 32},
                {"student_id": "stu_073", "student_name": "殷三三", "total_score": 131.0, "rank": 33},
                {"student_id": "stu_074", "student_name": "罗三四", "total_score": 116.5, "rank": 34},
                {"student_id": "stu_075", "student_name": "毕三五", "total_score": 102.0, "rank": 35},
                {"student_id": "stu_076", "student_name": "郝三六", "total_score": 87.5, "rank": 36},
                {"student_id": "stu_077", "student_name": "邬三七", "total_score": 73.0, "rank": 37},
                {"student_id": "stu_078", "student_name": "安三八", "total_score": 58.5, "rank": 38}
            ]
        }
    }
    
    # 获取对应班级的成绩数据，如果不存在则使用默认数据
    class_data = mock_class_scores.get(class_id, mock_class_scores["class_001"])
    
    # 根据examId可以返回不同考试的成绩（这里简化处理）
    if examId == "exam_002":
        # 对分数稍作调整，模拟不同考试
        adjusted_students = []
        for student in class_data["students"]:
            adjusted_score = max(0, student["total_score"] + ((student["rank"] % 5 - 2) * 10))
            adjusted_students.append(StudentScore(
                student_id=student["student_id"],
                student_name=student["student_name"],
                total_score=adjusted_score,
                rank=student["rank"]
            ))
        
        # 重新排序
        adjusted_students.sort(key=lambda x: x.total_score, reverse=True)
        for i, student in enumerate(adjusted_students, 1):
            student.rank = i
        
        # 重新计算统计数据
        scores = [s.total_score for s in adjusted_students]
        stats = Statistics(
            avgScore=sum(scores) / len(scores),
            maxScore=max(scores),
            passRate=len([s for s in scores if s >= 400]) / len(scores) * 100
        )
        
        return ClassScoreResponse(
            statistics=stats,
            students=adjusted_students
        )
    
    # 返回默认数据
    return ClassScoreResponse(
        statistics=Statistics(**class_data["statistics"]),
        students=[StudentScore(**student) for student in class_data["students"]]
    ) 