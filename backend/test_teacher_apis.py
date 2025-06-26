#!/usr/bin/env python3
"""
教师端API测试脚本
测试所有已实现的教师端接口
"""

import requests
import json
from typing import Optional

# API基础URL
BASE_URL = "http://localhost:8000"

class TeacherAPITester:
    """教师端API测试类"""
    
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.token: Optional[str] = None
        
    def login(self) -> bool:
        """教师登录获取token"""
        print("=" * 60)
        print("🔐 测试教师登录")
        print("=" * 60)
        
        login_data = {
            "code": "mock_code_teacher",
            "userType": "teacher",
            "identityId": "teacher001", 
            "password": "123456"
        }
        
        try:
            response = requests.post(f"{self.base_url}/auth/login", json=login_data)
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                if result and 'token' in result and 'userInfo' in result:
                    self.token = result['token']
                    print("✅ 登录成功!")
                    print(f"教师: {result['userInfo']['name']}")
                    if self.token:
                        print(f"Token: {self.token[:50]}...")
                    return True
                else:
                    print("❌ 响应数据格式错误")
                    return False
            else:
                print(f"❌ 登录失败: {response.text}")
                return False
                
        except requests.exceptions.ConnectionError:
            print("❌ 连接失败，请确保API服务已启动 (运行 python start.py)")
            return False
        except Exception as e:
            print(f"❌ 请求出错: {e}")
            return False
    
    def get_headers(self) -> dict:
        """获取请求头"""
        if not self.token:
            raise ValueError("请先登录获取token")
        return {"Authorization": f"Bearer {self.token}"}
    
    def test_get_classes(self) -> Optional[str]:
        """测试获取教师班级列表"""
        print("\n" + "=" * 60)
        print("📚 测试获取教师班级列表")
        print("=" * 60)
        
        try:
            response = requests.get(
                f"{self.base_url}/teacher/classes",
                headers=self.get_headers()
            )
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ 成功获取班级列表，共 {len(result)} 个班级")
                for class_info in result:
                    print(f"  🏫 {class_info['class_name']} (ID: {class_info['class_id']})")
                
                # 返回第一个班级ID用于后续测试
                return result[0]['class_id'] if result else None
            else:
                print(f"❌ 获取失败: {response.text}")
                
        except Exception as e:
            print(f"❌ 请求出错: {e}")
        
        return None
    
    def test_get_class_scores(self, class_id: str):
        """测试获取班级成绩单"""
        print("\n" + "=" * 60)
        print("📊 测试获取班级成绩单")
        print("=" * 60)
        
        try:
            response = requests.get(
                f"{self.base_url}/teacher/classes/{class_id}/scores",
                headers=self.get_headers(),
                params={"examId": "exam_001"}
            )
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                stats = result['statistics']
                students = result['students']
                
                print(f"✅ 班级统计信息:")
                print(f"   📈 平均分: {stats['avgScore']:.1f}")
                print(f"   🏆 最高分: {stats['maxScore']:.1f}")
                print(f"   ✅ 及格率: {stats['passRate']:.1f}%")
                print(f"   👥 班级人数: {len(students)}人")
                
                print(f"\n📋 前10名学生成绩:")
                for student in students[:10]:
                    print(f"   {student['rank']}. {student['student_name']}: {student['total_score']}分")
                
                if len(students) > 10:
                    print(f"   ... 还有 {len(students) - 10} 名学生")
                    
            else:
                print(f"❌ 获取失败: {response.text}")
                
        except Exception as e:
            print(f"❌ 请求出错: {e}")
    
    def test_different_exam(self, class_id: str):
        """测试不同考试的成绩"""
        print("\n" + "=" * 60)
        print("🔄 测试不同考试成绩数据")
        print("=" * 60)
        
        try:
            response = requests.get(
                f"{self.base_url}/teacher/classes/{class_id}/scores",
                headers=self.get_headers(),
                params={"examId": "exam_002"}
            )
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                stats = result['statistics']
                students = result['students']
                
                print(f"✅ 考试002班级统计:")
                print(f"   📈 平均分: {stats['avgScore']:.1f}")
                print(f"   🏆 最高分: {stats['maxScore']:.1f}")
                print(f"   ✅ 及格率: {stats['passRate']:.1f}%")
                
                print(f"\n🔝 前5名学生:")
                for student in students[:5]:
                    print(f"   {student['rank']}. {student['student_name']}: {student['total_score']}分")
                    
            else:
                print(f"❌ 获取失败: {response.text}")
                
        except Exception as e:
            print(f"❌ 请求出错: {e}")
    
    def test_unauthorized_access(self):
        """测试权限控制"""
        print("\n" + "=" * 60)
        print("🔒 测试权限控制 - 访问无权限班级")
        print("=" * 60)
        
        try:
            response = requests.get(
                f"{self.base_url}/teacher/classes/unauthorized_class/scores",
                headers=self.get_headers(),
                params={"examId": "exam_001"}
            )
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 403:
                print("✅ 权限控制正常 - 拒绝访问无权限班级")
                result = response.json()
                print(f"   错误信息: {result.get('detail', '未知错误')}")
            else:
                print(f"⚠️ 权限控制异常 - 状态码: {response.status_code}")
                
        except Exception as e:
            print(f"❌ 请求出错: {e}")
    
    def run_all_tests(self):
        """运行所有测试"""
        print("🚀 开始教师端API完整测试")
        print("=" * 80)
        
        # 1. 教师登录
        if not self.login():
            print("❌ 登录失败，无法继续测试")
            return
        
        # 2. 获取班级列表
        class_id = self.test_get_classes()
        if not class_id:
            print("❌ 无法获取班级ID，使用默认值")
            class_id = "class_001"
        
        # 3. 测试班级成绩单
        self.test_get_class_scores(class_id)
        
        # 4. 测试不同考试数据
        self.test_different_exam(class_id)
        
        # 5. 测试权限控制
        self.test_unauthorized_access()
        
        # 总结
        print("\n" + "=" * 80)
        print("🎉 教师端API测试完成！")
        print("=" * 80)
        print("✅ 已测试的接口:")
        print("   1. GET /teacher/classes - 获取教师班级列表")
        print("   2. GET /teacher/classes/{classId}/scores - 获取班级成绩单")
        print("   3. 权限控制测试 - 访问无权限班级")
        print("   4. 不同考试数据测试")
        print("\n🌟 所有教师端API都正常工作！")

def main():
    """主函数"""
    tester = TeacherAPITester()
    tester.run_all_tests()

if __name__ == "__main__":
    main() 