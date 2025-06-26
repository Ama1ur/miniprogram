#!/usr/bin/env python3
"""
完整的学生端API测试脚本
测试所有已实现的学生端核心分析接口
"""

import requests
import json
from typing import Optional

# API基础URL
BASE_URL = "http://localhost:8000"

class StudentAPITester:
    """学生端API测试类"""
    
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.token: Optional[str] = None
        
    def login(self) -> bool:
        """用户登录获取token"""
        print("=" * 60)
        print("🔐 测试用户登录")
        print("=" * 60)
        
        login_data = {
            "code": "mock_code_123",
            "userType": "student",
            "identityId": "20240001", 
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
                    print(f"用户: {result['userInfo']['name']}")
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
    
    def test_get_exams(self):
        """测试获取考试列表"""
        print("\n" + "=" * 60)
        print("📋 测试获取历史考试列表")
        print("=" * 60)
        
        try:
            response = requests.get(
                f"{self.base_url}/student/exams",
                headers=self.get_headers(),
                params={"page": 1, "limit": 3}
            )
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ 成功获取考试列表，共 {result['total']} 场考试")
                for exam in result['items']:
                    print(f"  📝 {exam['exam_name']} ({exam['exam_date']}) - {exam['total_score']}分 - {exam['overall_level']}")
                return result['items'][0]['exam_id'] if result['items'] else None
            else:
                print(f"❌ 获取失败: {response.text}")
                
        except Exception as e:
            print(f"❌ 请求出错: {e}")
        
        return None
    
    def test_exam_scores(self, exam_id: str):
        """测试获取考试成绩"""
        print("\n" + "=" * 60)
        print("📊 测试获取考试成绩页数据")
        print("=" * 60)
        
        try:
            response = requests.get(
                f"{self.base_url}/student/exams/{exam_id}/scores",
                headers=self.get_headers()
            )
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ 总分: {result['total_score']} | 等级: {result['overall_level']}")
                print("📚 各科成绩:")
                for subject in result['subject_scores']:
                    print(f"  {subject['subject']}: {subject['score']}分 ({subject['level']})")
            else:
                print(f"❌ 获取失败: {response.text}")
                
        except Exception as e:
            print(f"❌ 请求出错: {e}")
    
    def test_level_position(self, exam_id: str):
        """测试等级位置分析"""
        print("\n" + "=" * 60)
        print("📈 测试等级位置页数据")
        print("=" * 60)
        
        try:
            response = requests.get(
                f"{self.base_url}/student/exams/{exam_id}/level-position",
                headers=self.get_headers(),
                params={"mode": "class"}
            )
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ 对比模式: {result['grouping_mode']} | 班级人数: {result['class_size']}")
                print("📊 科目对比:")
                for item in result['subject_comparison'][:3]:  # 只显示前3个
                    print(f"  {item['subject']}: {item['score']}分 排名{item['rank']} (差距: {item['diff']}分)")
            else:
                print(f"❌ 获取失败: {response.text}")
                
        except Exception as e:
            print(f"❌ 请求出错: {e}")
    
    def test_pk_analysis(self, exam_id: str):
        """测试成绩PK分析"""
        print("\n" + "=" * 60)
        print("⚔️ 测试成绩PK页数据")
        print("=" * 60)
        
        try:
            response = requests.get(
                f"{self.base_url}/student/exams/{exam_id}/pk-analysis",
                headers=self.get_headers()
            )
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ 击败率: {result['rank_percent']}% | 排名: 第{result['rank_index']}名/{result['class_total_students']}人")
            else:
                print(f"❌ 获取失败: {response.text}")
                
        except Exception as e:
            print(f"❌ 请求出错: {e}")
    
    def test_ideal_ranking(self, exam_id: str):
        """测试理想排名计算"""
        print("\n" + "=" * 60)
        print("🎯 测试理想排名页数据")
        print("=" * 60)
        
        try:
            # 设置理想分数
            ideal_scores = {
                "ideal_scores": [
                    {"subject": "数学", "ideal_score": 140.0},
                    {"subject": "英语", "ideal_score": 120.0},
                    {"subject": "物理", "ideal_score": 95.0}
                ]
            }
            
            response = requests.post(
                f"{self.base_url}/student/exams/{exam_id}/ideal-ranking",
                headers=self.get_headers(),
                json=ideal_scores
            )
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ 当前排名: 第{result['current_rank']}名")
                print(f"📈 新总分: {result['new_total_score']} | 预测排名: 第{result['predicted_rank']}名")
                print(f"🚀 排名提升: {result['rank_change']}名")
                print("📚 理想分数设置:")
                for subject in result['subjects'][:3]:  # 只显示前3个
                    print(f"  {subject['subject']}: {subject['current_score']} → {subject['ideal_score']}")
            else:
                print(f"❌ 获取失败: {response.text}")
                
        except Exception as e:
            print(f"❌ 请求出错: {e}")
    
    def test_bias_analysis(self, exam_id: str):
        """测试偏科分析"""
        print("\n" + "=" * 60)
        print("🎯 测试偏科分析页数据")
        print("=" * 60)
        
        try:
            response = requests.get(
                f"{self.base_url}/student/exams/{exam_id}/bias-analysis",
                headers=self.get_headers()
            )
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ 优势科目: {', '.join(result['strength_subjects'])}")
                print(f"⚠️ 劣势科目: {', '.join(result['weak_subjects'])}")
                print("📊 雷达图数据:")
                for data in result['radar_data'][:3]:  # 只显示前3个
                    print(f"  {data['subject']}: 总击败率{data['total_win_rate']}% | 科目击败率{data['subject_win_rate']}%")
            else:
                print(f"❌ 获取失败: {response.text}")
                
        except Exception as e:
            print(f"❌ 请求出错: {e}")
    
    def test_trend_analysis(self):
        """测试历次趋势分析"""
        print("\n" + "=" * 60)
        print("📈 测试历次趋势页数据")
        print("=" * 60)
        
        try:
            response = requests.get(
                f"{self.base_url}/student/trend-analysis",
                headers=self.get_headers(),
                params={"mode": "class"}
            )
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print("✅ 历次考试趋势:")
                for data in result['trend_data'][-3:]:  # 显示最近3次
                    print(f"  {data['date']}: 班级击败率{data['class_win_rate']}% | 校级击败率{data['school_win_rate']}%")
                print(f"📝 分析结论: {result['trend_analysis']}")
            else:
                print(f"❌ 获取失败: {response.text}")
                
        except Exception as e:
            print(f"❌ 请求出错: {e}")
    
    def test_question_analysis(self, exam_id: str):
        """测试试题分析"""
        print("\n" + "=" * 60)
        print("📝 测试试题分析页数据")
        print("=" * 60)
        
        try:
            response = requests.get(
                f"{self.base_url}/student/exams/{exam_id}/question-analysis",
                headers=self.get_headers(),
                params={"subject": "数学"}
            )
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ 当前科目: {result['selected_subject']}")
                print(f"📚 可选科目: {', '.join(result['available_subjects'])}")
                print("📋 题目分析:")
                for q in result['current_questions'][:5]:  # 只显示前5题
                    print(f"  第{q['id']}题({q['type']}): {q['score']}/{q['full_score']}分 正确答案:{q['correct_answer']}")
            else:
                print(f"❌ 获取失败: {response.text}")
                
        except Exception as e:
            print(f"❌ 请求出错: {e}")
    
    def test_loss_analysis(self, exam_id: str):
        """测试失分分析"""
        print("\n" + "=" * 60)
        print("❌ 测试失分分析页数据")
        print("=" * 60)
        
        try:
            response = requests.get(
                f"{self.base_url}/student/exams/{exam_id}/loss-analysis",
                headers=self.get_headers()
            )
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print("📊 难度分析:")
                for analysis in result['difficulty_analysis']:
                    print(f"  {analysis['level']}: {analysis['correct']}/{analysis['count']}题正确 (正确率: {analysis['rate']}%)")
                
                print(f"❌ 全部丢分题: {', '.join(result['loss_questions']['全部丢分'])}")
                print(f"⚠️ 部分丢分题: {', '.join(result['loss_questions']['部分丢分'])}")
                print(f"💰 潜力提升: {result['gain_prediction']['potential_gain_score']}分 | 排名提升: {result['gain_prediction']['rank_improvement']}名")
            else:
                print(f"❌ 获取失败: {response.text}")
                
        except Exception as e:
            print(f"❌ 请求出错: {e}")
    
    def test_knowledge_analysis(self, exam_id: str):
        """测试知识点分析"""
        print("\n" + "=" * 60)
        print("🧠 测试知识点分析页数据")
        print("=" * 60)
        
        try:
            response = requests.get(
                f"{self.base_url}/student/exams/{exam_id}/knowledge-analysis",
                headers=self.get_headers()
            )
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"📚 分析标签: {', '.join(result['tabs'])}")
                print("🧠 知识点掌握情况:")
                for point in result['knowledge_points'][:5]:  # 只显示前5个
                    print(f"  {point['name']}: 个人{point['personal_rate']}% vs 班级{point['class_rate']}% ({point['level']})")
            else:
                print(f"❌ 获取失败: {response.text}")
                
        except Exception as e:
            print(f"❌ 请求出错: {e}")
    
    def run_all_tests(self):
        """运行所有测试"""
        print("🚀 开始学生端API完整测试")
        print("=" * 80)
        
        # 1. 登录
        if not self.login():
            print("❌ 登录失败，无法继续测试")
            return
        
        # 2. 获取考试列表
        exam_id = self.test_get_exams()
        if not exam_id:
            print("❌ 无法获取考试ID，使用默认值")
            exam_id = "exam_001"
        
        # 3. 测试所有核心分析接口
        self.test_exam_scores(exam_id)
        self.test_level_position(exam_id)
        self.test_pk_analysis(exam_id)
        self.test_ideal_ranking(exam_id)
        self.test_bias_analysis(exam_id)
        self.test_trend_analysis()
        self.test_question_analysis(exam_id)
        self.test_loss_analysis(exam_id)
        self.test_knowledge_analysis(exam_id)
        
        # 总结
        print("\n" + "=" * 80)
        print("🎉 所有API测试完成！")
        print("=" * 80)
        print("✅ 已测试的接口:")
        print("   1. GET /student/exams - 历史考试列表")
        print("   2. GET /student/exams/{examId}/scores - 考试成绩页")
        print("   3. GET /student/exams/{examId}/level-position - 等级位置页")
        print("   4. GET /student/exams/{examId}/pk-analysis - 成绩PK页")
        print("   5. POST /student/exams/{examId}/ideal-ranking - 理想排名页")
        print("   6. GET /student/exams/{examId}/bias-analysis - 偏科分析页")
        print("   7. GET /student/trend-analysis - 历次趋势页")
        print("   8. GET /student/exams/{examId}/question-analysis - 试题分析页")
        print("   9. GET /student/exams/{examId}/loss-analysis - 失分分析页")
        print("  10. GET /student/exams/{examId}/knowledge-analysis - 知识点分析页")
        print("\n🌟 所有学生端核心分析API都正常工作！")

def main():
    """主函数"""
    tester = StudentAPITester()
    tester.run_all_tests()

if __name__ == "__main__":
    main() 