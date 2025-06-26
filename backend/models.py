from sqlalchemy import Column, String, Integer, Text, ForeignKey, DateTime, DECIMAL, create_engine, Table
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy import LargeBinary, UniqueConstraint
from datetime import datetime,timezone
from typing import List, Optional

from sqlalchemy import BigInteger, Column, DECIMAL, DateTime, ForeignKeyConstraint, Index, LargeBinary, String, Table, Text
from sqlalchemy.dialects.mysql import TEXT
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


dbtype="mysql"
Base = declarative_base()

# 多对多中间表：题目和阅卷人之间的多对多关系
question_reviewer = Table(
    'question_reviewer', Base.metadata,
    Column('question_id', BIGINT, ForeignKey('question.id'), primary_key=True),
    Column('reviewer_id', BIGINT, ForeignKey('reviewer.id'), primary_key=True)
)

# 考试表
class Exam(Base):
    __tablename__ = 'exam'
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    intro = Column(Text)                        # 考试说明
    school_name = Column(String(255))           # 学校名称
    uploader_id = Column(Text)                  # 上传者 ID
    chief_teacher_id = Column(Text)             # 主责任教师 ID
    grade = Column(String(50))                  # 年级
    material_root = Column(Text)                # 考试材料包的根目录。可能是路径，可能是bucket/key
    # 一场考试有多个科目，一对多关系
    subjects = relationship("Subject", back_populates="exam")
    rawanswersheets = relationship("RawAnswerSheet", back_populates="exam")

# 科目表
class Subject(Base):
    __tablename__ = 'subject'
    __table_args__ = (
        UniqueConstraint('exam_id', 'name', name='uq_subject_exam_name'),
    )
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    exam_id = Column(BIGINT, ForeignKey('exam.id'))    # 多对一：属于某场考试
    name = Column(String(10))                          # 科目名称

    # 存储原始文件路径及二进制内容,以exam.material_root为根基
    question_path = Column(Text)
    ref_answer_path = Column(Text)
    sample_answer_sheet_path = Column(Text)

    question = Column(LargeBinary)
    ref_answer = Column(LargeBinary)
    sample_answer_sheet = Column(LargeBinary)

    answer_sheet_division = Column(Text)  # 答题卡切分配置（JSON 格式字符串）
    choice_sheet_location_list = Column(Text) #保存多选题的位置
    # ORM 关系
    exam = relationship("Exam", back_populates="subjects")  # 多对一：属于某个考试
    questions = relationship("Question", back_populates="subject")  # 一对多：包含某几个问题
    rawanswersheets = relationship("RawAnswerSheet", back_populates="subject")  # 一对多：包含多个答题卡


# 题目表
class Question(Base):
    __tablename__ = 'question'
    __table_args__ = (
        UniqueConstraint('subject_id', 'question_code', name='uq_subject_exam_name'),
    )
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    subject_id = Column(BIGINT, ForeignKey('subject.id'))  # 多对一：属于某个科目
    question_code = Column(BIGINT)                        # 题号

    # 题目图文、参考答案、评分模版
    #每一项有原始图片、识别后文本、路径 （exam.material_root）为基准

    question_text = Column(Text)
    question_path = Column(Text)

# 我们很可能不再需要大二进制文件了，我们选择用oss储存


    ref_answer_text = Column(Text)
    ref_answer_path= Column(Text)


    template_text = Column(Text)
    template_path = Column(Text)

    strategy = Column(Text)              # 评分策略
    full_score = Column(DECIMAL(5, 2))   # 满分
    question_type = Column(String(50))  # 问题类型
    question_division=Column(Text)          #一个json文件，包含一个xywh坐标，从原始答题卡划分为本题。
    sub_ocr_division= Column(Text)          #一个json列表，包含一组xywh坐标，从本题划分到子题，用于OCR
    
    subject = relationship("Subject", back_populates="questions")     # 多对一：属于某个科目
    answers = relationship("Answer", back_populates="question")       # 一对多：包含多个答案
    reviewers = relationship("Reviewer", secondary=question_reviewer, back_populates="questions")  # 多对多：若干监考老师对应若干问题

# 原始答题卡表
class RawAnswerSheet(Base):
    __tablename__ = 'raw_answer_sheet'
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    subject_id = Column(BIGINT, ForeignKey('subject.id'))  # 属于哪个科目
    student_id = Column(BIGINT, ForeignKey('student.id'), nullable=True)  # 学生 ID，可为空
    student_code = Column(String(50))  # 学生编号
    exam_id = Column(BIGINT, ForeignKey('exam.id'))    # 多对一：属于某场考试

    student = relationship("Student", back_populates="raw_sheets")  # 多对一 ：属于某个学生
    raw_image_path = Column(Text)                                   # 原始答题卡图片路径
    raw_image_blob = Column(LargeBinary)                            # 图片数据

     # ORM 关系
    exam = relationship("Exam", back_populates="rawanswersheets")  # 多对一：属于某个考试
    subject = relationship("Subject", back_populates="rawanswersheets")  # 多对一：属于某个科目

# 学生表
class Student(Base):
    __tablename__ = 'student'
    __table_args__ = (
        UniqueConstraint('student_code', name='uq_student_code'),
    )
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    student_code = Column(String(50))  # 学生编号
    name = Column(String(100))         # 学生姓名
    cclass =Column(BIGINT)          # 学生班级
    raw_sheets = relationship("RawAnswerSheet", back_populates="student")  # 一对多：学生拥有多张答题卡
    answers = relationship("Answer", back_populates="student")             # 一对多：学生拥有多个答案

# 答案表
class Answer(Base):
    __tablename__ = 'answer'
    __table_args__ = (
        UniqueConstraint('question_id', 'student_id', name='uq_question_student'),
    )
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    raw_sheet_id = Column(BIGINT, ForeignKey('raw_answer_sheet.id'), nullable=True)  # 原始答题卡 ID
    student_id = Column(BIGINT, ForeignKey('student.id'))          # 多对一：属于某个学生
    question_id = Column(BIGINT, ForeignKey('question.id'))        # 多对一：属于某个题目
    question_code = Column(BIGINT)                                # 题号

    answer_image_path = Column(Text)                # 学生作答图片路径(相对于exam.material_root)
    answer_text = Column(Text)                      # 识别出的文本答案

    final_score = Column(DECIMAL(5, 2))      # 最终得分
    final_comment = Column(Text)             # 最终评语

    student = relationship("Student", back_populates="answers")            # 多对一:属于某个学生
    question = relationship("Question", back_populates="answers")          # 多对一：属于某个题目
    grade_records = relationship("GradeRecord", back_populates="answer")   # 一对多：包含多个评分记录
    raw_sheet = relationship("RawAnswerSheet")                             # 多对一（未指定 back_populates）

# 阅卷人（评卷老师）
class Reviewer(Base):
    __tablename__ = 'reviewer'
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    name = Column(String(100))

    grade_records = relationship("GradeRecord", back_populates="reviewer")  # 一对多：一个阅卷人可以有多个评分记录
    questions = relationship("Question", secondary=question_reviewer, back_populates="reviewers")  # 多对多：阅卷人可评多个题目

# 评分记录
class GradeRecord(Base):
    __tablename__ = 'grade_record'
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    answer_id = Column(BIGINT, ForeignKey('answer.id'))          # 多对一：属于某个答案
    reviewer_id = Column(BIGINT, ForeignKey('reviewer.id'))      # 多对一：属于某个评卷人
    score = Column(DECIMAL(5, 2))                                # 分数
    comment = Column(Text)                                       # 评语
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))        # 时间戳

    answer = relationship("Answer", back_populates="grade_records")     # 多对一：属于某个答案
    reviewer = relationship("Reviewer", back_populates="grade_records") # 多对一：属于某个评卷人

#prompt表
class GradePrompts(Base):
    __tablename__ = 'gradeprompts'
    __table_args__ = {'comment': '储存所有用来打分的propmt'}

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    type: Mapped[Optional[str]] = mapped_column(String(100, 'utf8mb4_general_ci'), comment='prompt类型:\r\nOCR\r\ngrade_phase1\r\ngrade_phase2\r\n...')
    prompt: Mapped[Optional[str]] = mapped_column(Text(collation='utf8mb4_general_ci'), comment='真正的prompt本体')
    comment: Mapped[Optional[str]] = mapped_column(Text(collation='utf8mb4_general_ci'), comment='解释,比如生物填空题prompt') 