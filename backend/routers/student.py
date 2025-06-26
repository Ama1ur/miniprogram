from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import date
from database import get_db
from auth import get_current_student
from models import Exam, Student, Answer, Question, Subject

router = APIRouter(prefix="/student", tags=["学生端 - 核心分析 (Student - Core Analysis)"])

# ==================== Pydantic Models ====================

# 基础模型
class ExamItem(BaseModel):
    exam_id: str
    exam_name: str
    exam_date: date
    total_score: float
    overall_level: str

class ExamListResponse(BaseModel):
    items: List[ExamItem]
    total: int

# Page01 - 考试成绩页
class SubjectScore(BaseModel):
    subject: str
    score: float
    level: str

class Page01ExamScores(BaseModel):
    total_score: float
    overall_level: str
    subject_scores: List[SubjectScore]

# Page02 - 等级位置页
class SubjectComparison(BaseModel):
    subject: str
    score: float
    rank: int
    avg: float
    max: float
    diff: float

class Page02LevelPosition(BaseModel):
    grouping_mode: str
    class_size: int
    grade_size: int
    subject_comparison: List[SubjectComparison]

# Page03 - 成绩PK页
class Page03PKAnalysis(BaseModel):
    rank_percent: float
    rank_index: int
    class_total_students: int

# Page04 - 理想排名页
class IdealScoreRequest(BaseModel):
    subject: str
    ideal_score: float

class IdealScoresRequest(BaseModel):
    ideal_scores: List[IdealScoreRequest]

class SubjectIdealScore(BaseModel):
    subject: str
    current_score: float
    ideal_score: float
    max_score: float

class Page04IdealRanking(BaseModel):
    subjects: List[SubjectIdealScore]
    new_total_score: float
    predicted_rank: int
    rank_change: int
    current_rank: int

# Page05 - 偏科分析页
class RadarData(BaseModel):
    subject: str
    total_win_rate: float
    subject_win_rate: float

class Page05BiasAnalysis(BaseModel):
    radar_data: List[RadarData]
    strength_subjects: List[str]
    weak_subjects: List[str]

# Page06 - 历次趋势页
class TrendData(BaseModel):
    date: str
    class_win_rate: float
    school_win_rate: float

class Page06Trend(BaseModel):
    trend_data: List[TrendData]
    trend_analysis: str

# Page07 - 试题分析页
class QuestionItem(BaseModel):
    id: int
    type: str
    correct_answer: str
    full_score: float
    score: float
    analysis_url: Optional[str] = None

class Page07QuestionAnalysis(BaseModel):
    selected_subject: str
    available_subjects: List[str]
    current_questions: List[QuestionItem]

# Page08 - 失分分析页
class DifficultyAnalysis(BaseModel):
    level: str
    total_score: float
    count: int
    correct: int
    partial: int
    rate: float
    question_numbers: List[str]

class LossQuestions(BaseModel):
    全部丢分: List[str]
    部分丢分: List[str]

class GainPrediction(BaseModel):
    potential_gain_score: float
    rank_improvement: int

class Page08LossAnalysis(BaseModel):
    difficulty_analysis: List[DifficultyAnalysis]
    loss_questions: LossQuestions
    优势得分题: List[str]
    潜力追分题: List[str]
    gain_prediction: GainPrediction

# Page09 - 知识点分析页
class KnowledgePoint(BaseModel):
    name: str
    class_rate: float
    personal_rate: float
    level: str

class Page09KnowledgeAnalysis(BaseModel):
    knowledge_points: List[KnowledgePoint]
    tabs: List[str]

# ==================== API Endpoints ====================

@router.get("/exams", response_model=ExamListResponse)
async def get_student_exams(
    page: int = 1,
    limit: int = 10,
    current_user: Dict[str, Any] = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """获取历史考试列表"""
    
    # 获取当前学生ID
    student_id = current_user["user_id"]
    
    # 计算偏移量
    offset = (page - 1) * limit
    
    # 模拟数据
    mock_exams = [
        {
            "exam_id": "exam_001",
            "exam_name": "2024学年第一学期期末考试",
            "exam_date": "2024-01-15",
            "total_score": 532.0,
            "overall_level": "A3"
        },
        {
            "exam_id": "exam_002", 
            "exam_name": "2024学年第一学期期中考试",
            "exam_date": "2023-11-15",
            "total_score": 498.5,
            "overall_level": "B1"
        },
        {
            "exam_id": "exam_003",
            "exam_name": "2023学年第二学期期末考试", 
            "exam_date": "2023-07-10",
            "total_score": 456.0,
            "overall_level": "B2"
        },
        {
            "exam_id": "exam_004",
            "exam_name": "2023学年第二学期期中考试",
            "exam_date": "2023-05-15", 
            "total_score": 421.5,
            "overall_level": "C1"
        },
        {
            "exam_id": "exam_005",
            "exam_name": "2023学年第一学期期末考试",
            "exam_date": "2023-01-20",
            "total_score": 389.0,
            "overall_level": "C2"
        }
    ]
    
    # 应用分页
    total = len(mock_exams)
    paginated_exams = mock_exams[offset:offset + limit]
    
    # 转换为响应格式
    exam_items = []
    for exam in paginated_exams:
        exam_items.append(ExamItem(
            exam_id=exam["exam_id"],
            exam_name=exam["exam_name"],
            exam_date=exam["exam_date"],
            total_score=exam["total_score"],
            overall_level=exam["overall_level"]
        ))
    
    return ExamListResponse(
        items=exam_items,
        total=total
    )

@router.get("/exams/{exam_id}/scores", response_model=Page01ExamScores)
async def get_exam_scores(
    exam_id: str,
    current_user: Dict[str, Any] = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """01-获取考试成绩页数据"""
    
    # 模拟数据：根据exam_id返回不同的成绩
    mock_scores = {
        "exam_001": {
            "total_score": 532.0,
            "overall_level": "A3",
            "subject_scores": [
                {"subject": "语文", "score": 85.5, "level": "B1"},
                {"subject": "数学", "score": 92.0, "level": "A2"},
                {"subject": "英语", "score": 78.5, "level": "B2"},
                {"subject": "物理", "score": 88.0, "level": "A3"},
                {"subject": "化学", "score": 94.5, "level": "A1"},
                {"subject": "生物", "score": 83.5, "level": "B1"},
                {"subject": "文科综合", "score": 90.0, "level": "A2"}
            ]
        }
    }
    
    # 获取对应考试的成绩，如果不存在则使用默认数据
    exam_data = mock_scores.get(exam_id, mock_scores["exam_001"])
    
    return Page01ExamScores(
        total_score=exam_data["total_score"],
        overall_level=exam_data["overall_level"],
        subject_scores=[SubjectScore(**subject) for subject in exam_data["subject_scores"]]
    )

@router.get("/exams/{exam_id}/level-position", response_model=Page02LevelPosition)
async def get_level_position(
    exam_id: str,
    mode: str = Query(..., description="对比模式: class 或 grade"),
    current_user: Dict[str, Any] = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """02-获取等级位置页数据"""
    
    # 根据mode返回不同的对比数据
    grouping_mode = "班级" if mode == "class" else "年级"
    
    # 模拟科目对比数据
    subject_comparison = [
        {
            "subject": "语文",
            "score": 85.5,
            "rank": 15,
            "avg": 78.2,
            "max": 98.5,
            "diff": 13.0
        },
        {
            "subject": "数学", 
            "score": 92.0,
            "rank": 8,
            "avg": 82.1,
            "max": 100.0,
            "diff": 8.0
        },
        {
            "subject": "英语",
            "score": 78.5,
            "rank": 22,
            "avg": 75.3,
            "max": 95.0,
            "diff": 16.5
        },
        {
            "subject": "物理",
            "score": 88.0,
            "rank": 12,
            "avg": 76.8,
            "max": 96.5,
            "diff": 8.5
        },
        {
            "subject": "化学",
            "score": 94.5,
            "rank": 3,
            "avg": 79.2,
            "max": 98.0,
            "diff": 3.5
        },
        {
            "subject": "生物",
            "score": 83.5,
            "rank": 18,
            "avg": 77.6,
            "max": 92.5,
            "diff": 9.0
        }
    ]
    
    return Page02LevelPosition(
        grouping_mode=grouping_mode,
        class_size=45 if mode == "class" else 180,
        grade_size=180,
        subject_comparison=[SubjectComparison(**item) for item in subject_comparison]
    )

@router.get("/exams/{exam_id}/pk-analysis", response_model=Page03PKAnalysis)
async def get_pk_analysis(
    exam_id: str,
    class_id: Optional[str] = Query(None, description="班级ID"),
    current_user: Dict[str, Any] = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """03-获取成绩PK页数据"""
    
    # 模拟PK数据
    return Page03PKAnalysis(
        rank_percent=75.6,  # 击败了75.6%的同学
        rank_index=11,      # 排名第11
        class_total_students=45
    )

@router.post("/exams/{exam_id}/ideal-ranking", response_model=Page04IdealRanking)
async def calculate_ideal_ranking(
    exam_id: str,
    request: IdealScoresRequest,
    current_user: Dict[str, Any] = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """04-计算并获取理想排名页数据"""
    
    # 当前成绩数据
    current_subjects = [
        {"subject": "语文", "current_score": 85.5, "max_score": 150},
        {"subject": "数学", "current_score": 92.0, "max_score": 150},
        {"subject": "英语", "current_score": 78.5, "max_score": 150},
        {"subject": "物理", "current_score": 88.0, "max_score": 100},
        {"subject": "化学", "current_score": 94.5, "max_score": 100},
        {"subject": "生物", "current_score": 83.5, "max_score": 100}
    ]
    
    # 计算理想分数
    ideal_scores_dict = {item.subject: item.ideal_score for item in request.ideal_scores}
    
    subjects = []
    new_total_score = 0
    current_total = sum(s["current_score"] for s in current_subjects)
    
    for subject_data in current_subjects:
        subject = subject_data["subject"]
        ideal_score = ideal_scores_dict.get(subject, subject_data["current_score"])
        
        subjects.append(SubjectIdealScore(
            subject=subject,
            current_score=subject_data["current_score"],
            ideal_score=ideal_score,
            max_score=subject_data["max_score"]
        ))
        new_total_score += ideal_score
    
    # 计算排名变化（简单模拟）
    current_rank = 15
    score_improvement = new_total_score - current_total
    predicted_rank = max(1, current_rank - int(score_improvement / 10))  # 简单算法
    rank_change = current_rank - predicted_rank
    
    return Page04IdealRanking(
        subjects=subjects,
        new_total_score=new_total_score,
        predicted_rank=predicted_rank,
        rank_change=rank_change,
        current_rank=current_rank
    )

@router.get("/exams/{exam_id}/bias-analysis", response_model=Page05BiasAnalysis)
async def get_bias_analysis(
    exam_id: str,
    current_user: Dict[str, Any] = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """05-获取偏科分析页数据"""
    
    # 模拟雷达图数据
    radar_data = [
        {"subject": "语文", "total_win_rate": 75.6, "subject_win_rate": 68.2},
        {"subject": "数学", "total_win_rate": 75.6, "subject_win_rate": 85.3},
        {"subject": "英语", "total_win_rate": 75.6, "subject_win_rate": 62.1},
        {"subject": "物理", "total_win_rate": 75.6, "subject_win_rate": 78.9},
        {"subject": "化学", "total_win_rate": 75.6, "subject_win_rate": 92.4},
        {"subject": "生物", "total_win_rate": 75.6, "subject_win_rate": 71.5}
    ]
    
    return Page05BiasAnalysis(
        radar_data=[RadarData(**item) for item in radar_data],
        strength_subjects=["数学", "化学", "物理"],
        weak_subjects=["英语", "语文"]
    )

@router.get("/trend-analysis", response_model=Page06Trend)
async def get_trend_analysis(
    mode: str = Query(..., description="对比模式: class 或 school"),
    current_user: Dict[str, Any] = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """06-获取历次趋势页数据"""
    
    # 模拟历次考试趋势数据
    trend_data = [
        {"date": "2023年9月月考", "class_win_rate": 65.2, "school_win_rate": 58.3},
        {"date": "2023年10月月考", "class_win_rate": 71.8, "school_win_rate": 62.1},
        {"date": "2023年11月期中", "class_win_rate": 68.9, "school_win_rate": 60.5},
        {"date": "2023年12月月考", "class_win_rate": 73.2, "school_win_rate": 65.8},
        {"date": "2024年1月期末", "class_win_rate": 75.6, "school_win_rate": 67.2}
    ]
    
    analysis_text = "本次考试相比上次提升了2.4个百分点，在最近5次考试中排名第1。数学和化学是主要优势科目，英语仍需加强。"
    
    return Page06Trend(
        trend_data=[TrendData(**item) for item in trend_data],
        trend_analysis=analysis_text
    )

@router.get("/exams/{exam_id}/question-analysis", response_model=Page07QuestionAnalysis)
async def get_question_analysis(
    exam_id: str,
    subject: str = Query(..., description="科目名称"),
    current_user: Dict[str, Any] = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """07-获取试题分析页数据"""
    
    # 可选科目列表
    available_subjects = ["总分", "语文", "数学", "英语", "物理", "化学", "生物"]
    
    # 根据科目返回不同的题目数据
    subject_questions = {
        "数学": [
            {"id": 1, "type": "单选题", "correct_answer": "A", "full_score": 5.0, "score": 5.0, "analysis_url": None},
            {"id": 2, "type": "单选题", "correct_answer": "C", "full_score": 5.0, "score": 5.0, "analysis_url": None},
            {"id": 3, "type": "单选题", "correct_answer": "B", "full_score": 5.0, "score": 0.0, "analysis_url": None},
            {"id": 4, "type": "多选题", "correct_answer": "BC", "full_score": 5.0, "score": 3.0, "analysis_url": None},
            {"id": 5, "type": "填空题", "correct_answer": "32", "full_score": 5.0, "score": 5.0, "analysis_url": None},
            {"id": 6, "type": "解答题", "correct_answer": "见解析", "full_score": 12.0, "score": 10.0, "analysis_url": None},
            {"id": 7, "type": "解答题", "correct_answer": "见解析", "full_score": 12.0, "score": 8.0, "analysis_url": None},
            {"id": 8, "type": "解答题", "correct_answer": "见解析", "full_score": 14.0, "score": 12.0, "analysis_url": None}
        ]
    }
    
    # 获取当前科目的题目，如果不存在则返回默认数据
    current_questions = subject_questions.get(subject, subject_questions["数学"])
    
    return Page07QuestionAnalysis(
        selected_subject=subject,
        available_subjects=available_subjects,
        current_questions=[QuestionItem(**q) for q in current_questions]
    )

@router.get("/exams/{exam_id}/loss-analysis", response_model=Page08LossAnalysis)
async def get_loss_analysis(
    exam_id: str,
    current_user: Dict[str, Any] = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """08-获取失分分析页数据"""
    
    # 难度分析数据
    difficulty_analysis = [
        {
            "level": "极易",
            "total_score": 25.0,
            "count": 5,
            "correct": 4,
            "partial": 1,
            "rate": 90.0,
            "question_numbers": ["1", "2", "5", "8", "12"]
        },
        {
            "level": "较易", 
            "total_score": 30.0,
            "count": 6,
            "correct": 5,
            "partial": 0,
            "rate": 83.3,
            "question_numbers": ["3", "6", "9", "13", "16", "19"]
        },
        {
            "level": "适中",
            "total_score": 35.0,
            "count": 7,
            "correct": 4,
            "partial": 2,
            "rate": 71.4,
            "question_numbers": ["4", "7", "10", "14", "17", "20", "22"]
        },
        {
            "level": "较难",
            "total_score": 25.0,
            "count": 5,
            "correct": 2,
            "partial": 1,
            "rate": 50.0,
            "question_numbers": ["11", "15", "18", "21", "23"]
        },
        {
            "level": "极难",
            "total_score": 15.0,
            "count": 3,
            "correct": 1,
            "partial": 1,
            "rate": 33.3,
            "question_numbers": ["24", "25", "26"]
        }
    ]
    
    return Page08LossAnalysis(
        difficulty_analysis=[DifficultyAnalysis(**item) for item in difficulty_analysis],
        loss_questions=LossQuestions(
            全部丢分=["单选3", "多选11", "填空18"],
            部分丢分=["解答22", "解答23", "解答25"]
        ),
        优势得分题=["单选1", "单选2", "填空5", "解答8"],
        潜力追分题=["单选4", "多选7", "解答10", "解答14"],
        gain_prediction=GainPrediction(
            potential_gain_score=16.5,
            rank_improvement=8
        )
    )

@router.get("/exams/{exam_id}/knowledge-analysis", response_model=Page09KnowledgeAnalysis)
async def get_knowledge_analysis(
    exam_id: str,
    current_user: Dict[str, Any] = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """09-获取知识点分析页数据"""
    
    # 知识点分析数据
    knowledge_points = [
        {"name": "函数与导数", "class_rate": 78.5, "personal_rate": 85.2, "level": "优秀掌握"},
        {"name": "三角函数", "class_rate": 72.3, "personal_rate": 90.1, "level": "优秀掌握"},
        {"name": "数列", "class_rate": 68.9, "personal_rate": 75.6, "level": "及格掌握"},
        {"name": "立体几何", "class_rate": 65.2, "personal_rate": 58.3, "level": "未掌握"},
        {"name": "解析几何", "class_rate": 62.1, "personal_rate": 68.9, "level": "及格掌握"},
        {"name": "概率统计", "class_rate": 70.8, "personal_rate": 82.4, "level": "优秀掌握"},
        {"name": "平面向量", "class_rate": 75.2, "personal_rate": 65.7, "level": "未掌握"},
        {"name": "不等式", "class_rate": 73.6, "personal_rate": 78.9, "level": "及格掌握"}
    ]
    
    return Page09KnowledgeAnalysis(
        knowledge_points=[KnowledgePoint(**item) for item in knowledge_points],
        tabs=["满分知识点", "优势知识点", "短板知识点"]
    ) 