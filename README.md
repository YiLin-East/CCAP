# 股票数据获取工具

这是一个用于获取和管理股票数据的Python工具包。

## 功能特性

1. 获取指定股票近半年的数据
2. 以JSON格式保存数据到本地文件
3. 支持增量更新，避免重复获取已有数据
4. 自动填补缺失的日期数据
5. 计算常用技术指标（MA5, MA20, RSI等）

## 安装与初始化

1. 克隆或下载本项目到本地
2. 安装依赖：
   ```
   pip install -r requirements.txt
   ```

3. 初始化项目：
   ```
   python main.py init
   ```

4. 设置配置文件（可选）：
   ```
   python main.py setup-config
   ```

## 使用方法

### 获取股票数据

```
python main.py fetch --symbol STOCK_SYMBOL [--months N]
```

参数说明：
- `STOCK_SYMBOL`: 股票代码，例如 AAPL、000001.SZ 等
- `--months N`: 获取N个月的数据，默认为6个月

示例：
```
python main.py fetch --symbol AAPL
python main.py fetch --symbol 000001.SZ --months 12
```

### 数据格式

获取的数据将以JSON格式保存，每个数据点包含以下字段：

| 字段名 | 类型 | 描述 |
|--------|------|------|
| date | String | 时间戳/日期，ISO 8601格式 |
| open | Number | 开盘价 |
| high | Number | 最高价 |
| low | Number | 最低价 |
| close | Number | 收盘价 |
| volume | Integer | 成交量 |
| turnover | Number | 成交额 |
| change_percent | Number | 涨跌幅百分比 |
| ma5 | Number | 5日移动平均线 |
| ma20 | Number | 20日移动平均线 |
| rsi14 | Number | 14日相对强弱指数 |

## 增量更新机制

该工具支持增量更新，每次运行时会：

1. 检查本地是否已有该股票的数据文件
2. 如果有，则只获取最新的数据并追加到现有数据中
3. 自动去重并保持数据的时间顺序
4. 重新计算技术指标以确保准确性

## 配置文件

可以通过修改 `config.json` 文件来自定义行为：

```json
{
  "data_directory": "./stock_data",
  "default_months": 6,
  "api_settings": {
    "timeout": 30,
    "retry_times": 3
  },
  "technical_indicators": {
    "ma_periods": [5, 20, 60],
    "rsi_period": 14,
    "kdj_period": 9
  }
}
```

## 扩展开发

该项目设计具有良好的扩展性，你可以：

1. 替换 `fetch_real_time_data` 方法以接入真实的股票数据API
2. 修改技术指标计算方法以满足特定需求
3. 添加更多数据验证和清洗功能
4. 集成数据库存储而非JSON文件