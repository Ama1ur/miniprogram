# 贡献指南

感谢您对成绩报告小程序项目的关注！我们欢迎任何形式的贡献。

## 🤝 如何贡献

### 报告问题

如果您发现了bug或有功能建议，请：

1. 在[Issues](https://github.com/yourusername/miniprogram-score-report/issues)中搜索是否已有相关问题
2. 如果没有，请创建新的Issue
3. 详细描述问题或建议，包括：
   - 问题的具体表现
   - 复现步骤
   - 期望的行为
   - 环境信息（微信版本、系统版本等）

### 提交代码

1. **Fork项目**
   ```bash
   # 点击页面右上角的Fork按钮
   ```

2. **克隆到本地**
   ```bash
   git clone https://github.com/yourusername/miniprogram-score-report.git
   cd miniprogram-score-report
   ```

3. **创建分支**
   ```bash
   git checkout -b feature/your-feature-name
   # 或
   git checkout -b fix/your-bug-fix
   ```

4. **安装依赖**
   ```bash
   npm install
   ```

5. **进行开发**
   - 遵循代码规范
   - 添加必要的测试
   - 更新相关文档

6. **提交代码**
   ```bash
   git add .
   git commit -m "feat: 添加新功能描述"
   # 或
   git commit -m "fix: 修复问题描述"
   ```

7. **推送到远程**
   ```bash
   git push origin feature/your-feature-name
   ```

8. **创建Pull Request**
   - 在GitHub上点击"New Pull Request"
   - 详细描述您的修改
   - 等待代码审查

## 📝 代码规范

### 命名规范

- **文件命名**: 使用小写字母和连字符，如`user-profile.js`
- **变量命名**: 使用驼峰命名法，如`userInfo`
- **常量命名**: 使用大写字母和下划线，如`API_BASE_URL`
- **组件命名**: 使用PascalCase，如`UserProfile`

### 代码风格

```javascript
// ✅ 好的例子
const getUserInfo = async (userId) => {
  try {
    const response = await api.getUser(userId);
    return response.data;
  } catch (error) {
    console.error('获取用户信息失败:', error);
    throw error;
  }
};

// ❌ 不好的例子
function getUserInfo(userId){
    return api.getUser(userId).then(res=>{
        return res.data
    }).catch(err=>{
        console.log(err)
    })
}
```

### 注释规范

```javascript
/**
 * 获取用户成绩信息
 * @param {string} userId - 用户ID
 * @param {string} examId - 考试ID
 * @returns {Promise<Object>} 返回成绩数据
 */
const getUserScore = async (userId, examId) => {
  // 实现代码...
};
```

## 🧪 测试

在提交代码前，请确保：

1. **运行测试**
   ```bash
   npm test
   ```

2. **代码检查**
   ```bash
   npm run lint
   ```

3. **功能测试**
   - 在微信开发者工具中测试所有功能
   - 确保在不同设备上正常运行

## 📋 提交信息规范

使用[约定式提交](https://www.conventionalcommits.org/zh-hans/)格式：

```
<类型>[可选的作用域]: <描述>

[可选的正文]

[可选的脚注]
```

### 类型说明

- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档更新
- `style`: 代码格式调整（不影响功能）
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建过程或辅助工具的变动

### 示例

```
feat(student): 添加成绩趋势图表功能

- 实现趋势图组件
- 添加数据筛选功能
- 支持多科目切换

Closes #123
```

## 🎯 开发流程

### 功能开发

1. **需求分析**: 明确功能需求和用户场景
2. **设计方案**: 考虑技术实现和用户体验
3. **编写代码**: 遵循代码规范和最佳实践
4. **单元测试**: 编写测试用例确保功能正确
5. **集成测试**: 在完整环境中测试功能
6. **文档更新**: 更新相关文档和使用说明
7. **代码审查**: 提交Pull Request等待审查

### Bug修复

1. **问题重现**: 确认bug的存在和影响范围
2. **根因分析**: 分析问题产生的原因
3. **制定方案**: 设计修复方案
4. **实施修复**: 编写修复代码
5. **测试验证**: 确保问题已解决且未引入新问题
6. **回归测试**: 测试相关功能确保正常

## 📞 联系我们

如果您有任何问题或建议，请通过以下方式联系：

- **Issues**: [GitHub Issues](https://github.com/yourusername/miniprogram-score-report/issues)
- **邮箱**: your.email@example.com
- **微信群**: 扫码加入开发者群

## 🙏 致谢

感谢所有贡献者的支持和参与！

[![Contributors](https://contrib.rocks/image?repo=yourusername/miniprogram-score-report)](https://github.com/yourusername/miniprogram-score-report/graphs/contributors) 