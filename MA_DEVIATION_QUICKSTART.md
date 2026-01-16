# 均线偏离分析器 - 快速开始

## 🎯 功能概述

均线偏离分析器可以自动分析股票价格相对于移动平均线的偏离程度，识别超买超卖状态，并通过 PushPlus 推送到微信。

## 🚀 三种使用方式

### 方式一：本地运行

#### 1. 配置环境变量

在 `.env` 文件中添加：

```bash
# 自选股列表
STOCK_LIST=600519,000001,601899

# PushPlus 推送（可选）
PUSHPLUS_TOKEN=your_token_here
```

#### 2. 运行分析

```bash
# 运行单元测试
python ma_deviation_analyzer.py

# 批量分析（带推送）
python ma_deviation_analyzer.py --batch
```

📖 **详细文档**: [MA_DEVIATION_ANALYZER_README.md](./MA_DEVIATION_ANALYZER_README.md)

---

### 方式二：GitHub Actions 自动运行（推荐）

#### 1. 配置 GitHub Secrets

在仓库设置中添加：
- `PUSHPLUS_TOKEN`: PushPlus Token

#### 2. 配置 GitHub Variables

在仓库设置中添加：
- `STOCK_LIST`: 股票列表（如 `600519,000001,601899`）

#### 3. 启用 Workflow

进入 Actions 标签，启用 **均线偏离分析** workflow。

**自动运行时间**: 每个工作日 15:30（收盘后）

📖 **详细文档**: [GITHUB_ACTIONS_MA_DEVIATION_GUIDE.md](./GITHUB_ACTIONS_MA_DEVIATION_GUIDE.md)

---

### 方式三：集成到现有项目

```python
from ma_deviation_analyzer import MADeviationAnalyzer, batch_analyze_from_config

# 方式 A: 批量分析（从配置读取）
batch_analyze_from_config()

# 方式 B: 单只股票分析
analyzer = MADeviationAnalyzer(threshold=1.5)
result = analyzer.analyze(df, code='600519', name='贵州茅台')
print(analyzer.format_result(result))
```

📖 **详细文档**: [ma_deviation_real_example.py](./ma_deviation_real_example.py)

---

## 📱 PushPlus 推送配置

### 1. 获取 Token

1. 访问 https://www.pushplus.plus
2. 微信扫码登录
3. 复制 Token

### 2. 配置 Token

**本地运行**: 在 `.env` 文件中添加 `PUSHPLUS_TOKEN`

**GitHub Actions**: 在仓库 Secrets 中添加 `PUSHPLUS_TOKEN`

### 3. 推送效果

分析完成后会自动推送到微信，包含：
- 📊 操作建议汇总
- 🟢 买入机会列表
- 🔴 卖出提示列表
- ⚪ 中性观望列表

📖 **详细文档**: [MA_DEVIATION_PUSHPLUS_GUIDE.md](./MA_DEVIATION_PUSHPLUS_GUIDE.md)

---

## 📊 分析逻辑

### 偏离度计算

```
偏离度 = (当前价 - 均线值) / 均线值 × 100%
```

### 信号判断

| 偏离度 | 信号 | 强度 | 操作建议 |
|--------|------|------|---------|
| ≥ +3.5% | 卖出 | 强 | 超买严重，建议止盈 |
| +2.5% ~ +3.5% | 卖出 | 中 | 超买，注意回调 |
| +1.5% ~ +2.5% | 卖出 | 弱 | 轻微超买 |
| -1.5% ~ +1.5% | 中性 | - | 正常区间，观望 |
| -2.5% ~ -1.5% | 买入 | 弱 | 轻微超卖 |
| -3.5% ~ -2.5% | 买入 | 中 | 超卖，关注反弹 |
| ≤ -3.5% | 买入 | 强 | 超卖严重，分批买入 |

---

## 📁 文件说明

| 文件 | 说明 |
|------|------|
| `ma_deviation_analyzer.py` | 主程序文件 |
| `ma_deviation_real_example.py` | 真实数据集成示例 |
| `MA_DEVIATION_ANALYZER_README.md` | 完整使用文档 |
| `MA_DEVIATION_PUSHPLUS_GUIDE.md` | PushPlus 推送指南 |
| `GITHUB_ACTIONS_MA_DEVIATION_GUIDE.md` | GitHub Actions 配置指南 |
| `.github/workflows/ma_deviation_analysis.yml` | GitHub Actions Workflow |

---

## 🎯 快速测试

### 测试单元测试

```bash
python ma_deviation_analyzer.py
```

### 测试批量分析（不推送）

```bash
# 不配置 PUSHPLUS_TOKEN，只在控制台显示结果
python ma_deviation_analyzer.py --batch
```

### 测试推送功能

```bash
# 配置 PUSHPLUS_TOKEN 后运行
python ma_deviation_analyzer.py --batch
```

---

## ⚠️ 注意事项

1. **数据来源**: 当前使用模拟数据，实际使用需集成真实数据源
2. **推送频率**: PushPlus 免费版有次数限制，建议每天 1-2 次
3. **风险提示**: 本分析仅供参考，不构成投资建议

---

## 🆘 需要帮助？

- 📖 查看详细文档（见上方文件说明）
- 🐛 提交 Issue
- 💬 查看项目 README

---

**最后更新**: 2026-01-16
