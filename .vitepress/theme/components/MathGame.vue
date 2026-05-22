<template>
  <div class="v5-body">
    <div class="container">
      <div class="v5-header">
        <div class="muse-mark-wrapper">
          <div class="muse-mark-logo"></div>
          <div class="muse-mark-text">Nightingale's Melody</div>
          <h2>庄园解密：强制去括号特训 (负数全开版)</h2>
        </div>
      </div>
      
      <div class="rule-banner">
        <span>⚠️ 庄园新法则：注意！第一个数可能会变成<b>负数</b>！必须先写出去括号算式（如输入 -15-6+3 ），再计算结果！</span>
      </div>

      <div class="menu-box">
        <div>
          <label for="q-count">选择题量：</label>
          <select id="q-count" v-model.number="selectedCount" :disabled="isGraded">
            <option :value="5">5 题 (快速破译)</option>
            <option :value="10">10 题 (标准破译)</option>
          </select>
        </div>
        <button @click="generateQuiz">换一批新题</button>
      </div>

      <div class="quiz-container">
        <div v-for="(item, i) in currentQuestions" :key="i" class="quiz-item">
          <div class="q-title">第 {{ i + 1 }} 题：<span class="origin-q">{{ item.questionText }}</span></div>
          
          <div class="step-line">
            <span class="step-label">1. 去括号:</span>
            <input 
              type="text" 
              class="input-text" 
              v-model="userSteps[i]"
              placeholder="如: -17-6+2"
              :disabled="isGraded"
            >
          </div>

          <div class="step-line">
            <span class="step-label">2. 算结果:</span>
            <input 
              type="number" 
              class="input-ans" 
              v-model.number="userAnswers[i]"
              placeholder="答案"
              :disabled="isGraded"
            >
          </div>

          <div v-if="isGraded && feedbacks[i]" class="feedback" :class="feedbacks[i].isCorrect ? 'correct' : 'wrong'">
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
        <p style="color: #555; margin: 5px 0 0 0; font-size: 14px;">负数去括号是初中数学的终极基本功，继续加油！</p>
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
              <td>{{ item.correct }}</td>
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

const selectedCount = ref(5)
const currentQuestions = ref([])
const userSteps = ref([])      
const userAnswers = ref([])    
const feedbacks = ref([])
const isGraded = ref(false)
const finalScore = ref(0)
const historyList = ref([])

function getRandomInt(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min
}

// AI 核心出题引擎：完美注入首位负数逻辑
function generateQuiz() {
  currentQuestions.value = []
  userSteps.value = []
  userAnswers.value = []
  feedbacks.value = []
  isGraded.value = false
  finalScore.value = 0

  while (currentQuestions.value.length < selectedCount.value) {
    const type = getRandomInt(1, 2)
    
    // 💥 升级点：50% 概率让第一个数 a 蜕变为负数
    let a = getRandomInt(10, 25)
    if (Math.random() < 0.5) {
      a = -a
    }

    const b = getRandomInt(5, 12)
    const c = getRandomInt(1, 4)
    
    let questionText = ''
    let correctStep = '' 
    let answer = 0

    if (type === 1) { 
      // 模型一：a - (b - c) --> 去括号后：a - b + c
      questionText = `${a} - (${b} - ${c})`
      correctStep = `${a}-${b}+${c}`
      answer = a - b + c
    } else { 
      // 模型二：a - (b + c) --> 去括号后：a - b - c
      questionText = `${a} - (${b} + ${c})`
      correctStep = `${a}-${b}-${c}`
      answer = a - b - c
    }

    // 格式化一下正数开头的显示（例如把 --12 这种概率规避，确保公式优美）
    // 经过上面的规则调整，questionText 会完美呈现如 "-15 - (8 - 2)"
    currentQuestions.value.push({ questionText, correctStep, answer })
  }
}

function gradeQuiz() {
  let correctCount = 0
  const count = currentQuestions.value.length
  feedbacks.value = []

  for (let i = 0; i < count; i++) {
    // 过滤用户输入中的空格，并且把多余的 +- 号连消（防止小侦探输入 +- 绕过）
    const userStepClean = String(userSteps.value[i] || '').replace(/\s+/g, '').replace(/\+\-/g, '-').replace(/\-\+/g, '-')
    const userAnsClean = parseInt(userAnswers.value[i])
    
    const targetStep = currentQuestions.value[i].correctStep
    const targetAns = currentQuestions.value[i].answer

    if (userStepClean === targetStep && userAnsClean === targetAns) {
      correctCount++
      feedbacks.value[i] = { text: '● 成功破译机关！', isCorrect: true }
    } else if (userStepClean !== targetStep && userAnsClean === targetAns) {
      feedbacks.value[i] = { text: `✕ 偷懒警告：你没正常去括号！应填: ${targetStep}`, isCorrect: false }
    } else {
      feedbacks.value[i] = { text: `✕ 触发机关！正确步骤: ${targetStep} = ${targetAns}`, isCorrect: false }
    }
  }

  finalScore.value = Math.round((correctCount / count) * 100)
  isGraded.value = true

  saveToHistory(count, correctCount, finalScore.value)
}

function saveToHistory(total, correct, score) {
  if (typeof window === 'undefined') return
  const now = new Date()
  const timeStr = `${now.getMonth() + 1}/${now.getDate()} ${now.getHours()}:${String(now.getMinutes()).padStart(2, '0')}`
  let history = JSON.parse(localStorage.getItem('v5_step_history_v2') || '[]')
  history.unshift({ time: timeStr, total, correct, score })
  localStorage.setItem('v5_step_history_v2', JSON.stringify(history))
  historyList.value = history
}

function renderHistory() {
  if (typeof window !== 'undefined') {
    historyList.value = JSON.parse(localStorage.getItem('v5_step_history_v2') || '[]')
  }
}

function clearHistory() {
  if (confirm('确定要清空所有的历史记录吗？')) {
    localStorage.removeItem('v5_step_history_v2')
    historyList.value = []
  }
}

onMounted(() => {
  generateQuiz()
  renderHistory()
})
</script>

<style scoped>
/* 样式保持不变，完美适配第五人格羊皮纸风格 */
.v5-body { background-color: #1a1612; padding: 15px; border-radius: 12px; margin: 20px 0; }
.container { max-width: 750px; margin: 10px auto; background-color: #f4ecd8; padding: 25px; border-radius: 8px; border: 6px double #4a0404; color: #333; }
.v5-header { text-align: center; border-bottom: 4px dashed #4a0404; padding-bottom: 15px; margin-bottom: 20px; }
.muse-mark-wrapper { display: flex; flex-direction: column; align-items: center; }
.muse-mark-logo { width: 60px; height: 60px; background-repeat: no-repeat; background-position: center; background-size: contain; background-image: url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0iIzRhMDQwNCI+PHBhdGggZD0iTTEyIDJDMi40IDIgMiA4IDIgMTJzLjQgMTAgMTAgMTAgMTAtNCAxMC0xMFMyMS42IDIgMTIgMk0xMiAxMGMuNTUgMCAxIC40NSAxIDFTMTIgMTIgMTIgMTJzLTEtLjQ1LTEtMVMxMS40NSAxMCAxMiAxME04IDE2Yy41NSAwIDEgLjQ1IDEgMXMtLjQ1IDEtMSAxLTEtLjQ1LTEtMVN3LjQ1IDE2IDggMTZNMTYgMTZjLjSuNSAwIDEgLjQ1IDEgMXMtLjQ1IDEtMSAxLTEtLjQ1LTEtMVUzMTUuNDUgMTYgMTYgMTZNOC41NSA3LjU1TDkgMTVoMS40NWwtLjQ1LTIuNDVjLS4yLTEuMS0xLjM1LTEuOC0yLjQ1LTEuNTUtNy41LjYtMS4yLj打不开...'); filter: drop-shadow(0 0 5px #4a0404); }
.muse-mark-text { color: #4a0404; font-size: 11px; font-weight: bold; letter-spacing: 1px; }
.v5-header h2 { color: #4a0404 !important; margin: 10px 0 0 0 !important; font-size: 22px !important; border-top: 2px dashed #4a0404 !important; border-bottom: none !important; padding-top: 5px; }

.rule-banner { background: #e6ceb8; border: 1px solid #4a0404; padding: 10px; border-radius: 4px; margin-bottom: 20px; color: #4a0404; font-size: 14px; text-shadow: none; }
.menu-box { display: flex; justify-content: space-between; align-items: center; background: #e2d6b5; padding: 12px 20px; border-radius: 6px; margin-bottom: 25px; border: 1px solid #c4b593; }

.quiz-container { display: grid; grid-template-columns: 1fr; gap: 20px; }
@media(min-width: 600px) { .quiz-container { grid-template-columns: 1fr 1fr; } }

.quiz-item { background: rgba(74, 4, 4, 0.04); padding: 15px; border-radius: 6px; border: 1px solid #c4b593; display: flex; flex-direction: column; gap: 10px; }
.q-title { font-size: 15px; font-weight: bold; color: #4a0404; }
.origin-q { font-size: 20px; color: #111; font-family: monospace; font-weight: bold; }

.step-line { display: flex; align-items: center; justify-content: space-between; gap: 10px; }
.step-label { font-size: 14px; color: #555; }

.input-text, .input-ans { padding: 5px; font-size: 16px; border: 2px solid #4a0404; background: #fffaf0; color: #4a0404; border-radius: 4px; font-weight: bold; }
.input-text { width: 150px; text-align: left; }
.input-ans { width: 80px; text-align: center; }

.input-text:disabled, .input-ans:disabled { background: #e2d6b5; }
.feedback { font-size: 13px; font-weight: bold; margin-top: 5px; padding-top: 5px; border-top: 1px dotted #c4b593; }
.correct { color: #2d5a27; }
.wrong { color: #b80d0d; }

#result-panel { text-align: center; margin-top: 25px; padding: 20px; background: #e2d6b5; border: 2px solid #4a0404; border-radius: 6px; }
#score-display { font-size: 26px; font-weight: bold; color: #4a0404; }

.history-section { margin-top: 35px; border-top: 2px dashed #4a0404; padding-top: 20px; }
.history-title { font-size: 16px; color: #4a0404; font-weight: bold; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center; }
table { width: 100%; border-collapse: collapse; background: #fffaf0; font-size: 14px; }
th, td { border: 1px solid #c4b593 !important; padding: 10px; text-align: center; }
th { background: #4a0404 !important; color: #f4ecd8 !important; }
td { background: transparent !important; }
.btn-clear { padding: 4px 10px; font-size: 12px; background: #718096; border: none; color: #fff; border-radius: 4px; cursor: pointer; }
</style>