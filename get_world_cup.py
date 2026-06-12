import json
import os
import requests
from datetime import datetime

def fetch_sofascore_cloud_data():
    print("📡 正在由 GitHub 海外云端骨干网直接接入 SofaScore 核心数据源...")
    
    # 在云端我们不需要镜像，直接直连官方，因为 GitHub 服务器在海外，没有403封锁！
    today_str = datetime.now().strftime("%Y-%m-%d")
    url = f"https://api.sofascore.com/api/v1/sport/football/scheduled-events/{today_str}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    # 💥 关键一招：直接强行关闭 Python 的本地代理读取，防止本地测试时被墙干扰
    session = requests.Session()
    session.trust_env = False 

    response = session.get(url, headers=headers, timeout=15)
    print(f"🌐 骨干网响应完成，状态码: {response.status_code}")
    
    if response.status_code == 200:
        res_data = response.json()
        cleaned_data = {
            "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " (SofaScore 官方数据真活鱼)",
            "matches": []
        }
        
        # 遍历当天所有比赛
        for event in res_data.get("events", []):
            tournament_name = event.get("tournament", {}).get("name", "")
            
            # 动态匹配世界杯或者今天的测试比赛
            if "World Cup" in tournament_name or True: 
                match_id = event.get("id")
                status_type = event.get("status", {}).get("type") # finished / nst
                
                match_info = {
                    "home": event.get("homeTeam", {}).get("nameTranslations", {}).get("zh", event.get("homeTeam", {}).get("name")),
                    "away": event.get("awayTeam", {}).get("nameTranslations", {}).get("zh", event.get("awayTeam", {}).get("name")),
                    "time": datetime.fromtimestamp(event.get("startTimestamp", 0)).strftime("%H:%M"),
                    "status": "已结束" if status_type == "finished" else "等待首发"
                }
                
                # 如果比赛结束，深入抓取全员评分
                if status_type == "finished":
                    lineup_url = f"https://api.sofascore.com/api/v1/event/{match_id}/lineups"
                    lineup_res = session.get(lineup_url, headers=headers, timeout=10)
                    
                    if lineup_res.status_code == 200:
                        lineup_data = lineup_res.json()
                        
                        # 提取主队全员和 Sofa 真实评分
                        home_players = lineup_data.get("home", {}).get("players", [])
                        home_text = " \n".join([f"• {p['player']['name']}: {p.get('statistics', {}).get('rating', '暂无')}分" for p in home_players if p.get('statistics', {}).get('rating')])
                        
                        # 提取客队全员和 Sofa 真实评分
                        away_players = lineup_data.get("away", {}).get("players", [])
                        away_text = " \n".join([f"• {p['player']['name']}: {p.get('statistics', {}).get('rating', '暂无')}分" for p in away_players if p.get('statistics', {}).get('rating')])
                        
                        match_info["home_lineup"] = f"📊 【SofaScore 赛后全员权威评分】\n{home_text}"
                        match_info["away_lineup"] = f"📊 【SofaScore 赛后全员权威评分】\n{away_text}"
                else:
                    match_info["home_lineup"] = "⏱️ 赛前 60 分钟自动解锁首发名单"
                    match_info["away_lineup"] = "⏱️ 赛前 60 分钟自动解锁首发名单"
                    
                cleaned_data["matches"].append(match_info)
        
        # 写入 JSON
        data_dir = './.vitepress/theme/data'
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        with open(f'{data_dir}/world-cup.json', 'w', encoding='utf-8') as f:
            json.dump(cleaned_data, f, ensure_ascii=False, indent=2)
            
        print(f"💾 [云端封包成功] 成功洗出今日 {len(cleaned_data['matches'])} 场球赛真实 Sofa 评分清单！")
    else:
        raise Exception(f"SofaScore 核心接口拒绝响应，状态码: {response.status_code}")

if __name__ == "__main__":
    fetch_sofascore_cloud_data()