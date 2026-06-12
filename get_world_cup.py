import json
import os
import requests
from datetime import datetime

def fetch_real_world_cup_live_data():
    print("📡 [接口割接] 正在连接国际公开体育网关...")
    
    # 💥 开源世界杯比赛数据网关
    url = "https://raw.githubusercontent.com/openfootball/world-cup-data/master/2026/matches-today.json"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        print(f"🌐 骨干网物理层连通，网关返回状态码: {response.status_code}")
        
        # 🟢 如果成功拿到公开接口的数据（状态码200）
        if response.status_code == 200:
            res_data = response.json()
            matches_list = res_data.get("matches", [])
            
            # 如果接口里真的有赛事数据，走纯全自动清洗
            if matches_list:
                cleaned_data = {
                    "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " (🤖 纯网络全自动抓取)", # 💥 真伪防伪码1
                    "matches": []
                }
                for item in matches_list:
                    match_info = {
                        "home": item.get("home_team_name", "未知球队"),
                        "away": item.get("away_team_name", "未知球队"),
                        "time": item.get("match_time_string", "15:00"),
                        "status": item.get("match_status_display", "等待首发"),
                    }
                    home_players = item.get("home_ratings", [])
                    home_text = " \n".join([f"• {p['name']}: {p['rating']}分" for p in home_players if p.get('rating')])
                    away_players = item.get("away_ratings", [])
                    away_text = " \n".join([f"• {p['name']}: {p['rating']}分" for p in away_players if p.get('rating')])
                    
                    match_info["home_lineup"] = f"📊 【主队全员赛后权威评分】\n{home_text if home_text else '• 官方数据正在同步中...'}"
                    match_info["away_lineup"] = f"📊 【客队全员赛后权威评分】\n{away_text if away_text else '• 官方数据正在同步中...'}"
                    cleaned_data["matches"].append(match_info)
                
                # 写入落盘并结束
                write_to_json(cleaned_data)
                print("💾 [真活鱼] 100%全自动公网数据下载并覆盖成功！")
                return
                
        # 🚨 如果走到这里，说明网络返回了404/520，或者接口数据为空，触发容灾
        print("⚠️ 今日赛事尚未在开源网关建档，下发防伪兜底报文...")
        trigger_fallback()
        
    except Exception as e:
        print(f"❌ 链路中断异常: {e}，触发容灾")
        trigger_fallback()

def trigger_fallback():
    # 💥 如果显示了这套数据，名字里的【本地兜底】会直接把你出卖，绝不作弊！
    backup_data = {
        "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " (⚠️ 触发本地容灾兜底)", # 💥 真伪防伪码2
        "matches": [
            {
                "home": "韩国",
                "away": "捷克",
                "status": "已结束",
                "time": "15:00",
                "home_lineup": "📊 【韩国队全员赛后权威评分】\n• 孙兴慜【本地兜底】: 7.4分\n• 李刚仁【本地兜底】: 7.8分",
                "away_lineup": "📊 【捷克队全员赛后权威评分】\n• 希克【本地兜底】: 6.8分\n• 索切克【本地兜底】: 7.3分"
            }
        ]
    }
    write_to_json(backup_data)

def write_to_json(data):
    data_dir = './.vitepress/theme/data'
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    with open(f'{data_dir}/world-cup.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    fetch_real_world_cup_live_data()