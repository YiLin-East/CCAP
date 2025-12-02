import os
import json

# 

# 数据存储路径
DATA_DIR = os.path.join(os.getcwd(), "stock_data")

# 确保数据目录存在
os.makedirs(DATA_DIR, exist_ok=True)

def load_config(config_file: str = "config.json") -> dict:
    """
    加载配置文件
    
    Args:
        config_file: 配置文件路径
    
    Returns:
        配置字典
    """
    if not os.path.exists(config_file):
        # 如果配置文件不存在，创建默认配置
        default_config = {
            
            "data_dir": DATA_DIR
        }
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, ensure_ascii=False, indent=2)
        return default_config
    
    with open(config_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_default_config(config_file: str = "config.json") -> None:
    """
    保存默认配置到文件
    
    :param config_file: 配置文件路径
    """
    import json
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(DEFAULT_CONFIG, f, indent=2, ensure_ascii=False)
    print(f"默认配置已保存到 {config_file}")