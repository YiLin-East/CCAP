#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from advanced_stock_fetcher import AdvancedStockFetcher

def main():
    parser = argparse.ArgumentParser(description="股票数据获取工具")
    parser.add_argument(
        "action",
        choices=["fetch"],
        help="执行操作: fetch(获取数据)"
    )
    parser.add_argument(
        "--symbol",
        "-s",
        default='002050.SZ',
        help="股票代码，例如: AAPL, 000001.SZ"
    )
    parser.add_argument(
        "--months",
        "-m",
        type=int,
        default=6,
        help="获取数据的月数，默认为6（半年）"
    )
    
    args = parser.parse_args()
    
    fetcher = AdvancedStockFetcher()
    
    if args.action == "fetch":
        fetcher.fetch_stock_data(args.symbol, args.months)

if __name__ == "__main__":
    main()