# GitHub Actions 配置指南 - 均线偏离分析

## 📋 概述

本文档说明如何在 GitHub Actions 中配置和运行均线偏离分析。

## 🚀 快速开始

### 步骤 1：配置 Secrets

在 GitHub 仓库中配置必要的 Secrets：

1. 进入仓库页面
2. 点击 **Settings** → **Secrets and variables** → **Actions**
3. 点击 **New repository secret**
4. 添加以下 Secret：

| Secret 名称 | 说明 | 是否必需 | 示例值 |
|------------|------|---------|--------|
| `PUSHPLUS_TOKEN` | PushPlus 推送 Token | 可选 | `abc123...` |

### 步骤 2：配置 Variables（推荐）

配置股票列表（使用 Variables 而非 Secrets，便于修改）：

1. 在 **Settings** → **Secrets and variables** → **Actions** 页面
2. 切换到 **Variables** 标签
3. 点击 **New repository variable**
4. 添加以下 Variable：

| Variable 名称 | 说明 | 示例值 |
|--------------|------|--------|
| `STOCK_LIST` | 自选股列表（逗号分隔） | `600519,000001,601899,300750` |

### 步骤 3：启用 Workflow

1. 进入仓库的 **Actions** 标签
2. 找到 **均线偏离分析** workflow
3. 如果被禁用，点击 **Enable workflow**

## ⏰ 运行方式

### 方式一：自动定时运行

Workflow 已配置为每个工作日（周一至周五）北京时间 15:30 自动运行。

```yaml
schedule:
  - cron: '30 7 * * 1-5'  # UTC 07:30 = 北京 15:30
```

### 方式二：手动触发

1. 进入 **Actions** 标签
2. 选择 **均线偏离分析** workflow
3. 点击 **Run workflow**
4. 可选配置：
   - **偏离阈值**：默认 1.5%
   - **是否推送通知**：默认 true

## 📊 Workflow 详解

### 触发条件

```yaml
on:
  # 定时触发 - 每天北京时间 15:30（收盘后）
  schedule:
    - cron: '30 7 * * 1-5'  # 仅工作日
  
  # 手动触发
  workflow_dispatch:
    inputs:
      threshold:
        description: '偏离阈值（百分比）'
        default: '1.5'
      push_notification:
        description: '是否推送通知'
        default: true
```

### 执行步骤

1. **检出代码**：获取最新代码
2. **设置 Python 环境**：使用 Python 3.11
3. **安装依赖**：安装必要的 Python 包
4. **创建目录**：创建 data、logs、reports 目录
5. **执行分析**：运行 `ma_deviation_analyzer.py --batch`
6. **保存日志**：上传日志到 Artifacts
7. **显示摘要**：在 GitHub Actions 页面显示运行摘要

### 环境变量

```yaml
env:
  STOCK_LIST: ${{ vars.STOCK_LIST || secrets.STOCK_LIST || '600519,000001,601899' }}
  PUSHPLUS_TOKEN: ${{ secrets.PUSHPLUS_TOKEN }}
  LOG_LEVEL: INFO
```

## 🔧 自定义配置

### 修改运行时间

编辑 `.github/workflows/ma_deviation_analysis.yml`：

```yaml
schedule:
  # 示例：每天 9:30 和 15:30 运行两次
  - cron: '30 1 * * 1-5'   # UTC 01:30 = 北京 09:30
  - cron: '30 7 * * 1-5'   # UTC 07:30 = 北京 15:30
```

**Cron 表达式说明**：
- 格式：`分 时 日 月 星期`
- `30 7 * * 1-5`：每个工作日的 UTC 07:30
- `1-5`：周一到周五
- `*`：每天/每月

**时区转换**：
- GitHub Actions 使用 UTC 时间
- 北京时间 = UTC + 8
- 例如：北京 15:30 = UTC 07:30

### 修改偏离阈值

**方法一：修改默认值**

编辑 workflow 文件：

```yaml
workflow_dispatch:
  inputs:
    threshold:
      default: '2.0'  # 修改为 2.0%
```

**方法二：手动运行时指定**

在手动触发时输入自定义阈值。

### 添加更多股票

修改 `STOCK_LIST` Variable：

1. 进入 **Settings** → **Secrets and variables** → **Actions** → **Variables**
2. 编辑 `STOCK_LIST`
3. 添加更多股票代码，用逗号分隔

示例：
```
600519,000001,601899,300750,002594,000858,600036
```

## 📱 推送配置

### PushPlus 推送

1. **获取 Token**
   - 访问 https://www.pushplus.plus
   - 微信扫码登录
   - 复制 Token

2. **配置 Secret**
   - 在 GitHub 仓库添加 Secret：`PUSHPLUS_TOKEN`
   - 值为你的 PushPlus Token

3. **测试推送**
   - 手动触发 workflow
   - 检查微信是否收到推送

### 推送内容

推送报告包含：
- 操作建议汇总（买入/卖出/中性信号统计）
- 买入机会列表（按置信度排序）
- 卖出提示列表（按置信度排序）
- 中性观望列表
- 偏离度计算说明

## 📝 查看结果

### 方式一：GitHub Actions 页面

1. 进入 **Actions** 标签
2. 选择最近的运行记录
3. 查看运行摘要和日志

### 方式二：下载 Artifacts

1. 在运行记录页面
2. 滚动到底部的 **Artifacts** 部分
3. 下载 `ma-deviation-logs-xxx`
4. 解压查看详细日志

### 方式三：微信推送

如果配置了 PushPlus，会自动推送到微信。

## 🐛 故障排查

### 问题 1：Workflow 未自动运行

**可能原因**：
- Workflow 被禁用
- 仓库不活跃（GitHub 会禁用长期不活跃仓库的定时任务）

**解决方法**：
- 检查 Actions 页面，启用 workflow
- 定期手动触发或提交代码保持活跃

### 问题 2：推送失败

**可能原因**：
- `PUSHPLUS_TOKEN` 未配置或错误
- PushPlus 服务异常
- 网络问题

**解决方法**：
- 检查 Secret 配置
- 查看运行日志中的错误信息
- 访问 PushPlus 网站检查 Token 状态

### 问题 3：股票列表为空

**可能原因**：
- `STOCK_LIST` 未配置
- 配置格式错误

**解决方法**：
- 检查 Variables 或 Secrets 中的 `STOCK_LIST`
- 确保格式正确：`600519,000001,601899`（无空格）

### 问题 4：依赖安装失败

**可能原因**：
- `requirements.txt` 缺少依赖
- PyPI 网络问题

**解决方法**：
- 检查 workflow 中的依赖安装步骤
- 当前 workflow 已简化依赖，只安装必需的包

## 💡 最佳实践

### 1. 使用 Variables 而非 Secrets

对于非敏感信息（如股票列表），使用 Variables：
- ✅ 便于修改
- ✅ 可以在 workflow 文件中引用
- ✅ 不会被隐藏

对于敏感信息（如 Token），使用 Secrets：
- ✅ 加密存储
- ✅ 日志中自动隐藏
- ✅ 更安全

### 2. 合理设置运行时间

- 选择收盘后的时间（如 15:30）
- 避免在交易时间运行
- 考虑数据更新延迟

### 3. 定期检查运行状态

- 订阅 GitHub Actions 通知
- 定期查看运行记录
- 及时处理失败的运行

### 4. 控制推送频率

- 避免过于频繁推送
- PushPlus 免费版有次数限制
- 建议每天 1-2 次

## 📚 相关文档

- [GitHub Actions 官方文档](https://docs.github.com/en/actions)
- [Cron 表达式在线生成器](https://crontab.guru/)
- [PushPlus 官方文档](https://www.pushplus.plus/doc/)
- [均线偏离分析器使用说明](./MA_DEVIATION_ANALYZER_README.md)
- [PushPlus 推送功能指南](./MA_DEVIATION_PUSHPLUS_GUIDE.md)

## 🎯 示例配置

### 完整配置示例

**Secrets**:
```
PUSHPLUS_TOKEN=abc123def456...
```

**Variables**:
```
STOCK_LIST=600519,000001,601899,300750,002594
```

**Workflow 配置**:
```yaml
# 每天 15:30 自动运行
schedule:
  - cron: '30 7 * * 1-5'

# 偏离阈值 1.5%
threshold: '1.5'

# 启用推送
push_notification: true
```

### 运行效果

```
==========================================
均线偏离分析
==========================================
自选股: 600519,000001,601899,300750,002594
偏离阈值: 1.5%
推送通知: true
时间: 2026-01-16 15:30:00
==========================================

正在分析 600519...
正在分析 000001...
正在分析 601899...
正在分析 300750...
正在分析 002594...

==========================================
分析汇总
==========================================
总计分析: 5 只股票
  买入信号: 2 只
  卖出信号: 2 只
  中性信号: 1 只

==========================================
正在推送分析结果到 PushPlus...
==========================================
✅ 推送成功！已发送到 PushPlus

==========================================
分析完成
==========================================
```

---

**更新时间**: 2026-01-16  
**版本**: 1.0
