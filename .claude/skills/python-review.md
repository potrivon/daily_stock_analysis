# Python Code Review Skill

## 描述
专门审核 Python 代码的质量、安全性、性能和最佳实践。

## 使用方法
```
用户: 审核 <文件名> 的 Python 代码
用户: 检查 <模块名> 的代码质量
用户: 审核最近的修改（python 相关）
```

## 快速检查项

### 1. PEP 8 规范
```python
# ❌ 错误示例
def myfunction( x,y ):
    result=x+y
    return result

# ✅ 正确示例
def my_function(x: int, y: int) -> int:
    """计算两个数的和"""
    result = x + y
    return result
```

### 2. 类型提示 (Type Hints)
```python
# ❌ 缺少类型提示
def calculate(price, quantity):
    return price * quantity

# ✅ 完整类型提示
from typing import List, Dict, Optional

def calculate(price: float, quantity: int) -> float:
    """计算总价"""
    return price * quantity
```

### 3. 异常处理
```python
# ❌ 过于宽泛的异常捕获
try:
    do_something()
except:
    pass

# ✅ 精确的异常处理
try:
    do_something()
except ValueError as e:
    logger.error(f"值错误: {e}")
    raise
except Exception as e:
    logger.error(f"未知错误: {e}")
    raise
```

### 4. 资源管理
```python
# ❌ 未正确关闭资源
f = open('file.txt')
content = f.read()
f.close()

# ✅ 使用 with 语句
with open('file.txt', 'r', encoding='utf-8') as f:
    content = f.read()
```

### 5. 字符串格式化
```python
# ❌ 旧式格式化
name = "World"
print("Hello, %s" % name)

# ⚠️ format() 方法
print("Hello, {}".format(name))

# ✅ f-string (Python 3.6+)
print(f"Hello, {name}")
```

### 6. 列表和字典操作
```python
# ❌ 低效的列表拼接
result = []
for item in items:
    result = result + [process(item)]

# ✅ 使用列表推导式
result = [process(item) for item in items]

# ❌ 不必要的循环
squares = []
for i in range(10):
    squares.append(i ** 2)

# ✅ 列表推导式
squares = [i ** 2 for i in range(10)]
```

### 7. 配置和常量
```python
# ❌ 魔法数字
if price > 100:
    apply_discount()

# ✅ 使用常量
MIN_DISCOUNT_PRICE = 100
if price > MIN_DISCOUNT_PRICE:
    apply_discount()
```

### 8. 日志记录
```python
# ❌ 使用 print 调试
print(f"Processing item: {item}")
print(f"Error: {error}")

# ✅ 使用 logging 模块
import logging
logger = logging.getLogger(__name__)

logger.info(f"Processing item: {item}")
logger.error(f"Error: {error}", exc_info=True)
```

### 9. 类设计
```python
# ❌ 缺少文档字符串
class DataProcessor:
    def __init__(self, source):
        self.source = source

# ✅ 完整的类定义
class DataProcessor:
    """数据处理类

    负责从数据源读取、处理和保存数据。

    Attributes:
        source: 数据源路径
        data: 处理后的数据
    """

    def __init__(self, source: str) -> None:
        """初始化数据处理器

        Args:
            source: 数据源路径
        """
        self.source = source
        self.data: List[Dict] = []
```

### 10. 导入顺序
```python
# ❌ 导入顺序混乱
import sys
import os
from my_module import my_function
from datetime import datetime
import pandas as pd

# ✅ 标准导入顺序
# 1. 标准库
import os
import sys
from datetime import datetime

# 2. 第三方库
import pandas as pd
import requests

# 3. 本地模块
from my_module import my_function
```

## 常见问题检查清单

### 安全问题
- [ ] **硬编码密钥/Token**（严重安全风险）
- [ ] **敏感信息泄露到版本控制**
- [ ] **API Key 或密码明文存储**
- [ ] SQL 注入：使用参数化查询
- [ ] 硬编码密码：使用环境变量
- [ ] 不安全的 eval()：避免使用或限制上下文
- [ ] 路径遍历：验证和规范化路径
- [ ] XML/JSON 注入：使用安全的解析器

### 性能问题
- [ ] N+1 查询：使用 join 或批量查询
- [ ] 大内存占用：使用生成器或分块处理
- [ ] 重复计算：使用缓存（lru_cache）
- [ ] 全局解释器锁（GIL）：考虑多进程

### 代码质量
- [ ] 过长函数：拆分为小函数（< 50 行）
- [ ] 过深嵌套：使用早期返回
- [ ] 重复代码：提取为函数
- [ ] 注释过多：代码应自解释

### 错误处理
- [ ] 吞噬异常：记录并重新抛出
- [ ] 过于宽泛：捕获具体异常类型
- [ ] 缺少 finally：确保资源清理
- [ ] 错误信息丢失：保留原始异常

## 审核输出模板

```markdown
## 🐍 Python 代码审核报告

### 文件: `filename.py`

#### ✅ 优点
- 使用了类型提示
- 异常处理完善
- 代码格式符合 PEP 8

#### 🔴 严重问题
1. **SQL 注入风险** (Line: 45)
   ```python
   query = f"SELECT * FROM users WHERE name = '{name}'"
   ```
   **建议**: 使用参数化查询
   ```python
   cursor.execute("SELECT * FROM users WHERE name = %s", (name,))
   ```

#### ⚠️ 警告
1. **缺少文档字符串** (Line: 78)
   函数 `process_data()` 缺少 docstring
   **建议**: 添加 Google 风格的 docstring

#### 💡 优化建议
1. **使用列表推导式** (Line: 123)
   当前代码可以使用列表推导式简化
   ```python
   # Before
   result = []
   for item in items:
       result.append(item * 2)
   # After
   result = [item * 2 for item in items]
   ```

#### 📊 代码指标
- 圈复杂度: 8（建议 < 10）
- 函数平均长度: 25 行
- 类型提示覆盖率: 85%
- 测试覆盖率: 未知（建议添加）

### 总结
- 评分: ⭐⭐⭐⭐☆ (4/5)
- 主要问题: SQL 注入风险
- 改进方向: 增强安全性、添加测试
```

## Python 特定工具推荐

### 代码格式化
- **Black**: 自动代码格式化
- **isort**: 导入排序
- **autopep8**: PEP 8 自动修复

### 代码检查
- **Pylint**: 全面的代码分析
- **Flake8**: PEP 8 检查
- **mypy**: 静态类型检查
- **Bandit**: 安全问题检查

### 测试工具
- **pytest**: 测试框架
- **pytest-cov**: 覆盖率报告
- **unittest**: 标准库测试框架

### 文档生成
- **Sphinx**: 文档生成
- **pydoc**: 内置文档工具

### 安全扫描工具
- **Bandit**: Python 安全漏洞扫描
- **Safety**: 依赖包安全检查
- **git-secrets**: Git 敏感信息检测
- **truffleHog**: 密钥和证书扫描

## 敏感信息检测（Python 代码）

### 常见硬编码密钥模式

```python
# ❌ 严重问题：测试函数中的硬编码 Token
def test_pushplus():
    # 不要这样做！Token 会泄露到版本控制
    token = "32793335f3874de8ad06dac8b2c6f676"
    send_test_message(token)

# ✅ 正确做法1：使用环境变量
def test_pushplus():
    token = os.getenv("TEST_PUSHPLUS_TOKEN")
    if not token:
        pytest.skip("TEST_PUSHPLUS_TOKEN not configured")
    send_test_message(token)

# ✅ 正确做法2：使用命令行参数
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--token', help='PushPlus Token')
    args = parser.parse_args()
    test_pushplus(args.token)
```

### 检测硬编码凭证的技巧

**1. 搜索长字符串（可能是密钥）**
```bash
# 搜索 20+ 字符的字符串
grep -rE '"[A-Za-z0-9]{20,}"' *.py
grep -rE "'[A-Za-z0-9]{20,}'" *.py
```

**2. 搜索常见密钥关键词**
```bash
grep -rE "(api_key|apikey|token|secret|password|passwd)" *.py
```

**3. 检查 URL 参数中的密钥**
```python
# ❌ 错误：URL 中包含密钥
WEBHOOK_URL = "https://api.example.com/hook?token=abc123def456"

# ✅ 正确：使用环境变量
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
# 或
WEBHOOK_URL = f"https://api.example.com/hook?token={os.getenv('WEBHOOK_TOKEN')}"
```

**4. 检查配置文件**
```python
# ❌ 错误：config.py 中硬编码
class Config:
    SECRET_KEY = "supersecretkey12345"
    DB_PASSWORD = "mypassword"

# ✅ 正确：从环境变量读取
class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    DB_PASSWORD = os.getenv("DB_PASSWORD")

    def __init__(self):
        if not self.SECRET_KEY:
            raise ValueError("SECRET_KEY must be configured")
```

### 真实案例对比

#### 案例 1：PushPlus Token 泄露
```python
# ❌ 代码审查发现的问题（test_env.py:526）
def main():
    test_pushplus('32793335f3874de8ad06dac8b2c6f676')  # 真实Token！

# 🔴 审核发现：
# - 位置：test_env.py:526
# - 问题：硬编码 32 位十六进制 Token
# - 风险：Token 已暴露在代码仓库中
# - 影响：任何能访问代码的人都能使用此 Token
# - 修复：恢复命令行参数支持，使用 --pushplus <token>

# ✅ 修复后的代码
def main():
    parser.add_argument('--pushplus', nargs='?', const='', metavar='TOKEN')
    args = parser.parse_args()
    token = args.pushplus if args.pushplus else None
    test_pushplus(token)
```

#### 案例 2：数据库密码泄露
```python
# ❌ 错误示例
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydb',
        'USER': 'postgres',
        'PASSWORD': 'Sup3rS3cr3t!',  # 硬编码密码
        'HOST': 'localhost',
    }
}

# ✅ 正确示例
import os
from dotenv import load_dotenv

load_dotenv()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),  # 从环境变量读取
        'HOST': os.getenv('DB_HOST', 'localhost'),
    }
}
```

### 敏感信息检测清单

审核代码时，检查以下位置：

- [ ] 测试文件（`test_*.py`）中的硬编码值
- [ ] 配置文件（`config.py`, `settings.py`）中的密钥
- [ ] 函数默认参数中的敏感值
- [ ] 类属性中的凭证
- [ ] URL 参数中的 key/token
- [ ] 字典/列表中的密码或密钥
- [ ] 常量定义中的 SECRET/TOKEN/PASSWORD

### 自动检测脚本

```python
import re
import os

def detect_secrets(file_path):
    """检测 Python 文件中的敏感信息"""
    sensitive_patterns = [
        (r'(?:api[_-]?key|token|secret|password)\s*[:=]\s*["\']([a-zA-Z0-9]{16,})["\']', "Hardcoded credential"),
        (r'["\']([a-f0-9]{32})["\']', "Possible hex key"),
        (r'(["\'][\w-]+@[\w-]+\.\w+["\'])', "Email address"),
        (r'(https?://[^\s]+key=[a-zA-Z0-9]{16,})', "URL with key"),
    ]

    issues = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            for pattern, issue_type in sensitive_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    issues.append((line_num, line.strip(), issue_type))

    return issues

# 使用示例
if __name__ == "__main__":
    for py_file in os.listdir('.'):
        if py_file.endswith('.py'):
            print(f"\n检查 {py_file}:")
            issues = detect_secrets(py_file)
            for line_num, line, issue_type in issues:
                print(f"  Line {line_num}: {issue_type}")
                print(f"    {line}")
```

## 最佳实践链接

- [PEP 8 -- Style Guide](https://peps.python.org/pep-0008/)
- [PEP 257 -- Docstring Conventions](https://peps.python.org/pep-0257/)
- [Type Hints (PEP 484)](https://peps.python.org/pep-0484/)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/security.html)
