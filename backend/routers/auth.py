from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional

from database import get_db
from auth import create_access_token, get_wechat_session
from models import Student

router = APIRouter(prefix="/auth", tags=["认证 (Authentication)"])

class LoginRequest(BaseModel):
    code: str
    userType: str
    identityId: str
    password: str

class UserInfo(BaseModel):
    id: str
    name: str
    type: str
    avatar: Optional[str] = None

class LoginResponse(BaseModel):
    token: str
    userInfo: UserInfo

@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """用户登录与身份绑定"""
    
    # 1. 验证微信code（在生产环境中会调用微信API）
    try:
        # wechat_session = get_wechat_session(request.code)
        # 测试环境跳过微信验证
        pass
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"微信登录验证失败: {str(e)}"
        )
    
    # 2. 验证用户身份（学号/工号和密码）
    if request.userType == "student":
        # 模拟学生验证
        if request.identityId == "20240001" and request.password == "123456":
            user_info = UserInfo(
                id="1",
                name="张三",
                type="student",
                avatar="https://example.com/avatar.jpg"
            )
            token_data = {
                "sub": "1",
                "user_type": "student",
                "name": "张三",
                "student_code": "20240001"
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="学号或密码错误"
            )
    
    elif request.userType == "teacher":
        # 模拟教师验证
        if request.identityId == "teacher001" and request.password == "123456":
            user_info = UserInfo(
                id="t1",
                name="王老师",
                type="teacher",
                avatar="https://example.com/teacher_avatar.jpg"
            )
            token_data = {
                "sub": "t1",
                "user_type": "teacher",
                "name": "王老师",
                "teacher_id": "teacher001"
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="工号或密码错误"
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="不支持的用户类型"
        )
    
    # 3. 生成JWT令牌
    access_token = create_access_token(data=token_data)
    
    return LoginResponse(
        token=access_token,
        userInfo=user_info
    ) 