<template>
  <div class="world-cup-container">
    <div class="wc-header">
      <div class="trophy-icon">⚽</div>
      <h2>2026 世界杯 · 全自动情报监测站</h2>
      <p class="wc-subtitle">数据每 30 分钟由云端爬虫自动巡检刷新 | 强力驱动</p>
      <p class="time-badge">🕒 最后一波巡检同步时间：{{ wcData.update_time || '正在同步...' }}</p>
    </div>

    <!-- 自动循环渲染比赛卡片 -->
    <div class="match-list">
      <div v-for="(match, idx) in wcData.matches" :key="idx" class="match-card">
        <div class="match-meta">
          <span class="match-time">⏱️ {{ match.time }}</span>
          <span class="status-tag" :class="match.status === '已出首发' ? 'ready' : 'wait'">
            {{ match.status }}
          </span>
        </div>
        
        <div class="vs-line">
          <span class="team-name">{{ match.home }}</span>
          <span class="vs-text">VS</span>
          <span class="team-name">{{ match.away }}</span>
        </div>

        <div class="lineup-box">
          <div class="lineup-side">
            <span class="side-title">🏠 {{ match.home }}首发：</span>
            <p>{{ match.home_lineup }}</p>
          </div>
          <div class="lineup-side">
            <span class="side-title">🚀 {{ match.away }}首发：</span>
            <p>{{ match.away_lineup }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
// 💥 静态导入 Python 爬虫在本地落盘的 JSON 数据
import rawData from '../data/world-cup.json'

const wcData = ref({ update_time: '', matches: [] })

onMounted(() => {
  // 页面加载时，把清洗好的 JSON 报文直接灌入变量中
  if (rawData) {
    wcData.value = rawData
  }
})
</script>

<style scoped>
.world-cup-container { 
  max-width: 800px; 
  margin: 20px auto; 
  padding: 25px; 
  background: linear-gradient(135deg, #114329 0%, #1a5e38 100%); 
  border-radius: 16px; 
  color: #fff; 
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}
.time-badge { font-size: 12px; color: #a2fcd4; background: rgba(0,0,0,0.2); padding: 4px 10px; border-radius: 20px; display: inline-block; margin-top: 10px; }
.match-list { display: flex; flex-direction: column; gap: 20px; margin-top: 20px; }
.match-card { background: rgba(255,255,255,0.08); border-radius: 12px; padding: 20px; border: 1px solid rgba(255,255,255,0.1); }
.match-meta { display: flex; justify-content: space-between; font-size: 13px; color: #ccc; }
.status-tag { padding: 2px 8px; border-radius: 4px; font-weight: bold; font-size: 12px; }
.status-tag.ready { background: #00e676; color: #000; }
.status-tag.wait { background: #ffb300; color: #000; }
.vs-line { display: flex; justify-content: center; align-items: center; gap: 30px; font-size: 22px; font-weight: bold; margin: 15px 0; }
.vs-text { color: #ffeb3b; font-style: italic; font-size: 16px; }
.lineup-box { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; background: rgba(0,0,0,0.15); padding: 15px; border-radius: 8px; font-size: 14px; }
.side-title { font-weight: bold; color: #a2fcd4; display: block; margin-bottom: 5px; }
</style>