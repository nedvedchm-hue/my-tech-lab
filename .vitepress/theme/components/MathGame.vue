<template>
  <div class="v5-body">
    <div class="container">
      <div class="v5-header">
        <div class="muse-mark-wrapper">
          <div class="muse-mark-logo"></div>
          <div class="muse-mark-text">Nightingale's Melody</div>
          <h2>庄园解密：去括号与符号特训</h2>
        </div>
      </div>
      
      <div class="menu-box">
        <div>
          <label for="q-count">选择题量：</label>
          <select id="q-count" v-model.number="selectedCount" :disabled="isGraded">
            <option :value="5">5 题 (快速破译)</option>
            <option :value="10">10 题 (标准破译)</option>
            <option :value="20">20 题 (极限挑战)</option>
          </select>
        </div>
        <button @click="generateQuiz">换一批新题</button>
      </div>

      <div class="quiz-container">
        <div v-for="(item, i) in currentQuestions" :key="i" class="quiz-item">
          <div class="q-line">
            <span class="question-text">{{ i + 1 }}. &nbsp;{{ item.questionText }} =</span>
            <input 
              type="number" 
              class="input-ans" 
              v-model.number="userAnswers[i]"
              :disabled="isGraded"
            >
          </div>
          <div 
            v-if="feedbacks[i]" 
            class="feedback" 
            :class="feedbacks[i].isCorrect ? 'correct' : 'wrong'"
          >
            {{ feedbacks[i].text }}
          </div>
        </div>
      </div>

      <div style="margin-top: 30px;">
        <button 
          v-if="!isGraded" 
          @click="gradeQuiz" 
          style="width: 100%; padding: 12px; font-size: 18px;"
        >
          提交密文，查看破译结果
        </button>
      </div>

      <div v-if="isGraded" id="result-panel">
        <div id="score-display">最终得分：{{ finalScore }} 分</div>
        <p style="color: #555; margin: 5px 0 0 0; font-size: 14px;">数据已写入下方的“庄园破译日记”</p>
      </div>

      <div class="history-section">
        <div class="history-title">
          <span>📖 庄园破译日记 (历史留存)</span>
          <button class="btn-clear" @click="clearHistory">清空记录</button>
        </div>
        <table id="history-table">
          <thead>
            <tr>
              <th>破译时间</th>
              <th>总题数</th>
              <th>答对题数</th>
              <th>最终得分</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item, idx) in historyList" :key="idx">
              <td>{{ item.time }}</td>
              <td>{{ item.total }}</td>
              <td :style="{ color: item.correct === item.total ? '#2d5a27' : '#333', fontWeight: 'bold' }">
                {{ item.correct }}
              </td>
              <td :style="{ fontWeight: 'bold', color: item.score >= 80 ? '#2d5a27' : '#b80d0d' }">
                {{ item.score }} 分
              </td>
            </tr>
            <tr v-if="historyList.length === 0">
              <td colspan="4" style="color: #888;">暂无侦探破译记录</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

// 状态控制
const selectedCount = ref(10)
const currentQuestions = ref([])
const userAnswers = ref([])
const feedbacks = ref([])
const isGraded = ref(false)
const finalScore = ref(0)
const historyList = ref([])

// 工具函数：获取随机整数
function getRandomInt(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min
}

// 核心自适应逻辑：利用 Set 生成完全不重复的四种题型
function generateQuiz() {
  currentQuestions.value = []
  userAnswers.value = []
  feedbacks.value = []
  isGraded.value = false
  finalScore.value = 0

  const usedQuestions = new Set()

  while (currentQuestions.value.length < selectedCount.value) {
    const type = getRandomInt(1, 4)
    let questionText = ''
    let answer = 0

    if (type === 1) { // a - (b - c)
      const a = getRandomInt(12, 25)
      const b = getRandomInt(6, 9)
      const c = getRandomInt(1, 5)
      questionText = `${a} - (${b} - ${c})`
      answer = a - (b - c)
    } else if (type === 2) { // a - (b + c)
      const a = getRandomInt(12, 25)
      const b = getRandomInt(4, 8)
      const c = getRandomInt(1, 4)
      questionText = `${a} - (${b} + ${c})`
      answer = a - (b + c)
    } else if (type === 3) { // -a - b
      const a = getRandomInt(1, 9)
      const b = getRandomInt(1, 9)
      questionText = `-${a} - ${b}`
      answer = -a - b
    } else { // -a + b
      const a = getRandomInt(6, 12)
      const b = getRandomInt(1, 5)
      questionText = `-${a} + ${b}`
      answer = -a + b
    }

    if (!usedQuestions.has(questionText)) {
      usedQuestions.add(questionText)
      currentQuestions.value.push({ questionText, answer })
    }
  }
}

// 批量提交并检查得分
function gradeQuiz() {
  let correctCount = 0
  const count = currentQuestions.value.length
  feedbacks.value = []

  for (let i = 0; i < count; i++) {
    const userVal = parseInt(userAnswers.value[i])
    const realAns = currentQuestions.value[i].answer

    if (userVal === realAns) {
      correctCount++
      feedbacks.value[i] = {
        text: '● 成功破解',
        isCorrect: true
      }
    } else {
      feedbacks.value[i] = {
        text: `✕ 触发机关 (正确答案: ${realAns})`,
        isCorrect: false
      }
    }
  }

  finalScore.value = Math.round((correctCount / count) * 100)
  isGraded.value = true

  // 写入历史持久化记录
  saveToHistory(count, correctCount, finalScore.value)
}

// 持久化存储到浏览器
function saveToHistory(total, correct, score) {
  if (typeof window === 'undefined') return
  const now = new Date()
  const timeStr = `${now.getMonth() + 1}/${now.getDate()} ${now.getHours()}:${String(now.getMinutes()).padStart(2, '0')}`
  
  let history = JSON.parse(localStorage.getItem('v5_math_history') || '[]')
  history.unshift({ time: timeStr, total, correct, score })
  if (history.length > 15) history.pop()
  localStorage.setItem('v5_math_history', JSON.stringify(history))
  historyList.value = history
}

// 渲染读取缓存历史
function renderHistory() {
  if (typeof window !== 'undefined') {
    historyList.value = JSON.parse(localStorage.getItem('v5_math_history') || '[]')
  }
}

// 清空历史数据
function clearHistory() {
  if (confirm('确定要烧毁（清空）所有的破译日记记录吗？')) {
    localStorage.removeItem('v5_math_history')
    historyList.value = []
  }
}

// Vue 挂载钩子，接管原生 window.onload 行为
onMounted(() => {
  generateQuiz()
  renderHistory()
})
</script>

<style scoped>
/* 完美隔离全局样式的仿古暗黑庄园风格 */
.v5-body {
  background-color: #1a1612; /* 密室暗色背景 */
  padding: 15px;
  border-radius: 12px;
  margin: 20px 0;
}

.container {
  max-width: 750px;
  margin: 10px auto;
  background-color: #f4ecd8; /* 经典老旧羊皮纸色 */
  padding: 25px;
  border-radius: 8px;
  border: 6px double #4a0404; /* 哥特风双边框 */
  box-shadow: 0 10px 30px rgba(0,0,0,0.5);
  color: #333;
}

.v5-header {
  text-align: center;
  border-bottom: 4px dashed #4a0404;
  padding-bottom: 15px;
  margin-bottom: 25px;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.muse-mark-wrapper {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
}

.muse-mark-logo {
  width: 75px;
  height: 75px;
  background-repeat: no-repeat;
  background-position: center;
  background-size: contain;
  background-image: url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0iIzRhMDQwNCI+PHBhdGggZD0iTTEyIDJDMi40IDIgMiA4IDIgMTJzLjQgMTAgMTAgMTAgMTAtNCAxMC0xMFMyMS42IDIgMTIgMk0xMiAxMGMuNTUgMCAxIC40NSAxIDFTMTIgMTIgMTIgMTJzLTEtLjQ1LTEtMVMxMS40NSAxMCAxMiAxME04IDE2Yy41NSAwIDEgLjQ1IDEgMXMtLjQ1IDEtMSAxLTEtLjQ1LTEtMVN3LjQ1IDE2IDggMTZNMTYgMTZjLjSuNSAwIDEgLjQ1IDEgMXMtLjQ1IDEtMSAxLTEtLjQ1LTEtMVUzMTUuNDUgMTYgMTYgMTZNOC41NSA3LjU1TDkgMTVoMS40NWwtLjQ1LTIuNDVjLS4yLTEuMS0xLjM1LTEuOC0yLjQ1LTEuNTUtNy41LjYtMS4yLjgtMS40NSAxLjU1ek0xMSAxMi4xNUw4IDE5aDNsMy02Ljg1TDExIDEyLjE1eiIvPjwvc3ZnPg==');
  filter: drop-shadow(0 0 5px #4a0404);
  opacity: 0.9;
}

.muse-mark-text {
  color: #4a0404;
  font-size: 11px;
  font-weight: bold;
  font-family: 'Arial Narrow', sans-serif;
  margin-top: -2px;
  letter-spacing: 1px;
  text-transform: uppercase;
}

.v5-header h2 {
  color: #4a0404 !important;
  margin: 10px 0 0 0 !important;
  font-size: 24px !important;
  letter-spacing: 1px;
  border-top: 2px dashed #4a0404 !important;
  border-bottom: none !important;
  padding-top: 5px;
  background: transparent !important;
}

/* 顶部剪影装饰 */
.v5-header::before, .v5-header::after {
  content: '';
  display: block;
  width: 50px;
  height: 50px;
  background-repeat: no-repeat;
  background-position: center;
  background-size: contain;
  filter: sepia(0.8) contrast(1.2);
  opacity: 0.7;
}

.v5-header::before {
  background-image: url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0iIzRhMDQwNCI+PHBhdGggZD0iTTEyIDJDNi40OCA4IDIgNi40OCA4IDEycy40OCA2IDEwIDEyIDQuNDgtNi40OCA0LjQ4LTYuNDgtNC40OE0xMiAxMGMuNTUgMCAxIC40NSAxIDFTMTIgMTIgMTIgMTJzLTEtLjQ1LTEtMVMxMS40NSAxMCAxMiAxME04IDE2Yy41NSAwIDEgLjQ1IDEgMXMtLjQ1IDEtMSAxLTEtLjQ1LTEtMVN3LjQ1IDE2IDggMTZNMTYgMTZjLjU1IDAgMSAuNDUgMSAxcy0uNDUgMS0xIDEtMS0uNDUtMS0xUzE1LjQ1IDE2IDE2IDE2TTguNTUgNy41NUw5IDEwaDEuNDVsLS40NS0yLjQ1Yy0uMi0xLjEtMS4zNS0xLjgtMi40NS0xLjU1LTcuNS4yLTEuMi44LTEuNDUgMS41NXpNMTEgMTIuMTVMOCAxOWgzbDMtNi44NUwxMSAxMi4xNXoiLz48L3N2Zz4=');
}

.v5-header::after {
  background-image: url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0iIzRhMDQwNCI+PHBhdGggZD0iTTEyIDJDNi40OCA4IDIgNi40OCA4IDEycy40OCA2IDEwIDEyIDQuNDgtNi40OCA0LjQ4LTYuNDgtNC40OE0xMiAxMGMuNTUgMCAxIC40NSAxIDFTMTIgMTIgMTIgMTJzLTEtLjQ1LTEtMVMxMS40NSAxMCAxMiAxME04IDE2Yy41NSAwIDEgLjQ1IDEgMXMtLjQ1IDEtMSAxLTEtLjQ1LTEtMVN3LjQ1IDE2IDggMTZNMTYgMTZjLjU1IDAgMSAuNDUgMSAxcy0uNDUgMS0xIDEtMS0uNDUtMS0xUzE1LjQ1IDE2IDE2IDE2TTguNTUgNy41NUw5IDEwaDEuNDVsLS40NS0yLjQ1Yy0uMi0xLjEtMS4zNS0xLjgtMi40NS0xLjU1LTcuNS4yLTEuMi44LTEuNDUgMS41NXpNMTEgMTIuMTVMOCAxOWgzbDMtNi44NUwxMSAxMi4xNXoiLz48L3N2Zz4=');
  transform: scaleX(-1);
}

.menu-box {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #e2d6b5;
  padding: 12px 20px;
  border-radius: 6px;
  margin-bottom: 25px;
  border: 1px solid #c4b593;
}

label {
  font-weight: bold;
  color: #4a0404;
}

select, button {
  padding: 6px 14px;
  font-size: 15px;
  border-radius: 4px;
  border: 1px solid #4a0404;
  cursor: pointer;
}

select {
  background: #fffaf0;
  color: #333;
}

button {
  background-color: #4a0404;
  color: #f4ecd8;
  font-weight: bold;
  transition: all 0.2s;
}

button:hover {
  background-color: #720606;
  box-shadow: 0 0 8px rgba(114,6,6,0.5);
}

.quiz-container {
  display: grid;
  grid-template-columns: 1fr;
  gap: 15px;
}

@media(min-width: 600px) {
  .quiz-container { grid-template-columns: 1fr 1fr; }
}

.quiz-item {
  background: rgba(74, 4, 4, 0.04);
  padding: 15px;
  border-radius: 6px;
  border: 1px dashed #c4b593;
  display: flex;
  flex-direction: column;
}

.q-line {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.question-text {
  font-size: 18px;
  font-weight: bold;
  color: #2c1a04;
}

.input-ans {
  width: 75px;
  padding: 6px;
  font-size: 18px;
  text-align: center;
  border: 2px solid #4a0404;
  background: #fffaf0;
  color: #4a0404;
  border-radius: 4px;
  font-weight: bold;
}

.input-ans:disabled {
  background: #e2d6b5;
  opacity: 0.8;
}

.feedback {
  margin-top: 8px;
  font-size: 14px;
  font-weight: bold;
}

.correct { color: #2d5a27; }
.wrong { color: #b80d0d; }

#result-panel {
  text-align: center;
  margin-top: 25px;
  padding: 20px;
  background: #e2d6b5;
  border: 2px solid #4a0404;
  border-radius: 6px;
}

#score-display {
  font-size: 26px;
  font-weight: bold;
  color: #4a0404;
}

.history-section {
  margin-top: 35px;
  border-top: 2px dashed #4a0404;
  padding-top: 20px;
}

.history-title {
  font-size: 16px;
  color: #4a0404;
  font-weight: bold;
  margin-bottom: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

table {
  width: 100%;
  border-collapse: collapse;
  background: #fffaf0;
  font-size: 14px;
}

th, td {
  border: 1px solid #c4b593 !important;
  padding: 10px;
  text-align: center;
}

th {
  background: #4a0404 !important;
  color: #f4ecd8 !important;
}

td {
  background: transparent !important;
}

.btn-clear {
  padding: 4px 10px;
  font-size: 12px;
  background: #718096;
  border: none;
}
</style>