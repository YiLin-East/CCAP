import json
import os
import time
from datetime import datetime, timedelta
import akshare as ak
import pandas as pd

# 数据存储路径
DATA_DIR = os.path.join(os.getcwd(), "stock_data")

# 确保数据目录存在
os.makedirs(DATA_DIR, exist_ok=True)

class AdvancedStockFetcher:
    def __init__(self):
        pass  # akshare无需初始化
    
    def fetch_stock_data(self, symbol, months=6, start_date_str=None, end_date_str=None):
        """
        获取指定股票的历史数据
        
        Parameters:
        symbol: 股票代码，如'002050.SZ'
        months: 获取月数，默认6个月
        start_date_str: 起始日期字符串，格式YYYYMMDD
        end_date_str: 结束日期字符串，格式YYYYMMDD
        """
        try:
            if start_date_str and end_date_str:
                # 使用用户指定的起止日期
                start_date = datetime.strptime(start_date_str, '%Y%m%d')
                end_date = datetime.strptime(end_date_str, '%Y%m%d')
            else:
                # 计算时间范围（默认为过去N个月）
                end_date = datetime.now()
                start_date = end_date - timedelta(days=months*30)
            
            # 格式化日期
            start_date_str = start_date.strftime('%Y%m%d')
            end_date_str = end_date.strftime('%Y%m%d')
            
            # 使用 akshare 获取A股数据
            try:
                # akshare获取A股日线数据
                stock_code = symbol.replace('.SZ', '').replace('.SH', '')
                df = ak.stock_zh_a_hist(
                    symbol=stock_code,
                    period="daily",
                    start_date=start_date.strftime('%Y%m%d'),
                    end_date=end_date.strftime('%Y%m%d')
                )
                
                if df.empty:
                    raise ValueError("akshare返回数据为空")
                    
                # 打印前几行数据用于调试
                print(f"akshare返回的数据示例:\n{df.head()}")
                
            except Exception as e:
                raise ValueError(f"通过akshare获取股票数据失败: {str(e)}")
            
            # 检查是否获取到数据
            if df.empty:
                raise ValueError(f"未找到股票代码 {symbol} 的数据")
            
            # 获取股票名称（通过 symbol 映射）
            name_map = {
                "002050.SZ": "三花智控",
                # 可扩展其他股票映射
            }
            # 当前不使用股票名称，直接使用代码作为标识
            stock_name = symbol
            
            # akshare返回的数据已有'日期'列，无需重置索引
            df.rename(columns={'日期': 'trade_date'}, inplace=True)
            # 将日期转换为字符串并移除分隔符
            df['trade_date'] = df['trade_date'].astype(str).str.replace('-', '', regex=False)
            
            # yfinance已在此前获取数据，无需重复获取
            
            # 按日期排序
            df = df.sort_values('trade_date').reset_index(drop=True)
            
            # 计算技术指标，akshare字段名为'收盘'

            
            # 转换为字典列表
            data_list = []
            for index, row in df.iterrows():
                data_point = {
                    "date": row['trade_date'],
                    "open": float(row['开盘']),
                    "high": float(row['最高']),
                    "low": float(row['最低']),
                    "close": float(row['收盘']),
                    "volume": int(row['成交量']),  # akshare成交量单位为手，需转换
                    "turnover": float(row['成交额']),  # akshare直接提供成交额
                    "change_percent": float(row['涨跌幅']) if not pd.isna(row['涨跌幅']) else None,  # akshare提供涨跌幅
                    
                }
                data_list.append(data_point)
            
            # 构建文件名
            first_date = data_list[0]["date"] if data_list else datetime.now().strftime("%Y%m%d")
            last_date = data_list[-1]["date"] if data_list else datetime.now().strftime("%Y%m%d")
            filename = f"{symbol}_{first_date}_{last_date}.json"
            filepath = os.path.join(DATA_DIR, filename)
            
            # 增量更新检查
            existing_data = []
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    try:
                        existing_data = json.load(f)
                        # 如果已有数据，找到最新日期
                        if existing_data:
                            latest_date = max(item["date"] for item in existing_data)
                            # 过滤掉已存在的数据
                            new_data = [item for item in data_list if item["date"] > latest_date]
                            # 合并数据
                            data_list = existing_data + new_data
                    except json.JSONDecodeError:
                        pass  # 文件为空或损坏，直接覆盖
            
            # 保存数据
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data_list, f, ensure_ascii=False, indent=2)
            
            print(f"成功获取 {len(data_list)} 条数据，保存至 {filepath}")
            return data_list
            
        except Exception as e:
            print(f"获取股票数据时发生错误: {str(e)}")
            raise

def main():
    # 示例：获取AAPL股票数据
    fetcher = AdvancedStockDataFetcher()
    
    # 增量更新数据
    fetcher.update_incrementally()

if __name__ == "__main__":
    main()