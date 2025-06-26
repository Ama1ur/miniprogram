from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import create_tables
from routers import auth, student, teacher
from config import settings

# 创建FastAPI应用实例
app = FastAPI(
    title="学生考试分析与成绩展示小程序 API",
    description="一个为学生提供考试成绩分析、学情诊断和成绩展示的微信小程序后端API。支持多维度成绩对比、偏科分析、失分分析和理想排名预测等功能。",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境中应该限制为特定域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth.router)
app.include_router(student.router)
app.include_router(teacher.router)

# 根路径
@app.get("/")
async def root():
    """API根路径"""
    return {
        "message": "学生考试分析与成绩展示小程序 API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

# 健康检查
@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {"status": "healthy"}

# 应用启动事件
@app.on_event("startup")
async def startup_event():
    """应用启动时执行的操作"""
    # 创建数据库表
    create_tables()
    print("数据库表创建完成")
    print(f"API文档地址: http://localhost:8000/docs")

# 应用关闭事件
@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭时执行的操作"""
    print("应用正在关闭...")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True,  # 开发模式，代码更改时自动重载
        log_level="info"
    ) 