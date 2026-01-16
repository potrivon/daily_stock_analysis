# 均线偏离分析器 - PushPlus 推送功能说明

## 🎉 新增功能

已为均线偏离分析器添加 **PushPlus 推送功能**，可以将分析结果自动推送到微信！

## 📱 功能特点

### 1. 自动推送分析报告
- 批量分析完成后自动推送
- 支持 Markdown 格式，排版美观
- 包含买入/卖出信号汇总
- 详细展示每只股票的偏离情况

### 2. 推送内容
推送报告包含以下内容：
- **操作建议汇总**：买入/卖出/中性信号统计
- **买入机会**：超卖股票列表（按置信度排序）
- **卖出提示**：超买股票列表（按置信度排序）
- **中性观望**：偏离正常的股票
- **说明文档**：偏离度计算公式和信号强度说明

## 🔧 配置方法

### 步骤 1：获取 PushPlus Token

1. 访问 [PushPlus 官网](https://www.pushplus.plus)
2. 使用微信扫码登录
3. 复制你的 Token（在首页可以看到）

### 步骤 2：配置环境变量

在项目根目录的 `.env` 文件中添加：

```bash
# PushPlus 推送配置
PUSHPLUS_TOKEN=your_token_here
```

将 `your_token_here` 替换为你从 PushPlus 获取的 Token。

### 步骤 3：运行批量分析

```bash
python ma_deviation_analyzer.py --batch
```

分析完成后会自动推送到你的微信！

## 📊 推送示例

### 推送标题
```
📊 均线偏离分析报告 - 2026-01-16
```

### 推送内容示例
```markdown
# 📊 2026-01-16 均线偏离分析报告

> 共分析 **3** 只股票 | 报告生成时间：19:31:59

---

## 📈 操作建议汇总

| 指标 | 数值 |
|------|------|
| 🟢 买入信号 | **1** 只 |
| 🔴 卖出信号 | **2** 只 |
| ⚪ 中性信号 | **0** 只 |

---

## 🟢 买入机会（超卖信号）

### 📈 股票000001 (000001)

**当前价格**: 12.62 | **置信度**: 100%

- **MA5**: 12.88 | 偏离 -2.00% | 弱超卖
- **MA10**: 13.17 | 偏离 -4.12% | 强超卖
- **MA20**: 13.45 | 偏离 -6.12% | 强超卖
- **MA60**: 13.76 | 偏离 -8.24% | 强超卖

💡 **操作建议**: 价格跌破均线支撑，出现超卖迹象，可关注反弹机会

---

## 🔴 卖出提示（超买信号）

### 📉 股票600519 (600519)

**当前价格**: 104.08 | **置信度**: 40%

- **MA60**: 101.36 | 偏离 +2.69% | 中超买

⚠️ **风险提示**: 价格突破均线压力，出现超买迹象，注意回调风险

---

## 📝 说明

**偏离度计算**: (当前价 - 均线) / 均线 × 100%

**信号强度**:
- 弱: 偏离 1.5% - 2.5%
- 中: 偏离 2.5% - 3.5%
- 强: 偏离 > 3.5%

⚠️ **风险提示**: 本分析仅供参考，不构成投资建议

*报告生成时间：2026-01-16 19:31:59*
```

## 🔍 技术实现

### 核心函数

#### 1. `send_to_pushplus()`
```python
def send_to_pushplus(token: str, title: str, content: str) -> bool:
    """
    发送消息到 PushPlus
    
    Args:
        token: PushPlus Token
        title: 消息标题
        content: 消息内容（Markdown 格式）
        
    Returns:
        是否发送成功
    """
```

#### 2. `generate_ma_deviation_report()`
```python
def generate_ma_deviation_report(results: List[DeviationAnalysisResult]) -> str:
    """
    生成均线偏离分析的 Markdown 推送报告
    
    Args:
        results: 分析结果列表
        
    Returns:
        Markdown 格式的报告内容
    """
```

### API 调用

使用 PushPlus 官方 API：
- **端点**: `https://www.pushplus.plus/send`
- **方法**: POST
- **格式**: JSON
- **参数**:
  - `token`: 你的 PushPlus Token
  - `title`: 消息标题
  - `content`: 消息内容
  - `template`: `markdown`（使用 Markdown 格式）
  - `channel`: `wechat`（推送到微信）

## 💡 使用技巧

### 1. 定时推送
可以结合系统定时任务实现每日自动推送：

**Windows 任务计划程序**:
```bash
# 每天 18:00 执行
schtasks /create /tn "股票分析" /tr "python d:\code\daily_stock_analysis\ma_deviation_analyzer.py --batch" /sc daily /st 18:00
```

**Linux Crontab**:
```bash
# 每天 18:00 执行
0 18 * * * cd /path/to/daily_stock_analysis && python ma_deviation_analyzer.py --batch
```

### 2. 集成到主程序
可以在主程序中调用批量分析功能：

```python
from ma_deviation_analyzer import batch_analyze_from_config

# 执行分析并推送
batch_analyze_from_config()
```

### 3. 自定义阈值
可以修改代码中的阈值参数：

```python
# 在 batch_analyze_from_config() 函数中
analyzer = MADeviationAnalyzer(threshold=2.0)  # 提高阈值，减少信号
```

## ⚠️ 注意事项

1. **Token 安全**: 不要将 Token 提交到公开的代码仓库
2. **推送频率**: PushPlus 免费版有推送次数限制，建议每天推送1-2次
3. **内容长度**: 单次推送内容不宜过长，建议控制在 10 只股票以内
4. **网络要求**: 需要能访问 PushPlus API（国内网络正常可用）

## 🐛 常见问题

### Q1: 提示"未配置 PushPlus Token"
**A**: 检查 `.env` 文件中是否正确配置了 `PUSHPLUS_TOKEN`

### Q2: 推送失败
**A**: 可能的原因：
- Token 错误或过期
- 网络连接问题
- PushPlus 服务异常

查看日志获取详细错误信息。

### Q3: 收不到微信推送
**A**: 
- 确认已在 PushPlus 网站上绑定微信
- 检查微信是否关注了 PushPlus 公众号
- 查看 PushPlus 网站的消息记录

## 📚 相关文档

- [PushPlus 官方文档](https://www.pushplus.plus/doc/)
- [均线偏离分析器使用说明](./MA_DEVIATION_ANALYZER_README.md)
- [项目主文档](./README.md)

## 🎯 下一步计划

- [ ] 支持更多推送渠道（企业微信、飞书、Telegram）
- [ ] 添加图表可视化
- [ ] 支持自定义推送模板
- [ ] 添加推送历史记录

---

**更新时间**: 2026-01-16  
**版本**: 1.0 - 首次发布 PushPlus 推送功能
