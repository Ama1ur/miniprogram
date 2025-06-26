#!/usr/bin/env python3
"""
学生考试分析小程序后端启动脚本
"""

import sys
import os

def main():
    """主启动函数"""
    try:
        import uvicorn
    except ImportError:
        print("错误: 请先安装依赖包")
        print("运行: pip install -r requirements.txt")
        sys.exit(1)
    
    # 检查配置文件是否存在
    if not os.path.exists("config.py"):
        print("警告: config.py 文件不存在")
        print("请将 config_example.py 复制为 config.py 并修改相应配置")
        print("或者创建 .env 文件设置环境变量")
        print()
    
    print("正在启动学生考试分析小程序后端API...")
    print("API文档地址: http://localhost:8000/docs")
    print("ReDoc文档: http://localhost:8000/redoc")
    print("按 Ctrl+C 停止服务")
    print("-" * 50)
    
    # 启动应用
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # 开发模式，代码更改时自动重载
        log_level="info"
    )

if __name__ == "__main__":
    main() 
 