#!/usr/bin/env python3
"""
API测试脚本
演示如何调用学生考试分析小程序的API接口
"""

import requests
import json

# API基础URL
BASE_URL = "http://localhost:8000"

def test_login():
    """测试登录接口"""
    print("=== 测试用户登录 ===")
    
    login_data = {
        "code": "mock_code_123",
        "userType": "student", 
        "identityId": "20240001",
        "password": "123456"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("登录成功!")
            print(f"用户信息: {result['userInfo']}")
            token = result['token']
            print(f"Token: {token[:50]}...")
            return token
        else:
            print(f"登录失败: {response.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("连接失败，请确保API服务已启动 (运行 python start.py)")
        return None
    except Exception as e:
        print(f"请求出错: {e}")
        return None

def test_get_exams(token):
    """测试获取考试列表接口"""
    print("\n=== 测试获取考试列表 ===")
    
    if not token:
        print("需要先登录获取token")
        return
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    params = {
        "page": 1,
        "limit": 5
    }
    
    try:
        response = requests.get(f"{BASE_URL}/student/exams", headers=headers, params=params)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"总考试数: {result['total']}")
            print("考试列表:")
            for exam in result['items']:
                print(f"  - {exam['exam_name']} ({exam['exam_date']}) - 总分: {exam['total_score']} - 等级: {exam['overall_level']}")
        else:
            print(f"获取考试列表失败: {response.text}")
            
    except Exception as e:
        print(f"请求出错: {e}")

def test_health_check():
    """测试健康检查接口"""
    print("=== 测试健康检查 ===")
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"服务状态: {result['status']}")
        else:
            print("健康检查失败")
            
    except requests.exceptions.ConnectionError:
        print("连接失败，请确保API服务已启动")
    except Exception as e:
        print(f"请求出错: {e}")

def test_api_docs():
    """测试API文档访问"""
    print("\n=== API文档地址 ===")
    print(f"Swagger UI: {BASE_URL}/docs")
    print(f"ReDoc: {BASE_URL}/redoc")
    print(f"OpenAPI JSON: {BASE_URL}/openapi.json")

def main():
    """主测试函数"""
    print("学生考试分析小程序 API 测试脚本")
    print("=" * 50)
    
    # 测试健康检查
    test_health_check()
    
    # 测试登录
    token = test_login()
    
    # 测试获取考试列表
    test_get_exams(token)
    
    # 显示API文档地址
    test_api_docs()
    
    print("\n测试完成!")

if __name__ == "__main__":
    main() 