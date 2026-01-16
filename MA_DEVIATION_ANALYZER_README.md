# 均线偏离分析器使用说明

## 📋 概述

`ma_deviation_analyzer.py` 是一个股票均线偏离分析工具，用于识别股票价格相对于移动平均线的超买超卖状态。

## ✨ 功能特性

### 1. 核心分析功能
- **多周期均线分析**：支持 MA5、MA10、MA20、MA60
- **偏离度计算**：精确计算价格相对均线的偏离百分比
- **信号强度分级**：弱/中/强三级信号强度
- **综合信号判断**：基于多均线加权计算综合买卖信号
- **置信度评估**：0-100% 的信号置信度评分

### 2. 推送通知功能（新增）
- **PushPlus 推送**：支持将分析结果推送到微信
- **Markdown 格式**：推送内容排版美观，易于阅读
- **自动汇总**：智能汇总买入/卖出信号
- **一键推送**：批量分析完成后自动推送

详细配置请参考：[PushPlus 推送功能指南](./MA_DEVIATION_PUSHPLUS_GUIDE.md)

### 3. 两种运行模式

#### 模式一：单元测试模式（默认）
运行内置的4个测试用例，验证分析器功能：
```bash
python ma_deviation_analyzer.py
```

测试用例包括：
- ✅ 测试用例1：价格大幅低于均线（买入信号）
- ✅ 测试用例2：价格大幅高于均线（卖出信号）
- ✅ 测试用例3：价格在均线附近（中性信号）
- ✅ 测试用例4：极端超跌（强买入信号）

#### 模式二：批量分析模式（新增）
从配置文件读取股票列表并批量分析：
```bash
python ma_deviation_analyzer.py --batch
```

此模式会：
1. 从 `.env` 文件读取 `STOCK_LIST` 配置
2. 批量获取每只股票的历史数据
3. 进行均线偏离分析
4. 生成汇总报告，按置信度排序

## 🔧 配置说明

### 环境变量配置

在项目根目录的 `.env` 文件中配置股票列表：

```bash
# 自选股列表（逗号分隔）
STOCK_LIST=600519,000001,601899,300750,002594
```

### 默认股票列表

如果未配置 `STOCK_LIST`，系统将使用默认列表：
- 600519 - 贵州茅台
- 000001 - 平安银行
- 601899 - 紫金矿业

## 📊 分析逻辑

### 偏离度计算公式
```
偏离度 = (当前价 - 均线值) / 均线值 × 100%
```

### 信号判断规则

| 偏离度 | 信号类型 | 信号强度 | 操作建议 |
|--------|---------|---------|---------|
| ≥ +3.5% | 卖出 | 强 | 超买严重，建议止盈 |
| +2.5% ~ +3.5% | 卖出 | 中 | 超买，注意回调风险 |
| +1.5% ~ +2.5% | 卖出 | 弱 | 轻微超买 |
| -1.5% ~ +1.5% | 中性 | 无 | 正常区间，观望 |
| -2.5% ~ -1.5% | 买入 | 弱 | 轻微超卖 |
| -3.5% ~ -2.5% | 买入 | 中 | 超卖，关注反弹 |
| ≤ -3.5% | 买入 | 强 | 超卖严重，分批买入 |

### 综合信号计算

使用加权算法计算综合信号：
- 强信号权重 = 3
- 中信号权重 = 2
- 弱信号权重 = 1

置信度 = min(100, 信号权重总和 × 20)

## 📈 输出示例

### 单只股票分析结果
```
## [分析] 贵州茅台 (600519) 均线偏离分析

**当前价格**: 108.51
**分析时间**: 2026-01-16 19:21:04

### 偏离详情

[卖出] **MA5**: 106.38 | 偏离: +2.00% | 价格高于 MA5 2.00%，弱超买
[卖出] **MA10**: 104.47 | 偏离: +3.87% | 价格高于 MA10 3.87%，强超买
[卖出] **MA20**: 102.01 | 偏离: +6.37% | 价格高于 MA20 6.37%，强超买
[卖出] **MA60**: 99.6 | 偏离: +8.94% | 价格高于 MA60 8.94%，强超买

### 综合判断

[卖出] **综合信号**: 卖出 (置信度: 100%)

**操作建议**:
- 价格突破均线压力，出现超买迹象
- 建议注意回调风险，可考虑分批止盈
```

### 批量分析汇总
```
============================================================
分析汇总
============================================================
总计分析: 3 只股票
  买入信号: 1 只
  卖出信号: 2 只
  中性信号: 0 只

【买入机会】
  601899 股票601899 - 当前价: 11.63 - 置信度: 100%

【卖出提示】
  600519 股票600519 - 当前价: 108.51 - 置信度: 100%
  000001 股票000001 - 当前价: 14.96 - 置信度: 100%
```

## 🔌 集成到项目

### 在其他模块中使用

```python
from ma_deviation_analyzer import MADeviationAnalyzer
import pandas as pd

# 初始化分析器（可自定义阈值）
analyzer = MADeviationAnalyzer(threshold=1.5)

# 准备数据（需要包含 'date' 和 'close' 列）
df = pd.DataFrame({
    'date': [...],
    'close': [...]
})

# 进行分析
result = analyzer.analyze(df, code='600519', name='贵州茅台')

# 获取分析结果
print(f"综合信号: {result.overall_signal}")
print(f"置信度: {result.confidence}%")

# 格式化输出
print(analyzer.format_result(result))
```

### 数据结构

#### DeviationSignal（单均线信号）
```python
@dataclass
class DeviationSignal:
    ma_type: str          # 均线类型 (MA5/MA10/MA20/MA60)
    ma_value: float       # 均线值
    current_price: float  # 当前价格
    deviation_pct: float  # 偏离百分比
    signal: str           # 信号类型 (BUY/SELL/NEUTRAL)
    strength: str         # 信号强度 (弱/中/强)
    reason: str           # 信号原因
```

#### DeviationAnalysisResult（综合分析结果）
```python
@dataclass
class DeviationAnalysisResult:
    code: str                      # 股票代码
    name: str                      # 股票名称
    current_price: float           # 当前价格
    signals: List[DeviationSignal] # 各均线信号列表
    overall_signal: str            # 综合信号 (BUY/SELL/NEUTRAL)
    confidence: int                # 信号置信度 (0-100)
    analysis_time: str             # 分析时间
    raw_data: Dict                 # 原始数据
```

## 🚀 扩展开发

### 替换数据源

当前批量分析使用模拟数据，实际使用时需要替换 `get_stock_data_demo()` 函数：

```python
def get_stock_data_real(code: str) -> Optional[pd.DataFrame]:
    """从真实数据源获取股票数据"""
    from data_provider import AkShareProvider
    
    provider = AkShareProvider()
    df = provider.get_daily_data(code, days=100)
    
    # 确保包含必需的列
    if df is not None and 'close' in df.columns:
        return df
    return None
```

### 自定义阈值

```python
# 创建更敏感的分析器（阈值降低）
sensitive_analyzer = MADeviationAnalyzer(threshold=1.0)

# 创建更保守的分析器（阈值提高）
conservative_analyzer = MADeviationAnalyzer(threshold=2.5)
```

## 📝 注意事项

1. **数据质量**：分析结果依赖于输入数据的质量，确保数据完整且准确
2. **市场环境**：均线偏离分析在震荡市场效果较好，趋势市场需结合其他指标
3. **风险提示**：本工具仅供参考，不构成投资建议，投资有风险
4. **参数调整**：可根据不同股票特性调整阈值参数

## 🛠️ 依赖项

```bash
pip install pandas numpy python-dotenv
```

## 📄 许可证

本项目遵循 MIT 许可证。

---

**最后更新**: 2026-01-16  
**版本**: 2.0 - 新增批量分析功能
