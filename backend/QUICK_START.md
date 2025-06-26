# 🚀 快速开始指南

## 📋 前置条件

- Python 3.8+
- MySQL数据库 (可选，使用模拟数据)

## ⚡ 5分钟快速启动

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置数据库 (可选)

```bash
# 复制配置文件
cp config_example.py config.py

# 编辑 config.py 中的数据库连接 (如果需要)
# 不配置也可以运行，会使用模拟数据
```

### 3. 启动API服务

```bash
python start.py
```

看到以下输出表示启动成功：
```
正在启动学生考试分析小程序后端API...
API文档地址: http://localhost:8000/docs
ReDoc文档: http://localhost:8000/redoc
按 Ctrl+C 停止服务
--------------------------------------------------
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### 4. 验证API服务

打开浏览器访问：http://localhost:8000/docs

您应该看到完整的API文档界面。

### 5. 运行完整测试

```bash
# 在新的终端窗口中运行
python test_complete_apis.py
```

## 🧪 测试用户账号

### 学生账号
- **用户类型**: student
- **账号**: 20240001
- **密码**: 123456

### 教师账号
- **用户类型**: teacher  
- **账号**: teacher001
- **密码**: 123456

## 📖 API使用示例

### 1. 学生登录

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "mock_code_123",
    "userType": "student",
    "identityId": "20240001",
    "password": "123456"
  }'
```

### 2. 获取考试列表

```bash
curl -X GET "http://localhost:8000/student/exams" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### 3. 教师登录

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "mock_code_teacher",
    "userType": "teacher",
    "identityId": "teacher001",
    "password": "123456"
  }'
```

### 4. 获取班级列表

```bash
curl -X GET "http://localhost:8000/teacher/classes" \
  -H "Authorization: Bearer YOUR_TEACHER_TOKEN_HERE"
```

## 🎯 关键功能测试

### 学生端功能
1. ✅ 登录认证
2. ✅ 查看历史考试
3. ✅ 考试成绩分析
4. ✅ 等级位置对比
5. ✅ 成绩PK排名
6. ✅ 理想排名计算
7. ✅ 偏科分析雷达图
8. ✅ 历次趋势分析
9. ✅ 试题分析详情
10. ✅ 失分分析诊断
11. ✅ 知识点掌握分析

### 教师端功能
1. ✅ 教师登录认证
2. ✅ 班级列表管理
3. ✅ 班级成绩单查看
4. ✅ 权限控制验证

## 🔍 故障排除

### 常见问题

**Q: 启动时报错 "ImportError: No module named 'xxx'"**
A: 请确保已安装所有依赖：`pip install -r requirements.txt`

**Q: 端口8000被占用**
A: 修改 `start.py` 中的端口号，或者先关闭占用8000端口的程序

**Q: 测试脚本连接失败**
A: 确保API服务已启动且运行在正确端口

**Q: 数据库连接失败**  
A: 项目使用模拟数据，无需配置数据库也可正常运行

### 检查服务状态

```bash
# 检查服务健康状态
curl http://localhost:8000/health

# 期望响应
{"status": "healthy"}
```

### 日志调试

如果遇到问题，查看终端中的详细日志输出。API服务会显示：
- 请求路径
- 响应状态码
- 错误信息
- SQL查询 (如果连接了数据库)

## 🌟 下一步

1. **探索API文档**: http://localhost:8000/docs
2. **查看完整指南**: [API_使用指南.md](API_使用指南.md)
3. **了解项目架构**: [backend_README.md](backend_README.md)
4. **微信小程序接入**: 使用这些API开发前端界面

## 💡 提示

- 首次使用建议运行 `test_complete_apis.py` 验证所有功能
- API支持跨域访问，可直接从前端调用
- 所有接口都有详细的错误信息返回
- 支持热重载，修改代码后自动重启

**🎉 现在您已经成功启动了完整的考试分析API系统！** 