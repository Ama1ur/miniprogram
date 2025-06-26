# 学生考试分析与成绩展示小程序 - 后端API

这是一个基于FastAPI框架开发的微信小程序后端API，为学生提供考试成绩分析、学情诊断和成绩展示功能。

## 项目结构

```
├── main.py                 # FastAPI应用主文件
├── config.py              # 应用配置文件
├── config_example.py      # 配置文件示例
├── database.py            # 数据库连接配置
├── auth.py                # JWT认证模块
├── models.py              # 数据库模型(已存在)
├── requirements.txt       # Python依赖包
├── routers/               # API路由模块
│   ├── __init__.py
│   ├── auth.py           # 认证相关路由
│   └── student.py        # 学生端路由
└── openapi.yaml          # API文档(已存在)
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置数据库

将 `config_example.py` 复制为 `config.py` 并修改数据库连接配置：

```python
database_url = "mysql+pymysql://用户名:密码@主机:端口/数据库名"
```

### 3. 配置JWT密钥

在 `config.py` 中设置一个强密钥：

```python
secret_key = "your-super-secret-key-here"
```

### 4. 配置微信小程序

在微信公众平台获取小程序的 AppID 和 AppSecret，并在 `config.py` 中配置：

```python
wechat_app_id = "your-wechat-app-id"
wechat_app_secret = "your-wechat-app-secret"
```

### 5. 启动应用

```bash
# 方式1: 直接运行
python main.py

# 方式2: 使用uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 6. 访问API文档

启动后访问以下地址查看API文档：

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 已实现的功能

### 1. 用户认证 (`/auth/login`)

- **功能**: 微信小程序用户登录与身份绑定
- **方法**: POST
- **参数**: 
  - `code`: 微信登录凭证
  - `userType`: 用户类型 (student/teacher)
  - `identityId`: 学号或工号
  - `password`: 密码
- **返回**: JWT令牌和用户信息

**测试示例**:
```json
{
  "code": "mock_code_123",
  "userType": "student", 
  "identityId": "20240001",
  "password": "123456"
}
```

### 2. 学生历史考试列表 (`/student/exams`)

- **功能**: 获取学生参加过的所有历史考试
- **方法**: GET
- **认证**: 需要Bearer Token
- **参数**: 
  - `page`: 页码 (默认1)
  - `limit`: 每页数量 (默认10)
- **返回**: 考试列表和总数

## JWT认证使用方式

1. 首先调用 `/auth/login` 获取token
2. 在后续请求的Header中加入：
   ```
   Authorization: Bearer {your_token_here}
   ```

## 数据库模型

项目使用SQLAlchemy ORM，主要模型包括：

- `Exam`: 考试信息
- `Student`: 学生信息
- `Subject`: 科目信息
- `Question`: 题目信息
- `Answer`: 学生答案
- `GradeRecord`: 评分记录

## 开发说明

### 添加新的API接口

1. 在相应的路由文件中添加新的路由函数
2. 使用适当的认证依赖项 (`get_current_student` 或 `get_current_teacher`)
3. 添加合适的Pydantic模型用于请求和响应
4. 在main.py中注册新的路由器

### 认证依赖项

- `get_current_user`: 获取当前认证用户
- `get_current_student`: 获取当前学生用户  
- `get_current_teacher`: 获取当前教师用户

### 数据库会话

使用 `get_db()` 依赖项获取数据库会话：

```python
from database import get_db

@router.get("/example")
async def example_endpoint(db: Session = Depends(get_db)):
    # 使用db进行数据库操作
    pass
```

## 待实现的功能

根据 `openapi.yaml` 规范，还需要实现以下接口：

- 考试成绩详情页
- 等级位置分析
- 成绩PK分析  
- 理想排名计算
- 偏科分析
- 历次趋势分析
- 试题分析
- 失分分析
- 知识点分析
- 教师端接口

## 注意事项

1. **安全性**: 生产环境中请修改默认的JWT密钥
2. **CORS**: 生产环境中请限制CORS允许的域名
3. **数据库**: 确保MySQL数据库已创建并可连接
4. **微信接口**: 开发阶段可以使用模拟数据，生产环境需要真实的微信AppID和AppSecret

## 错误处理

API使用标准的HTTP状态码：

- `200`: 成功
- `400`: 请求参数错误
- `401`: 认证失败
- `403`: 权限不足
- `404`: 资源不存在
- `500`: 服务器内部错误 