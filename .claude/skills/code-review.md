# Code Review Skill

## 描述
对代码进行全面的代码审核，检查代码质量、安全性、性能、可维护性等方面。

## 使用场景
- 审核新提交的代码
- 审核特定功能模块
- 审核整体代码架构
- 审核特定问题（安全、性能等）

## 参数
- `scope`: 审核范围（可选）
  - `all`: 全面审核（默认）
  - `security`: 仅安全审核
  - `performance`: 仅性能审核
  - `quality`: 仅代码质量审核
  - `architecture`: 仅架构审核

- `files`: 指定审核的文件或目录（可选）
  - 例如：`notification.py` 或 `data_provider/`

## 审核检查项

### 1. 代码质量 (Code Quality)
- [x] 命名规范（变量、函数、类名）
- [x] 代码格式（缩进、空行、行长）
- [x] 注释完整性（函数文档、行内注释）
- [x] 类型提示（Type Hints）
- [x] 代码复杂度（圈复杂度、嵌套层级）
- [x] 魔法数字和字符串（应使用常量）
- [x] 重复代码（DRY 原则）

### 2. 安全性 (Security)
- [x] SQL 注入风险
- [x] XSS 风险（Web 应用）
- [x] 命令注入风险
- [x] **敏感信息泄露（密码、Token、API Key）**
- [x] **硬编码的凭证或密钥**
- [x] **代码中的真实 Token/Key 检测**
- [x] 不安全的随机数生成
- [x] 依赖库漏洞
- [x] 文件路径遍历风险

### 3. 性能 (Performance)
- [x] 数据库查询效率（N+1 问题）
- [x] 循环效率（不必要的嵌套循环）
- [x] 内存泄漏风险
- [x] 缓存使用
- [x] 并发处理
- [x] 大数据集处理
- [x] API 调用优化

### 4. 错误处理 (Error Handling)
- [x] 异常捕获完整性
- [x] 错误日志记录
- [x] 用户友好的错误提示
- [x] 资源清理（with 语句）
- [x] 降级策略

### 5. 架构设计 (Architecture)
- [x] 模块化程度
- [x] 职责分离（单一职责原则）
- [x] 依赖管理
- [x] 接口设计
- [x] 可扩展性
- [x] 配置管理

### 6. 测试覆盖 (Testing)
- [x] 单元测试存在性
- [x] 测试覆盖率
- [x] 边界条件测试
- [x] 异常情况测试

### 7. 文档 (Documentation)
- [x] README 完整性
- [x] API 文档
- [x] 注释清晰度
- [x] 示例代码

## 输出格式

```markdown
## 📊 代码审核报告

### 基本信息
- 审核范围: [范围]
- 审核文件: [文件列表]
- 审核时间: [时间戳]

### 审核结果摘要
- 总体评分: ⭐⭐⭐⭐☆ (X/5)
- 严重问题: X 个
- 警告问题: X 个
- 建议优化: X 个

### 详细问题列表

#### 🔴 严重问题 (Critical)
1. **[问题标题]**
   - 文件: `file.py:123`
   - 严重性: 高/中/低
   - 描述: [问题描述]
   - 影响: [影响范围]
   - 建议: [修复建议]

#### ⚠️ 警告问题 (Warning)
[同样格式]

#### 💡 优化建议 (Suggestion)
[同样格式]

### 优点总结
✅ [优点1]
✅ [优点2]

### 改进建议优先级
1. [P0 - 立即修复] [问题]
2. [P1 - 尽快修复] [问题]
3. [P2 - 逐步改进] [问题]

### 最佳实践推荐
- [推荐1]
- [推荐2]
```

## 审核流程

1. **收集信息**
   - 读取指定文件/目录
   - 分析代码结构
   - 识别关键模块

2. **执行检查**
   - 按照检查项逐一审核
   - 记录发现的问题
   - 评估严重程度

3. **生成报告**
   - 汇总审核结果
   - 提供修复建议
   - 给出优先级排序

4. **优化建议**
   - 推荐最佳实践
   - 提供改进方案
   - 参考行业标准

## 使用示例

```
用户: 审核 notification.py 的代码质量
用户: 审核最近修改的安全性问题
用户: 审核整个项目的架构设计
用户: 审核 data_provider/ 目录的性能问题
```

## 评分标准

- ⭐⭐⭐⭐⭐ (5/5): 优秀，无重大问题
- ⭐⭐⭐⭐☆ (4/5): 良好，有少量改进空间
- ⭐⭐⭐☆☆ (3/5): 一般，存在一些问题
- ⭐⭐☆☆☆ (2/5): 较差，存在较多问题
- ⭐☆☆☆☆ (1/5): 差，存在严重问题

## 特殊检查

### Python 特定
- PEP 8 规范遵守
- Type Hints 使用
- Docstring 格式（Google/NumPy）
- 虚拟环境隔离
- requirements.txt 管理

### 数据库相关
- ORM 使用正确性
- 事务处理
- 连接池管理
- 索引优化

### API 相关
- RESTful 规范
- 错误码规范
- 版本管理
- 限流控制

### 配置管理
- 敏感信息隔离
- 环境变量使用
- 配置文件结构
- 默认值合理性

## 敏感信息检测 (Security & Secrets Detection)

**必须检查的敏感信息类型：**

### 1. API Keys 和 Tokens
```python
# ❌ 严重问题：硬编码的 API Key
def send_notification():
    api_key = "sk-1234567890abcdef"  # 真实密钥
    headers = {"Authorization": f"Bearer {api_key}"}
    requests.post(url, headers=headers)

# ✅ 正确：使用环境变量
def send_notification():
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("API_KEY not configured")
    headers = {"Authorization": f"Bearer {api_key}"}
    requests.post(url, headers=headers)
```

### 2. 数据库凭证
```python
# ❌ 严重问题：硬编码的数据库密码
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "MySecretPassword123",  # 真实密码
    "database": "mydb"
}

# ✅ 正确：从环境变量读取
db_config = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}
```

### 3. 第三方服务凭证
```python
# ❌ 严重问题：硬编码的第三方 Token
PUSHPLUS_TOKEN = "32793335f3874de8ad06dac8b2c6f676"  # 真实Token
WECHAT_WEBHOOK = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=abc123def456"

# ✅ 正确：使用配置文件
PUSHPLUS_TOKEN = os.getenv("PUSHPLUS_TOKEN")
WECHAT_WEBHOOK = os.getenv("WECHAT_WEBHOOK_URL")
```

### 4. 加密密钥和盐值
```python
# ❌ 严重问题：硬编码的密钥
SECRET_KEY = "supersecretkey12345"
ENCRYPTION_SALT = "fixedsaltvalue"

# ✅ 正确：从安全配置读取
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY or len(SECRET_KEY) < 32:
    raise ValueError("SECRET_KEY must be at least 32 characters")
```

### 常见敏感信息模式

**检测规则（正则表达式）：**
- API Key: `(?:api[_-]?key|apikey|api_key)\s*[:=]\s*['"]([a-zA-Z0-9]{20,})['"]`
- Token: `(?:token|access_token|auth_token)\s*[:=]\s*['"]([a-zA-Z0-9]{20,})['"]`
- 密码: `(?:password|passwd|pwd)\s*[:=]\s*['"]([^'"]{6,})['"]`
- Webhook: `https?://[^\s'"]+key[=]([a-zA-Z0-9]{20,})`
- Base64 编码的密钥: `['"]([A-Za-z0-9+/]{32,}={0,2})['"]`

**高风险文件：**
- 配置文件：`.env`, `config.py`, `settings.py`
- 测试文件：`test_*.py`, `*_test.py`
- 初始化文件：`__init__.py`, `bootstrap.py`
- 数据库迁移文件
- CI/CD 配置文件

**检查方法：**
1. 搜索常见敏感信息关键词
2. 检查硬编码的长字符串（>20字符）
3. 检查 URL 参数中的敏感信息
4. 验证是否使用环境变量
5. 检查配置文件是否被提交到版本控制

**报告格式：**
```markdown
#### 🔴 严重问题：敏感信息泄露
1. **硬编码的 API Token** (test_env.py:526)
   ```python
   test_pushplus('32793335f3874de8ad06dac8b2c6f676')
   ```
   - 风险等级：🔴 严重
   - 影响：Token 泄露到代码仓库，可能导致未授权访问
   - 检测到：32位十六进制字符串（可能是 Token）
   - 建议：
     1. 立即撤销此 Token
     2. 从代码中移除，使用环境变量或命令行参数
     3. 检查 Git 历史记录，考虑清理
     4. 将此文件添加到 .gitignore（如包含敏感信息）
```

## 注意事项

- 审核时注意上下文，不要过度优化
- 平衡代码质量和开发效率
- 考虑团队技术栈和习惯
- 提供建设性意见，而非批评
- 优先关注严重问题和安全隐患
