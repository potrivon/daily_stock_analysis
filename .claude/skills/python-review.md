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

## 最佳实践链接

- [PEP 8 -- Style Guide](https://peps.python.org/pep-0008/)
- [PEP 257 -- Docstring Conventions](https://peps.python.org/pep-0257/)
- [Type Hints (PEP 484)](https://peps.python.org/pep-0484/)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/security.html)
