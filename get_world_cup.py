import json
import os
import requests

def fetch_world_cup_data():
    print("📡 启动世界杯数据前线巡检...")
    
    # 这里我们模拟/调用一个公开的体育数据开源网关，或者解析特定无防御的公开体育数据源
    # 为了演示自动化闭环，我们先让它自动生成今天的比赛队列数据
    #（真实环境下可以用 requests.get 获取真实 API）
    
    mock_data = {
        "update_time": "2026-06-12 01:00:00",
        "matches": [
            {
                "home": "加拿大",
                "away": "波黑",
                "status": "已出首发",
                "time": "明早 06:00",
                "home_lineup": "戴维、拉林、布坎南、科内、奥斯塔基奥",
                "away_lineup": "哲科、皮亚尼奇、克鲁尼奇、艾哈迈德霍季奇"
            },
            {
                "home": "美国",
                "away": "巴拉圭",
                "status": "等待首发",
                "time": "明早 08:30",
                "home_lineup": "预计赛前60分钟解锁",
                "away_lineup": "预计赛前60分钟解锁"
            }
        ]
    }
    
    # 自动把抓到的数据清洗，并写入到项目的前端数据目录下
    # 确保保存路径在你的 components 容易读取的地方
    data_dir = './.vitepress/theme/data'
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        
    with open(f'{data_dir}/world-cup.json', 'w', encoding='utf-8') as f:
        json.dump(mock_data, f, ensure_ascii=False, indent=2)
        
    print("✅ 数据清洗完毕，world-cup.json 已封包！")

if __name__ == "__main__":
    fetch_world_cup_data()