import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any

class StockDataFetcher:
    def __init__(self, stock_symbol: str, data_file: str = None):
        """
        初始化股票数据获取器
        
        :param stock_symbol: 股票代码
        :param data_file: 数据存储文件路径
        """
        self.stock_symbol = stock_symbol
        self.data_file = data_file or f"{stock_symbol}_data.json"
        
    def fetch_historical_data(self, months: int = 6) -> List[Dict[str, Any]]:
        """
        获取指定月份的历史数据（模拟实现）
        实际应用中应该连接到真实的股票数据API
        
        :param months: 获取几个月的数据
        :return: 股票数据列表
        """
        # 这里是模拟数据生成，实际应替换为真实API调用
        # 比如可以使用 yfinance, tushare, akshare 等库获取真实数据
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=months*30)
        
        # 模拟生成数据
        data = []
        current_date = start_date
        open_price = 100.0  # 初始价格
        
        while current_date <= end_date:
            # 生成模拟的K线数据
            open_price = round(open_price * (1 + (0.05 - 0.1 * 0.5)), 2)  # 随机波动
            
            # 保证high >= open >= low 或 high >= close >= low 的逻辑关系
            high = round(open_price * (1 + 0.03), 2)
            low = round(open_price * (1 - 0.02), 2)
            close = round(low + (high - low) * 0.7, 2)  # 收盘价在高低之间
            volume = int(1000000 + 2000000 * 0.5)  # 随机成交量
            turnover = round(volume * close / 100, 2)  # 成交额
            
            # 计算涨跌幅百分比
            if len(data) > 0:
                prev_close = data[-1]['close']
                change_percent = round((close - prev_close) / prev_close * 100, 2)
            else:
                change_percent = 0.0
                
            # 添加技术指标（简化计算）
            ma5 = round(sum([d['close'] for d in data[-4:]] + [close]) / min(len(data)+1, 5), 2)
            ma20 = round(sum([d['close'] for d in data[-19:]] + [close]) / min(len(data)+1, 20), 2)
            
            # 简化的RSI计算（实际应该更复杂）
            rsi14 = round(50 + 10 * (0.5 - 0.5), 2)  # 简化处理
            
            data.append({
                "date": current_date.isoformat(),
                "open": open_price,
                "high": high,
                "low": low,
                "close": close,
                "volume": volume,
                "turnover": turnover,
                "change_percent": change_percent,
                "ma5": ma5,
                "ma20": ma20,
                "rsi14": rsi14
            })
            
            # 移动到下一个时间点（这里按天移动，可根据需要调整）
            current_date += timedelta(days=1)
            
        return data
    
    def save_data(self, data: List[Dict[str, Any]]) -> None:
        """
        将数据保存到JSON文件
        
        :param data: 要保存的股票数据
        """
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def load_existing_data(self) -> List[Dict[str, Any]]:
        """
        加载已有的数据
        
        :return: 已存在的股票数据列表
        """
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def get_latest_date(self, data: List[Dict[str, Any]]) -> datetime:
        """
        获取数据中的最新日期
        
        :param data: 股票数据列表
        :return: 最新日期
        """
        if not data:
            return None
        
        # 假设数据按日期排序
        latest_entry = data[-1]
        return datetime.fromisoformat(latest_entry['date'])
    
    def update_data(self) -> None:
        """
        更新数据（增量方式）
        """
        # 加载已有数据
        existing_data = self.load_existing_data()
        
        # 确定开始日期
        if existing_data:
            latest_date = self.get_latest_date(existing_data)
            # 从最后一条数据的后一天开始获取数据
            start_date = latest_date + timedelta(days=1)
        else:
            # 如果没有历史数据，则获取最近6个月的数据
            start_date = datetime.now() - timedelta(days=180)
            
        # 这里应该调用实际的API来获取从start_date开始到现在的数据
        # 作为示例，我们仍然使用模拟数据
        new_data = self.fetch_historical_data(6)
        
        # 合并数据
        # 在实际实现中，这里应该是合并现有数据和新增数据
        all_data = existing_data + new_data
        
        # 去重和排序（确保数据正确顺序）
        unique_data = {item['date']: item for item in all_data}
        sorted_data = sorted(unique_data.values(), key=lambda x: x['date'])
        
        # 保存更新后的数据
        self.save_data(sorted_data)
        
        print(f"数据已更新，共 {len(sorted_data)} 条记录")

def main():
    # 示例：获取AAPL股票数据
    fetcher = StockDataFetcher("AAPL")
    
    # 获取并保存半年的数据
    data = fetcher.fetch_historical_data(6)
    fetcher.save_data(data)
    print(f"已保存 {len(data)} 条股票数据到 {fetcher.data_file}")

if __name__ == "__main__":
    main()