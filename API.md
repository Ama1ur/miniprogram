# API 文档

本文档描述了成绩报告小程序的主要数据接口和数据结构。

## 📋 基础接口

### 用户认证

#### 登录接口
```
POST /api/auth/login
```

**请求参数:**
```json
{
  "code": "微信登录凭证",
  "userType": "student|teacher",
  "userInfo": {
    "studentId": "学号（学生）",
    "teacherId": "工号（教师）",
    "password": "密码"
  }
}
```

**响应数据:**
```json
{
  "code": 200,
  "message": "登录成功",
  "data": {
    "token": "JWT令牌",
    "userInfo": {
      "id": "用户ID",
      "name": "姓名",
      "type": "用户类型",
      "avatar": "头像URL"
    }
  }
}
```

## 🎓 学生端接口

### 获取成绩列表
```
GET /api/student/scores
```

**查询参数:**
- `page`: 页码（默认1）
- `limit`: 每页数量（默认10）
- `examId`: 考试ID（可选）

**响应数据:**
```json
{
  "code": 200,
  "data": {
    "list": [
      {
        "examId": "考试ID",
        "examName": "考试名称",
        "examDate": "2024-01-15",
        "totalScore": 532,
        "rank": 12,
        "level": "A3",
        "subjects": [
          {
            "subject": "语文",
            "score": 85,
            "fullScore": 100,
            "level": "B1",
            "rank": 15
          }
        ]
      }
    ],
    "total": 50,
    "page": 1,
    "limit": 10
  }
}
```

### 获取成绩详情
```
GET /api/student/scores/{examId}
```

**响应数据:**
```json
{
  "code": 200,
  "data": {
    "examInfo": {
      "id": "考试ID",
      "name": "2024年期末考试",
      "date": "2024-01-15",
      "type": "期末考试"
    },
    "totalScore": 532,
    "rank": 12,
    "level": "A3",
    "subjects": [
      {
        "subject": "语文",
        "score": 85,
        "fullScore": 100,
        "level": "B1",
        "rank": 15,
        "classAvg": 78.5,
        "gradeAvg": 76.8
      }
    ]
  }
}
```

### 获取等级位置分析
```
GET /api/student/level-comparison/{examId}
```

**查询参数:**
- `mode`: 对比模式（class|grade）

**响应数据:**
```json
{
  "code": 200,
  "data": {
    "grouping_mode": "班级",
    "class_size": 45,
    "grade_size": 680,
    "subject_comparison": [
      {
        "subject": "语文",
        "score": 85,
        "rank": 12,
        "avg": 78.5,
        "max": 95,
        "diff": -10
      }
    ]
  }
}
```

### 获取学情分析
```
GET /api/student/analysis/{examId}
```

**查询参数:**
- `type`: 分析类型（trend|radar|knowledge|bias|loss）

**响应数据:**
```json
{
  "code": 200,
  "data": {
    "trend": {
      "trend_data": [
        {
          "date": "2024-01",
          "class_win_rate": 65,
          "school_win_rate": 72
        }
      ],
      "trend_analysis": "这次比上次提升了10个名次"
    },
    "radar": {
      "radar_data": [
        {
          "subject": "语文",
          "total_win_rate": 75,
          "subject_win_rate": 82
        }
      ],
      "strength_subjects": ["数学", "生物"],
      "weak_subjects": ["物理", "化学"]
    },
    "knowledge": {
      "tabs": ["满分知识点", "优势知识点", "短板知识点"],
      "knowledge_points": [
        {
          "name": "函数与导数",
          "class_rate": 80,
          "personal_rate": 85,
          "level": "优秀掌握"
        }
      ]
    },
    "loss": {
      "difficulty_analysis": [
        {
          "level": "极易",
          "count": 2,
          "correct": 0,
          "rate": 12.55,
          "question_numbers": ["1", "2", "5"]
        }
      ],
      "loss_questions": {
        "全部丢分": ["单选3", "单选8"],
        "部分丢分": ["填空题", "22", "23"]
      },
      "gain_prediction": {
        "potential_gain_score": 16,
        "rank_improvement": 28
      }
    }
  }
}
```

### 获取试题分析
```
GET /api/student/questions/{examId}
```

**查询参数:**
- `subject`: 科目名称（总分|语文|数学|英语|物理|化学|生物）

**响应数据:**
```json
{
  "code": 200,
  "data": {
    "selected_subject": "语文",
    "available_subjects": ["语文", "数学", "英语", "物理", "化学", "生物"],
    "current_questions": [
      {
        "id": 1,
        "type": "单选题",
        "correct_answer": "A",
        "full_score": 5,
        "score": 5,
        "analysis_url": "/analysis/detail/1"
      }
    ]
  }
}
```

### 理想排名计算
```
POST /api/student/ideal-ranking/{examId}
```

**请求参数:**
```json
{
  "ideal_scores": [
    {
      "subject": "语文",
      "ideal_score": 90
    },
    {
      "subject": "数学",
      "ideal_score": 100
    }
  ]
}
```

**响应数据:**
```json
{
  "code": 200,
  "data": {
    "subjects": [
      {
        "subject": "语文",
        "current_score": 85,
        "ideal_score": 90,
        "max_score": 150
      }
    ],
    "new_total_score": 555,
    "predicted_rank": 8,
    "rank_change": 7,
    "current_rank": 15
  }
}
```

## 👨‍🏫 教师端接口

### 获取班级列表
```
GET /api/teacher/classes
```

**响应数据:**
```json
{
  "code": 200,
  "data": [
    {
      "id": "班级ID",
      "name": "高三1班",
      "grade": "高三",
      "studentCount": 45,
      "subjects": ["语文", "数学", "英语"]
    }
  ]
}
```

### 获取班级成绩
```
GET /api/teacher/classes/{classId}/scores
```

**查询参数:**
- `examId`: 考试ID
- `subject`: 科目（可选）
- `orderBy`: 排序字段（total|subject）
- `order`: 排序方向（asc|desc）

**响应数据:**
```json
{
  "code": 200,
  "data": {
    "examInfo": {
      "id": "考试ID",
      "name": "2024年期末考试"
    },
    "classInfo": {
      "id": "班级ID",
      "name": "高三1班",
      "studentCount": 45
    },
    "statistics": {
      "avgScore": 485.6,
      "maxScore": 620,
      "minScore": 320,
      "passRate": 85.5,
      "excellentRate": 42.2
    },
    "students": [
      {
        "studentId": "学号",
        "name": "姓名",
        "totalScore": 532,
        "rank": 12,
        "subjects": [
          {
            "subject": "语文",
            "score": 85,
            "rank": 15
          }
        ]
      }
    ]
  }
}
```

### 获取班级分析
```
GET /api/teacher/classes/{classId}/analysis
```

**响应数据:**
```json
{
  "code": 200,
  "data": {
    "scoreDistribution": [
      {
        "range": "600-650",
        "count": 5,
        "percentage": 11.1
      }
    ],
    "subjectAnalysis": [
      {
        "subject": "语文",
        "avgScore": 78.5,
        "passRate": 88.9,
        "excellentRate": 33.3,
        "difficulty": "适中"
      }
    ],
    "trendAnalysis": [
      {
        "examName": "期中考试",
        "avgScore": 475.2
      }
    ]
  }
}
```

## 💰 付费功能接口

### 检查付费状态
```
GET /api/payment/status
```

**响应数据:**
```json
{
  "code": 200,
  "data": {
    "isPremium": true,
    "expireDate": "2025-01-15",
    "features": ["analysis", "trend", "knowledge"]
  }
}
```

### 创建支付订单
```
POST /api/payment/create
```

**请求参数:**
```json
{
  "productId": "premium_analysis",
  "amount": 9.9
}
```

**响应数据:**
```json
{
  "code": 200,
  "data": {
    "orderId": "订单ID",
    "paymentInfo": {
      "appId": "小程序AppID",
      "timeStamp": "时间戳",
      "nonceStr": "随机字符串",
      "package": "统一下单接口返回的package参数",
      "signType": "MD5",
      "paySign": "签名"
    }
  }
}
```

## 📊 数据结构

### 用户信息
```typescript
interface User {
  id: string;
  name: string;
  type: 'student' | 'teacher';
  avatar?: string;
  studentId?: string; // 学生学号
  teacherId?: string; // 教师工号
  classId?: string;   // 所属班级
  grade?: string;     // 年级
}
```

### 考试信息
```typescript
interface Exam {
  id: string;
  name: string;
  date: string;
  type: string;
  subjects: string[];
  totalScore: number;
  duration: number; // 考试时长（分钟）
}
```

### 成绩信息
```typescript
interface Score {
  examId: string;
  studentId: string;
  totalScore: number;
  rank: number;
  level: string;
  subjects: SubjectScore[];
}

interface SubjectScore {
  subject: string;
  score: number;
  fullScore: number;
  level: string;
  rank: number;
  classAvg: number;
  gradeAvg: number;
}
```

### 分析数据
```typescript
interface Analysis {
  trend?: TrendData;
  radar?: RadarData;
  knowledge?: KnowledgeData;
  loss?: LossData;
}

interface TrendData {
  trend_data: Array<{
    date: string;
    class_win_rate: number;
    school_win_rate: number;
  }>;
  trend_analysis: string;
}

interface RadarData {
  radar_data: Array<{
    subject: string;
    total_win_rate: number;
    subject_win_rate: number;
  }>;
  strength_subjects: string[];
  weak_subjects: string[];
}

interface KnowledgeData {
  tabs: string[];
  knowledge_points: Array<{
    name: string;
    class_rate: number;
    personal_rate: number;
    level: string;
  }>;
}

interface LossData {
  difficulty_analysis: Array<{
    level: string;
    count: number;
    correct: number;
    rate: number;
    question_numbers: string[];
  }>;
  loss_questions: {
    "全部丢分": string[];
    "部分丢分": string[];
  };
  gain_prediction: {
    potential_gain_score: number;
    rank_improvement: number;
  };
}
```

### 理想排名数据
```typescript
interface IdealRanking {
  subjects: Array<{
    subject: string;
    current_score: number;
    ideal_score: number;
    max_score: number;
  }>;
  new_total_score: number;
  predicted_rank: number;
  rank_change: number;
  current_rank: number;
}
```

### 试题分析数据
```typescript
interface QuestionAnalysis {
  selected_subject: string;
  available_subjects: string[];
  current_questions: Array<{
    id: number;
    type: string;
    correct_answer: string;
    full_score: number;
    score: number;
    analysis_url?: string;
  }>;
}
```

## 🔒 错误码说明

| 错误码 | 说明 |
|--------|------|
| 200 | 成功 |
| 400 | 请求参数错误 |
| 401 | 未授权 |
| 403 | 权限不足 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |
| 1001 | 用户不存在 |
| 1002 | 密码错误 |
| 1003 | 账号已被禁用 |
| 2001 | 成绩数据不存在 |
| 2002 | 考试未结束 |
| 2003 | 理想分数输入无效 |
| 3001 | 需要付费解锁 |
| 3002 | 支付失败 |

## 🔧 请求规范

### 请求头
```
Authorization: Bearer {token}
Content-Type: application/json
User-Agent: MiniProgram/1.0.0
```

### 响应格式
```json
{
  "code": 200,
  "message": "success",
  "data": {},
  "timestamp": 1640995200
}
```

### 分页参数
```json
{
  "page": 1,
  "limit": 10,
  "total": 100,
  "hasMore": true
}
```

## 📝 注意事项

1. **认证**: 除登录接口外，所有接口都需要在请求头中携带有效的JWT令牌
2. **权限**: 学生只能查看自己的数据，教师只能查看自己班级的数据
3. **付费**: 部分高级功能需要付费解锁才能访问
4. **缓存**: 成绩数据建议缓存，减少重复请求
5. **限流**: API有调用频率限制，请合理安排请求
6. **HTTPS**: 生产环境必须使用HTTPS协议
7. **理想排名**: 理想排名计算基于历史数据统计模型，仅供参考

## 🆕 更新说明

### v2.0 更新内容：
1. **删除功能**: 移除了答题卡相关接口和数据结构
2. **等级位置**: 删除了联考排名选项，仅支持班级和年级对比
3. **理想排名**: 新增交互式理想排名计算功能
4. **试题分析**: 支持按科目筛选查看题目分析
5. **失分分析**: 增加题号显示，便于定位具体题目

## 🌐 环境配置

### 开发环境
```
BASE_URL: https://dev-api.example.com
```

### 测试环境
```
BASE_URL: https://test-api.example.com
```

### 生产环境
```
BASE_URL: https://api.example.com
``` 