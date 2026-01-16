# -*- coding: utf-8 -*-
"""
均线偏离分析器 - 真实数据集成示例

演示如何将 ma_deviation_analyzer 集成到实际项目中，
使用真实的股票数据进行分析。
"""

import sys
from typing import Optional
import pandas as pd
from ma_deviation_analyzer import MADeviationAnalyzer, DeviationAnalysisResult
from config import get_config

# 尝试导入数据提供者
try:
    from data_provider.akshare_provider import AkShareProvider
    HAS_DATA_PROVIDER = True
except ImportError:
    HAS_DATA_PROVIDER = False
    print("警告: 未找到 data_provider 模块，将使用模拟数据")


def get_real_stock_data(code: str, days: int = 100) -> Optional[pd.DataFrame]:
    """
    获取真实股票数据
    
    Args:
        code: 股票代码
        days: 获取天数
        
    Returns:
        包含历史数据的 DataFrame
    """
    if not HAS_DATA_PROVIDER:
        print(f"  [警告] 无法获取 {code} 的真实数据，请安装数据提供者模块")
        return None
    
    try:
        provider = AkShareProvider()
        df = provider.get_daily_data(code, days=days)
        
        if df is None or len(df) == 0:
            print(f"  [警告] {code} 数据为空")
            return None
        
        # 确保包含必需的列
        if 'close' not in df.columns:
            print(f"  [错误] {code} 数据缺少 'close' 列")
            return None
        
        # 确保有日期列
        if 'date' not in df.columns:
            if df.index.name == 'date':
                df = df.reset_index()
            else:
                print(f"  [错误] {code} 数据缺少 'date' 列")
                return None
        
        return df
        
    except Exception as e:
        print(f"  [错误] 获取 {code} 数据失败: {e}")
        return None


def analyze_single_stock(code: str, name: str = None, threshold: float = 1.5) -> Optional[DeviationAnalysisResult]:
    """
    分析单只股票
    
    Args:
        code: 股票代码
        name: 股票名称（可选）
        threshold: 偏离阈值
        
    Returns:
        分析结果
    """
    print(f"\n{'='*60}")
    print(f"分析股票: {code} {name or ''}")
    print('='*60)
    
    # 获取数据
    df = get_real_stock_data(code)
    if df is None:
        return None
    
    print(f"获取到 {len(df)} 天的历史数据")
    
    # 创建分析器
    analyzer = MADeviationAnalyzer(threshold=threshold)
    
    # 进行分析
    try:
        result = analyzer.analyze(df, code, name or code)
        
        # 打印结果
        print(analyzer.format_result(result))
        
        return result
        
    except Exception as e:
        print(f"分析失败: {e}")
        return None


def batch_analyze_with_real_data(threshold: float = 1.5):
    """
    使用真实数据批量分析配置中的股票
    
    Args:
        threshold: 偏离阈值
    """
    print("\n" + "="*60)
    print("批量分析 - 使用真实数据")
    print("="*60 + "\n")
    
    # 获取配置
    config = get_config()
    stock_list = config.stock_list
    
    if not stock_list:
        print("[错误] 配置中没有股票列表，请在 .env 文件中设置 STOCK_LIST")
        return
    
    print(f"读取到 {len(stock_list)} 只股票: {', '.join(stock_list)}")
    
    # 初始化分析器
    analyzer = MADeviationAnalyzer(threshold=threshold)
    
    # 存储分析结果
    results = []
    
    # 批量分析
    for i, code in enumerate(stock_list, 1):
        print(f"\n[{i}/{len(stock_list)}] 正在分析 {code}...")
        
        try:
            # 获取真实数据
            df = get_real_stock_data(code)
            
            if df is None or len(df) == 0:
                print(f"  [跳过] {code} - 无法获取数据")
                continue
            
            print(f"  获取到 {len(df)} 天的历史数据")
            
            # 进行分析
            result = analyzer.analyze(df, code, f"股票{code}")
            results.append(result)
            
            # 打印简要结果
            signal_emoji = {
                'BUY': '📈 [买入]',
                'SELL': '📉 [卖出]',
                'NEUTRAL': '➡️  [中性]'
            }
            print(f"  {signal_emoji[result.overall_signal]} 当前价: {result.current_price} | 置信度: {result.confidence}%")
            
        except Exception as e:
            print(f"  [错误] {code} - {str(e)}")
            continue
    
    # 打印汇总报告
    print_summary_report(results)


def print_summary_report(results: list):
    """
    打印分析汇总报告
    
    Args:
        results: 分析结果列表
    """
    print("\n" + "="*60)
    print("📊 分析汇总报告")
    print("="*60)
    
    if not results:
        print("没有成功分析的股票")
        return
    
    # 分类统计
    buy_signals = [r for r in results if r.overall_signal == 'BUY']
    sell_signals = [r for r in results if r.overall_signal == 'SELL']
    neutral_signals = [r for r in results if r.overall_signal == 'NEUTRAL']
    
    print(f"\n总计分析: {len(results)} 只股票")
    print(f"  📈 买入信号: {len(buy_signals)} 只")
    print(f"  📉 卖出信号: {len(sell_signals)} 只")
    print(f"  ➡️  中性信号: {len(neutral_signals)} 只")
    
    # 买入机会（按置信度排序）
    if buy_signals:
        print("\n" + "="*60)
        print("📈 【买入机会】（按置信度排序）")
        print("="*60)
        for r in sorted(buy_signals, key=lambda x: x.confidence, reverse=True):
            print(f"  {r.code:8s} {r.name:12s} | 当前价: {r.current_price:8.2f} | 置信度: {r.confidence:3d}%")
            # 显示最强偏离信号
            strongest = max(r.signals, key=lambda s: abs(s.deviation_pct) if s.signal == 'BUY' else 0)
            if strongest.signal == 'BUY':
                print(f"           └─ {strongest.reason}")
    
    # 卖出提示（按置信度排序）
    if sell_signals:
        print("\n" + "="*60)
        print("📉 【卖出提示】（按置信度排序）")
        print("="*60)
        for r in sorted(sell_signals, key=lambda x: x.confidence, reverse=True):
            print(f"  {r.code:8s} {r.name:12s} | 当前价: {r.current_price:8.2f} | 置信度: {r.confidence:3d}%")
            # 显示最强偏离信号
            strongest = max(r.signals, key=lambda s: abs(s.deviation_pct) if s.signal == 'SELL' else 0)
            if strongest.signal == 'SELL':
                print(f"           └─ {strongest.reason}")
    
    # 中性观望
    if neutral_signals:
        print("\n" + "="*60)
        print("➡️  【中性观望】")
        print("="*60)
        for r in neutral_signals:
            print(f"  {r.code:8s} {r.name:12s} | 当前价: {r.current_price:8.2f}")
    
    print("\n" + "="*60)
    print("⚠️  风险提示：本分析仅供参考，不构成投资建议")
    print("="*60 + "\n")


def main():
    """主函数"""
    if len(sys.argv) > 1:
        if sys.argv[1] == '--batch':
            # 批量分析模式
            threshold = float(sys.argv[2]) if len(sys.argv) > 2 else 1.5
            batch_analyze_with_real_data(threshold=threshold)
        else:
            # 单股分析模式
            code = sys.argv[1]
            name = sys.argv[2] if len(sys.argv) > 2 else None
            threshold = float(sys.argv[3]) if len(sys.argv) > 3 else 1.5
            analyze_single_stock(code, name, threshold)
    else:
        print("用法:")
        print("  单股分析: python ma_deviation_real_example.py <股票代码> [股票名称] [阈值]")
        print("  批量分析: python ma_deviation_real_example.py --batch [阈值]")
        print()
        print("示例:")
        print("  python ma_deviation_real_example.py 600519 贵州茅台")
        print("  python ma_deviation_real_example.py --batch 1.5")
        print()
        print("默认使用配置文件中的股票列表进行批量分析...")
        batch_analyze_with_real_data()


if __name__ == "__main__":
    main()
