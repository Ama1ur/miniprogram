# 成绩报告 - 微信小程序

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![WeChat](https://img.shields.io/badge/WeChat-MiniProgram-brightgreen.svg)](https://developers.weixin.qq.com/miniprogram/dev/framework/)
[![TDesign](https://img.shields.io/badge/UI-TDesign-orange.svg)](https://tdesign.tencent.com/miniprogram/overview)

> 一个现代化的学生成绩查询与分析微信小程序，支持学生端和教师端双重角色。

## 📋 项目概述

成绩报告小程序是一个基于微信小程序的教育信息化工具，旨在为学生、教师和家长提供便捷的成绩查询、分析和管理服务。通过数据可视化和智能分析，帮助用户更好地了解学习情况和教学效果。

### 🎯 核心价值

- **便捷性**: 基于微信生态，免安装、易访问
- **即时性**: 成绩发布后实时通知推送
- **数据化**: 多维度数据分析图表
- **安全性**: 严格的身份认证和权限控制

## ✨ 功能特性

### 🎓 学生端功能

- **📊 成绩查询**: 查看个人历史考试成绩
- **📈 趋势分析**: 各科目成绩变化趋势图表
- **🎯 学情分析**: 个人学习情况深度分析
- **📝 答题卡查看**: 在线查看考试答题卡
- **🏆 排名对比**: 班级、年级排名对比
- **🔍 知识点分析**: 掌握情况分析
- **💡 提升建议**: 智能学习建议

### 👨‍🏫 教师端功能

- **📋 班级管理**: 多班级切换管理
- **📊 成绩统计**: 班级整体成绩分析
- **🔍 学生查询**: 快速查找学生成绩
- **📈 数据分析**: 班级学情分析报告
- **📊 可视化图表**: 多种图表展示数据

### 🔒 付费高级功能

- **🎯 偏科分析**: 雷达图展示各科优劣势
- **📈 历次趋势**: 成绩变化趋势分析
- **🎯 理想排名**: 目标分数分析
- **❌ 失分分析**: 答题情况深度分析
- **📚 知识点诊断**: 详细知识点掌握情况

## 🛠 技术栈

### 前端技术
- **微信小程序**: 基础框架
- **TDesign**: 腾讯设计语言UI组件库
- **F2**: 蚂蚁金服数据可视化图表库
- **Canvas 2D**: 高性能图表渲染

### 开发工具
- **微信开发者工具**: 主要开发环境
- **Node.js**: 依赖管理
- **npm**: 包管理工具

## 🚀 快速开始

### 环境要求

- **微信开发者工具**: 最新版本
- **Node.js**: >= 14.0.0
- **npm**: >= 6.0.0

### 安装步骤

1. **克隆项目**
```bash
git clone https://github.com/yourusername/miniprogram-score-report.git
cd miniprogram-score-report
```

2. **安装依赖**
```bash
npm install
```

3. **打开项目**
   - 启动微信开发者工具
   - 选择"导入项目"
   - 选择项目根目录
   - 填写AppID（测试可使用测试号）

4. **构建npm包**
   - 在微信开发者工具中点击"工具" → "构建npm"
   - 等待构建完成

5. **运行项目**
   - 点击"编译"按钮
   - 在模拟器中查看效果

## 📖 使用指南

### 学生使用流程

1. **首次登录**
   - 微信授权登录
   - 选择"我是学生"
   - 输入学号和密码进行绑定

2. **查看成绩**
   - 在首页查看最新考试成绩
   - 点击历史考试查看详细成绩
   - 查看各科目得分和排名

3. **解锁高级功能**
   - 点击"解锁学情分析"
   - 支付9.9元解锁完整功能
   - 享受专业数据分析服务

### 教师使用流程

1. **登录绑定**
   - 微信授权登录
   - 选择"我是教师"
   - 输入工号和密码

2. **班级管理**
   - 选择要管理的班级
   - 查看班级整体成绩
   - 搜索特定学生成绩

3. **数据分析**
   - 查看班级平均分、及格率
   - 分析成绩分布情况
   - 导出成绩报告

## 📁 项目结构

```
miniprogram-2/
├── app.js                 # 小程序主入口
├── app.json              # 全局配置
├── app.wxss              # 全局样式
├── components/           # 自定义组件
│   └── f2-canvas/       # 图表组件
├── pages/               # 页面文件
│   ├── index/          # 首页
│   ├── login/          # 登录页
│   ├── common/         # 公共页面
│   ├── student/        # 学生端页面
│   │   ├── analysis.js    # 学情分析逻辑
│   │   ├── analysis.wxml  # 分析页面结构
│   │   ├── analysis.wxss  # 分析页面样式
│   │   ├── home.js        # 学生首页
│   │   └── detail.js      # 成绩详情
│   └── teacher/        # 教师端页面
├── miniprogram_npm/    # npm包
├── common/            # 公共资源
└── utils/            # 工具函数
```

## 🔧 开发指南

### 添加新页面

1. 在 `pages` 目录下创建新文件夹
2. 创建 `.js`, `.wxml`, `.wxss`, `.json` 四个文件
3. 在 `app.json` 中注册页面路径

### 使用图表组件

```javascript
// 在页面中引入图表配置
data: {
  chartOpts: {
    onInit: (canvas, width, height, F2) => {
      // 初始化图表逻辑
      const chart = new F2.Chart({
        el: canvas,
        width,
        height
      });
      // 配置图表...
      chart.render();
      return chart;
    }
  }
}
```

### 使用TDesign组件

```json
{
  "usingComponents": {
    "t-button": "tdesign-miniprogram/button/button",
    "t-cell": "tdesign-miniprogram/cell/cell"
  }
}
```

### 样式规范

- 使用 `rpx` 作为尺寸单位
- 遵循TDesign设计规范
- 保持良好的响应式设计

## 🎨 主题定制

项目使用TDesign主题系统，可以通过以下方式自定义主题：

1. **修改CSS变量**
```css
:root {
  --td-primary-color: #0052d9;
  --td-success-color: #00a870;
  --td-warning-color: #ed7b2f;
}
```

2. **自定义组件样式**
```css
.custom-button {
  background: linear-gradient(135deg, #0052d9 0%, #1890ff 100%);
  border-radius: 50rpx;
}
```

## 📱 功能截图

### 学生端界面
- 成绩首页
- 学情分析
- 趋势图表
- 知识点分析

### 教师端界面
- 班级管理
- 成绩统计
- 数据分析
- 学生查询

## 🚀 部署指南

### 小程序发布

1. **准备工作**
   - 注册微信小程序账号
   - 获取AppID和AppSecret
   - 配置服务器域名

2. **代码上传**
   - 在微信开发者工具中点击"上传"
   - 填写版本号和项目备注
   - 等待上传完成

3. **提交审核**
   - 登录微信公众平台
   - 选择"版本管理"
   - 提交审核并等待通过

4. **发布上线**
   - 审核通过后点击"发布"
   - 小程序正式上线

### 后端服务部署

如需完整功能，需要部署后端服务：

1. **数据库设计**
   - 用户表（学生、教师）
   - 成绩表
   - 考试表
   - 班级表

2. **API接口**
   - 用户认证接口
   - 成绩查询接口
   - 数据分析接口
   - 消息推送接口

## 🤝 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. **Fork 项目**
2. **创建特性分支** (`git checkout -b feature/AmazingFeature`)
3. **提交更改** (`git commit -m 'Add some AmazingFeature'`)
4. **推送到分支** (`git push origin feature/AmazingFeature`)
5. **创建Pull Request**

### 代码规范

- 使用ESLint进行代码检查
- 遵循JavaScript Standard Style
- 添加必要的注释
- 编写单元测试

## 📝 更新日志

### v1.0.0 (2024-01-20)
- ✨ 初始版本发布
- 🎓 学生端基础功能
- 👨‍🏫 教师端管理功能
- 📊 图表可视化
- 🔒 付费功能模块

### v1.1.0 (计划中)
- 🔔 消息推送功能
- 👨‍👩‍👧‍👦 家长端功能
- 📊 更多图表类型
- 🌙 深色模式支持

## ❓ 常见问题

### Q: 图表不显示怎么办？
A: 请检查Canvas 2D API是否正确初始化，确保F2库正确导入。

### Q: TDesign组件样式异常？
A: 请确保正确导入TDesign样式文件，检查CSS变量设置。

### Q: 如何自定义主题色？
A: 修改app.wxss中的CSS变量，或在具体页面中覆盖样式。

### Q: 付费功能如何测试？
A: 开发环境下可以使用resetPremiumStatus方法重置付费状态。

## 📄 许可证

本项目基于 [MIT License](LICENSE) 开源协议。

## 📞 联系我们

- **项目维护者**: [Your Name]
- **邮箱**: your.email@example.com
- **问题反馈**: [GitHub Issues](https://github.com/yourusername/miniprogram-score-report/issues)

## 🙏 致谢

感谢以下开源项目：

- [TDesign](https://tdesign.tencent.com/) - 企业级设计语言
- [F2](https://antv.vision/zh/f2/3.x) - 移动端可视化方案
- [微信小程序](https://developers.weixin.qq.com/miniprogram/dev/framework/) - 基础框架

---

⭐ 如果这个项目对你有帮助，请给它一个星标！ 