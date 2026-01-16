# -*- coding: utf-8 -*-
"""
===================================
均线偏离分析器 (MA Deviation Analyzer)
===================================

分析股票价格相对于均线的偏离程度，当偏离超过阈值时给出交易信号。

逻辑：
- 偏离度 = (当前价 - 均线) / 均线 × 100%
- 正偏离过大 → 超买 → 卖出信号
- 负偏离过大 → 超卖 → 买入信号
"""

import logging
from dataclasses import dataclass
from typing import Optional, List, Dict
from datetime import datetime

import pandas as pd
import numpy as np

# 导入配置模块
from config import get_config

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class DeviationSignal:
    """偏离信号"""
    ma_type: str          # 均线类型 (MA5/MA10/MA20)
    ma_value: float       # 均线值
    current_price: float  # 当前价格
    deviation_pct: float  # 偏离百分比
    signal: str           # 信号类型 (BUY/SELL/NEUTRAL)
    strength: str         # 信号强度 (弱/中/强)
    reason: str           # 信号原因


@dataclass
class DeviationAnalysisResult:
    """偏离分析结果"""
    code: str
    name: str
    current_price: float
    signals: List[DeviationSignal]
    overall_signal: str   # 综合信号 (BUY/SELL/NEUTRAL)
    confidence: int       # 信号置信度 (0-100)
    analysis_time: str
    raw_data: Dict        # 原始数据


class MADeviationAnalyzer:
    """
    均线偏离分析器

    分析价格相对于均线的偏离程度，识别超买超卖状态。
    """

    # 偏离阈值配置
    THRESHOLDS = {
        'weak': 1.5,      # 弱信号阈值
        'medium': 2.5,    # 中信号阈值
        'strong': 3.5,    # 强信号阈值
    }

    def __init__(self, threshold: float = 1.5):
        """
        初始化分析器

        Args:
            threshold: 触发信号的偏离阈值（百分比），默认 1.5%
        """
        self.threshold = threshold
        self.THRESHOLDS = {
            'weak': threshold,
            'medium': threshold + 1.0,
            'strong': threshold + 2.0,
        }

    def calculate_ma(self, prices: pd.Series, period: int) -> float:
        """
        计算移动平均线

        Args:
            prices: 价格序列
            period: 周期

        Returns:
            MA 值
        """
        if len(prices) < period:
            return 0.0
        return prices.tail(period).mean()

    def calculate_deviation(self, current_price: float, ma_value: float) -> float:
        """
        计算偏离百分比

        Args:
            current_price: 当前价格
            ma_value: 均线值

        Returns:
            偏离百分比
        """
        if ma_value == 0:
            return 0.0
        return (current_price - ma_value) / ma_value * 100

    def get_signal_strength(self, deviation_pct: float) -> str:
        """
        根据偏离程度判断信号强度

        Args:
            deviation_pct: 偏离百分比

        Returns:
            信号强度: 弱/中/强
        """
        abs_dev = abs(deviation_pct)

        if abs_dev >= self.THRESHOLDS['strong']:
            return '强'
        elif abs_dev >= self.THRESHOLDS['medium']:
            return '中'
        elif abs_dev >= self.THRESHOLDS['weak']:
            return '弱'
        else:
            return '无'

    def generate_signal(self, deviation_pct: float, ma_type: str) -> DeviationSignal:
        """
        生成交易信号

        Args:
            deviation_pct: 偏离百分比
            ma_type: 均线类型

        Returns:
            DeviationSignal 对象
        """
        strength = self.get_signal_strength(deviation_pct)

        if deviation_pct >= self.THRESHOLDS['weak']:
            # 正偏离过大，超买，卖出信号
            signal = 'SELL'
            reason = f"价格高于 {ma_type} {abs(deviation_pct):.2f}%，{strength}超买"
        elif deviation_pct <= -self.THRESHOLDS['weak']:
            # 负偏离过大，超卖，买入信号
            signal = 'BUY'
            reason = f"价格低于 {ma_type} {abs(deviation_pct):.2f}%，{strength}超卖"
        else:
            # 偏离在正常范围内
            signal = 'NEUTRAL'
            reason = f"价格偏离 {ma_type} {deviation_pct:.2f}%，处于正常区间"

        return DeviationSignal(
            ma_type=ma_type,
            ma_value=0.0,  # 需要外部填入
            current_price=0.0,  # 需要外部填入
            deviation_pct=deviation_pct,
            signal=signal,
            strength=strength,
            reason=reason
        )

    def analyze(self, df: pd.DataFrame, code: str, name: str) -> DeviationAnalysisResult:
        """
        分析股票的均线偏离情况

        Args:
            df: 包含收盘价的历史数据 DataFrame
            code: 股票代码
            name: 股票名称

        Returns:
            DeviationAnalysisResult 对象
        """
        # 确保数据按日期排序
        df = df.sort_values('date').reset_index(drop=True)

        # 获取最新收盘价
        if len(df) == 0:
            raise ValueError(f"股票 {code} 数据为空")

        current_price = df.iloc[-1]['close']

        # 计算各周期均线
        ma_periods = [5, 10, 20, 60]
        signals = []
        raw_data = {}

        for period in ma_periods:
            if len(df) < period:
                logger.warning(f"{code} 数据不足，无法计算 MA{period}")
                continue

            ma_value = self.calculate_ma(df['close'], period)
            deviation_pct = self.calculate_deviation(current_price, ma_value)

            # 生成信号
            signal = self.generate_signal(deviation_pct, f'MA{period}')

            # 填入实际值
            signal.ma_value = round(ma_value, 2)
            signal.current_price = round(current_price, 2)

            signals.append(signal)

            raw_data[f'MA{period}'] = {
                'value': round(ma_value, 2),
                'deviation_pct': round(deviation_pct, 2),
                'signal': signal.signal,
                'strength': signal.strength
            }

        # 计算综合信号
        overall_signal, confidence = self._calculate_overall_signal(signals)

        return DeviationAnalysisResult(
            code=code,
            name=name,
            current_price=round(current_price, 2),
            signals=signals,
            overall_signal=overall_signal,
            confidence=confidence,
            analysis_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            raw_data=raw_data
        )

    def _calculate_overall_signal(self, signals: List[DeviationSignal]) -> tuple:
        """
        计算综合信号

        Args:
            signals: 各均线信号列表

        Returns:
            (综合信号, 置信度)
        """
        if not signals:
            return 'NEUTRAL', 0

        buy_count = sum(1 for s in signals if s.signal == 'BUY')
        sell_count = sum(1 for s in signals if s.signal == 'SELL')

        # 计算加权强度（强=3，中=2，弱=1）
        strength_weights = {'强': 3, '中': 2, '弱': 1, '无': 0}

        buy_weight = sum(
            strength_weights[s.strength] for s in signals if s.signal == 'BUY'
        )
        sell_weight = sum(
            strength_weights[s.strength] for s in signals if s.signal == 'SELL'
        )

        if buy_weight > sell_weight and buy_count > 0:
            confidence = min(100, int(buy_weight * 20))
            return 'BUY', confidence
        elif sell_weight > buy_weight and sell_count > 0:
            confidence = min(100, int(sell_weight * 20))
            return 'SELL', confidence
        else:
            return 'NEUTRAL', 0

    def format_result(self, result: DeviationAnalysisResult) -> str:
        """
        格式化分析结果为易读文本

        Args:
            result: 分析结果

        Returns:
            格式化的文本
        """
        lines = [
            f"## [分析] {result.name} ({result.code}) 均线偏离分析",
            "",
            f"**当前价格**: {result.current_price}",
            f"**分析时间**: {result.analysis_time}",
            "",
            "### 偏离详情",
            "",
        ]

        for sig in result.signals:
            emoji = "[卖出]" if sig.signal == "SELL" else ("[买入]" if sig.signal == "BUY" else "[中性]")
            lines.append(f"{emoji} **{sig.ma_type}**: {sig.ma_value} | 偏离: {sig.deviation_pct:+.2f}% | {sig.reason}")

        lines.extend([
            "",
            "### 综合判断",
            "",
        ])

        overall_emoji = "[卖出]" if result.overall_signal == "SELL" else ("[买入]" if result.overall_signal == "BUY" else "[中性]")
        signal_text = {"BUY": "买入", "SELL": "卖出", "NEUTRAL": "观望"}[result.overall_signal]

        lines.append(f"{overall_emoji} **综合信号**: {signal_text} (置信度: {result.confidence}%)")

        if result.overall_signal != 'NEUTRAL':
            lines.extend([
                "",
                "**操作建议**:",
            ])
            if result.overall_signal == 'BUY':
                lines.append("- 价格跌破均线支撑，出现超卖迹象")
                lines.append("- 建议关注反弹机会，可考虑分批买入")
            else:
                lines.append("- 价格突破均线压力，出现超买迹象")
                lines.append("- 建议注意回调风险，可考虑分批止盈")

        return "\n".join(lines)


# ==================== 测试代码 ====================

def create_test_data(close_prices: List[float]) -> pd.DataFrame:
    """
    创建测试数据

    Args:
        close_prices: 收盘价列表

    Returns:
        DataFrame
    """
    dates = pd.date_range(end=datetime.now(), periods=len(close_prices), freq='D')
    return pd.DataFrame({
        'date': dates,
        'close': close_prices
    })


def test_case_1():
    """测试用例1: 价格大幅低于均线（买入信号）"""
    print("=" * 60)
    print("测试用例1: 价格大幅低于均线（买入信号）")
    print("=" * 60)

    # 构造测试数据：均线约100，当前价格97（偏离-3%）
    base_price = 100
    prices = [
        base_price] * 20 + [  # 前20天稳定在100
        101, 100, 99, 98, 97   # 最近5天下跌到97
    ]

    df = create_test_data(prices)
    analyzer = MADeviationAnalyzer(threshold=1.5)

    result = analyzer.analyze(df, '600519', '贵州茅台')
    print(analyzer.format_result(result))
    print()

    # 验证
    assert result.overall_signal == 'BUY', f"期望 BUY，实际 {result.overall_signal}"
    assert result.confidence > 0, f"期望置信度 > 0，实际 {result.confidence}"
    print("[PASS] 测试用例1 通过\n")


def test_case_2():
    """测试用例2: 价格大幅高于均线（卖出信号）"""
    print("=" * 60)
    print("测试用例2: 价格大幅高于均线（卖出信号）")
    print("=" * 60)

    # 构造测试数据：均线约100，当前价格103.5（偏离+3.5%）
    base_price = 100
    prices = [
        base_price] * 20 + [  # 前20天稳定在100
        101, 102, 103, 103.2, 103.5   # 最近5天上涨到103.5
    ]

    df = create_test_data(prices)
    analyzer = MADeviationAnalyzer(threshold=1.5)

    result = analyzer.analyze(df, '000001', '平安银行')
    print(analyzer.format_result(result))
    print()

    # 验证
    assert result.overall_signal == 'SELL', f"期望 SELL，实际 {result.overall_signal}"
    assert result.confidence > 0, f"期望置信度 > 0，实际 {result.confidence}"
    print("[PASS] 测试用例2 通过\n")


def test_case_3():
    """测试用例3: 价格在均线附近（中性信号）"""
    print("=" * 60)
    print("测试用例3: 价格在均线附近（中性信号）")
    print("=" * 60)

    # 构造测试数据：价格围绕均线小幅波动
    base_price = 100
    prices = [
        base_price] * 20 + [  # 前20天稳定在100
        100.5, 99.8, 100.2, 99.9, 100.3   # 最近5天小幅波动
    ]

    df = create_test_data(prices)
    analyzer = MADeviationAnalyzer(threshold=1.5)

    result = analyzer.analyze(df, '300750', '宁德时代')
    print(analyzer.format_result(result))
    print()

    # 验证
    assert result.overall_signal == 'NEUTRAL', f"期望 NEUTRAL，实际 {result.overall_signal}"
    print("[PASS] 测试用例3 通过\n")


def test_case_4():
    """测试用例4: 极端超跌（强买入信号）"""
    print("=" * 60)
    print("测试用例4: 极端超跌（强买入信号）")
    print("=" * 60)

    # 构造测试数据：均线约100，当前价格94（偏离-6%）
    base_price = 100
    prices = [
        base_price] * 20 + [  # 前20天稳定在100
        98, 96, 95, 94.5, 94   # 最近5天大幅下跌到94
    ]

    df = create_test_data(prices)
    analyzer = MADeviationAnalyzer(threshold=1.5)

    result = analyzer.analyze(df, '601899', '紫金矿业')
    print(analyzer.format_result(result))
    print()

    # 验证
    assert result.overall_signal == 'BUY', f"期望 BUY，实际 {result.overall_signal}"
    assert result.confidence >= 80, f"期望置信度 >= 80，实际 {result.confidence}"
    print("[PASS] 测试用例4 通过\n")


def batch_analyze_from_config():
    """
    从配置文件读取股票列表并批量分析
    
    这个函数会：
    1. 从 config.stock_list 读取股票代码
    2. 获取每只股票的历史数据
    3. 获取股票真实名称
    4. 进行均线偏离分析
    5. 汇总并展示结果
    6. 推送到配置的通知渠道（如 PushPlus）
    """
    print("=" * 60)
    print("批量分析 - 从配置文件读取股票列表")
    print("=" * 60)
    
    # 获取配置
    config = get_config()
    stock_list = config.stock_list
    
    if not stock_list:
        print("[ERROR] 配置中没有股票列表，请在 .env 文件中设置 STOCK_LIST")
        return
    
    print(f"读取到 {len(stock_list)} 只股票: {', '.join(stock_list)}")
    print()
    
    # 初始化分析器
    analyzer = MADeviationAnalyzer(threshold=1.5)
    
    # 获取股票名称映射
    stock_names = get_stock_names(stock_list)
    
    # 存储分析结果
    results = []
    
    # 批量分析
    for code in stock_list:
        try:
            # 获取股票名称
            stock_name = stock_names.get(code, f'股票{code}')
            print(f"正在分析 {code} ({stock_name})...")
            
            # 这里需要实际的数据获取逻辑
            # 为了演示，我们使用模拟数据
            # 在实际使用中，应该从 data_provider 获取真实数据
            df = get_stock_data_demo(code)
            
            if df is None or len(df) == 0:
                print(f"  [跳过] {code} - 无法获取数据\n")
                continue
            
            # 进行分析
            result = analyzer.analyze(df, code, stock_name)
            results.append(result)
            
            # 打印分析结果
            print(analyzer.format_result(result))
            print()
            
        except Exception as e:
            print(f"  [错误] {code} - {str(e)}\n")
            continue
    
    # 汇总结果
    print("=" * 60)
    print("分析汇总")
    print("=" * 60)
    
    if not results:
        print("没有成功分析的股票")
        return
    
    buy_signals = [r for r in results if r.overall_signal == 'BUY']
    sell_signals = [r for r in results if r.overall_signal == 'SELL']
    neutral_signals = [r for r in results if r.overall_signal == 'NEUTRAL']
    
    print(f"总计分析: {len(results)} 只股票")
    print(f"  买入信号: {len(buy_signals)} 只")
    print(f"  卖出信号: {len(sell_signals)} 只")
    print(f"  中性信号: {len(neutral_signals)} 只")
    print()
    
    if buy_signals:
        print("【买入机会】")
        for r in sorted(buy_signals, key=lambda x: x.confidence, reverse=True):
            print(f"  {r.code} {r.name} - 当前价: {r.current_price} - 置信度: {r.confidence}%")
        print()
    
    if sell_signals:
        print("【卖出提示】")
        for r in sorted(sell_signals, key=lambda x: x.confidence, reverse=True):
            print(f"  {r.code} {r.name} - 当前价: {r.current_price} - 置信度: {r.confidence}%")
        print()
    
    # 推送到通知渠道
    try:
        config = get_config()
        
        # 检查是否配置了 PushPlus
        if hasattr(config, 'pushplus_token') and config.pushplus_token:
            print("\n" + "=" * 60)
            print("正在推送分析结果到 PushPlus...")
            print("=" * 60)
            
            # 生成推送内容
            report_content = generate_ma_deviation_report(results)
            
            # 发送到 PushPlus
            success = send_to_pushplus(
                token=config.pushplus_token,
                title=f"📊 均线偏离分析报告 - {datetime.now().strftime('%Y-%m-%d')}",
                content=report_content
            )
            
            if success:
                print("✅ 推送成功！已发送到 PushPlus")
            else:
                print("❌ 推送失败，请检查配置")
        else:
            print("\n💡 提示：未配置 PushPlus Token，跳过推送")
            print("   可在 .env 文件中配置 PUSHPLUS_TOKEN 启用推送功能")
    except Exception as e:
        print(f"\n❌ 推送失败: {e}")
        logger.error(f"推送异常: {e}", exc_info=True)


def get_stock_names(stock_codes: List[str]) -> Dict[str, str]:
    """
    批量获取股票名称
    
    Args:
        stock_codes: 股票代码列表
        
    Returns:
        股票代码到名称的映射字典
    """
    stock_names = {}
    
    try:
        import akshare as ak
        
        logger.info("正在获取股票名称...")
        
        # 获取A股实时行情（包含所有股票的名称）
        df = ak.stock_zh_a_spot_em()
        
        if df is not None and not df.empty:
            # 创建代码到名称的映射
            for code in stock_codes:
                # 查找对应股票
                row = df[df['代码'] == code]
                if not row.empty:
                    stock_names[code] = row.iloc[0]['名称']
                    logger.info(f"  {code}: {stock_names[code]}")
                else:
                    logger.warning(f"  {code}: 未找到名称，使用默认")
                    stock_names[code] = f'股票{code}'
        else:
            logger.warning("获取股票名称失败，使用默认名称")
            for code in stock_codes:
                stock_names[code] = f'股票{code}'
                
    except ImportError:
        logger.warning("akshare 未安装，使用默认股票名称")
        for code in stock_codes:
            stock_names[code] = f'股票{code}'
    except Exception as e:
        logger.error(f"获取股票名称失败: {e}")
        for code in stock_codes:
            stock_names[code] = f'股票{code}'
    
    return stock_names



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
    try:
        import requests
        
        # PushPlus API 端点
        api_url = "https://www.pushplus.plus/send"
        
        # 构建请求数据
        payload = {
            "token": token,
            "title": title,
            "content": content,
            "template": "markdown",
            "channel": "wechat"
        }
        
        # 发送请求
        response = requests.post(api_url, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            # PushPlus 返回格式：{"code": 200, "msg": "请求成功", "data": {...}}
            if result.get('code') == 200:
                logger.info("PushPlus 消息发送成功")
                return True
            else:
                error_msg = result.get('msg', '未知错误')
                logger.error(f"PushPlus 返回错误: {error_msg}")
                return False
        else:
            logger.error(f"PushPlus 请求失败: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        logger.error(f"发送 PushPlus 消息失败: {e}")
        return False



def generate_ma_deviation_report(results: List[DeviationAnalysisResult]) -> str:
    """
    生成均线偏离分析的 Markdown 推送报告
    
    Args:
        results: 分析结果列表
        
    Returns:
        Markdown 格式的报告内容
    """
    report_date = datetime.now().strftime('%Y-%m-%d')
    report_time = datetime.now().strftime('%H:%M:%S')
    
    # 统计信息
    buy_signals = [r for r in results if r.overall_signal == 'BUY']
    sell_signals = [r for r in results if r.overall_signal == 'SELL']
    neutral_signals = [r for r in results if r.overall_signal == 'NEUTRAL']
    
    lines = [
        f"# 📊 {report_date} 均线偏离分析报告",
        "",
        f"> 共分析 **{len(results)}** 只股票 | 报告生成时间：{report_time}",
        "",
        "---",
        "",
        "## 📈 操作建议汇总",
        "",
        f"| 指标 | 数值 |",
        f"|------|------|",
        f"| 🟢 买入信号 | **{len(buy_signals)}** 只 |",
        f"| 🔴 卖出信号 | **{len(sell_signals)}** 只 |",
        f"| ⚪ 中性信号 | **{len(neutral_signals)}** 只 |",
        "",
        "---",
        "",
    ]
    
    # 买入机会
    if buy_signals:
        lines.extend([
            "## 🟢 买入机会（超卖信号）",
            "",
        ])
        
        for r in sorted(buy_signals, key=lambda x: x.confidence, reverse=True):
            lines.extend([
                f"### 📈 {r.name} ({r.code})",
                "",
                f"**当前价格**: {r.current_price} | **置信度**: {r.confidence}%",
                "",
            ])
            
            # 显示各均线偏离情况
            for sig in r.signals:
                if sig.signal == 'BUY':
                    lines.append(f"- **{sig.ma_type}**: {sig.ma_value} | 偏离 {sig.deviation_pct:+.2f}% | {sig.strength}超卖")
            
            lines.extend([
                "",
                f"💡 **操作建议**: 价格跌破均线支撑，出现超卖迹象，可关注反弹机会",
                "",
                "---",
                "",
            ])
    
    # 卖出提示
    if sell_signals:
        lines.extend([
            "## 🔴 卖出提示（超买信号）",
            "",
        ])
        
        for r in sorted(sell_signals, key=lambda x: x.confidence, reverse=True):
            lines.extend([
                f"### 📉 {r.name} ({r.code})",
                "",
                f"**当前价格**: {r.current_price} | **置信度**: {r.confidence}%",
                "",
            ])
            
            # 显示各均线偏离情况
            for sig in r.signals:
                if sig.signal == 'SELL':
                    lines.append(f"- **{sig.ma_type}**: {sig.ma_value} | 偏离 {sig.deviation_pct:+.2f}% | {sig.strength}超买")
            
            lines.extend([
                "",
                f"⚠️ **风险提示**: 价格突破均线压力，出现超买迹象，注意回调风险",
                "",
                "---",
                "",
            ])
    
    # 中性观望
    if neutral_signals:
        lines.extend([
            "## ⚪ 中性观望",
            "",
        ])
        
        for r in neutral_signals:
            lines.append(f"- **{r.name} ({r.code})**: 当前价 {r.current_price}，偏离在正常区间")
        
        lines.extend([
            "",
            "---",
            "",
        ])
    
    # 底部说明
    lines.extend([
        "",
        "## 📝 说明",
        "",
        "**偏离度计算**: (当前价 - 均线) / 均线 × 100%",
        "",
        "**信号强度**:",
        "- 弱: 偏离 1.5% - 2.5%",
        "- 中: 偏离 2.5% - 3.5%",
        "- 强: 偏离 > 3.5%",
        "",
        "⚠️ **风险提示**: 本分析仅供参考，不构成投资建议",
        "",
        f"*报告生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*",
    ])
    
    return "\n".join(lines)


def get_stock_data_demo(code: str) -> Optional[pd.DataFrame]:
    """
    获取股票数据（演示版本）
    
    在实际使用中，应该替换为真实的数据获取逻辑，例如：
    - 从 data_provider 模块获取
    - 从数据库读取
    - 从 API 获取
    
    Args:
        code: 股票代码
        
    Returns:
        包含历史数据的 DataFrame，如果获取失败则返回 None
    """
    try:
        # 这里使用模拟数据作为演示
        # 实际使用时应该调用真实的数据获取函数
        
        # 模拟不同股票的价格走势
        base_prices = {
            '600519': 100.0,  # 贵州茅台
            '000001': 15.0,   # 平安银行
            '601899': 12.0,   # 紫金矿业
            '300750': 200.0,  # 宁德时代
            '002594': 50.0,   # 比亚迪
        }
        
        base_price = base_prices.get(code, 50.0)
        
        # 生成60天的历史数据，包含一些随机波动
        np.random.seed(hash(code) % 2**32)  # 使用股票代码作为随机种子
        
        prices = []
        current_price = base_price
        
        for i in range(60):
            # 添加随机波动 (-2% 到 +2%)
            change = np.random.uniform(-0.02, 0.02)
            current_price = current_price * (1 + change)
            prices.append(current_price)
        
        # 最后5天添加趋势（用于生成信号）
        trend = np.random.choice(['up', 'down', 'neutral'])
        if trend == 'up':
            for i in range(5):
                prices.append(prices[-1] * 1.01)  # 上涨1%
        elif trend == 'down':
            for i in range(5):
                prices.append(prices[-1] * 0.99)  # 下跌1%
        else:
            for i in range(5):
                prices.append(prices[-1] * (1 + np.random.uniform(-0.005, 0.005)))
        
        return create_test_data(prices)
        
    except Exception as e:
        logger.error(f"获取股票 {code} 数据失败: {e}")
        return None



def run_all_tests():
    """运行所有测试"""
    print("\n" + "=" * 60)
    print("均线偏离分析器 - 测试套件")
    print("=" * 60 + "\n")

    try:
        test_case_1()
        test_case_2()
        test_case_3()
        test_case_4()

        print("=" * 60)
        print("[SUCCESS] 所有测试通过!")
        print("=" * 60)

    except AssertionError as e:
        print(f"[FAIL] 测试失败: {e}")
        return False
    except Exception as e:
        print(f"[FAIL] 测试异常: {e}")
        import traceback
        traceback.print_exc()
        return False

    return True


if __name__ == "__main__":
    import sys
    
    # 检查命令行参数
    if len(sys.argv) > 1 and sys.argv[1] == '--batch':
        # 批量分析模式：从配置文件读取股票列表
        print("\n" + "=" * 60)
        print("均线偏离分析器 - 批量分析模式")
        print("=" * 60 + "\n")
        batch_analyze_from_config()
    else:
        # 默认模式：运行单元测试
        success = run_all_tests()
        exit(0 if success else 1)

