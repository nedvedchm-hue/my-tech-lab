<template>
  <div class="v5-body">
    <div class="container">
      <div class="v5-header">
        <div class="muse-mark-wrapper">
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
            <input type="text" class="input-text" v-model="userSteps[i]" placeholder="如: -17-6+2" :disabled="isGraded">
          </div>

          <div class="step-line">
            <span class="step-label">2. 算结果:</span>
            <input type="number" class="input-ans" v-model.number="userAnswers[i]" placeholder="答案" :disabled="isGraded">
          </div>

          <div v-if="isGraded && feedbacks[i]" class="feedback" :class="feedbacks[i].isCorrect ? 'correct' : 'wrong'">
            {{ feedbacks[i].text }}
          </div>
        </div>
      </div>

      <div style="margin-top: 30px;">
        <button v-if="!isGraded" @click="gradeQuiz" style="width: 100%; padding: 12px; font-size: 18px;">
          提交密文，查看破译结果
        </button>
      </div>

      <div v-if="isGraded" id="result-panel">
        <div id="score-display">最终得分：{{ finalScore }} 分</div>
      </div>

      <div class="history-section">
        <div class="history-title"><span>📖 庄园破译日记</span></div>
        </div>
    </div>

    <div class="ai-assistant-wrapper">
      <div class="ai-badge" @click="toggleChat">
        <div class="badge-icon">🦉</div>
        <div class="badge-text">求助管家</div>
      </div>

      <div v-if="isChatOpen" class="ai-chat-window">
        <div class="chat-header">
          <span>🕵️‍♂️ 庄园数学助教（DeepSeek 驱动）</span>
          <span class="close-btn" @click="toggleChat">✖</span>
        </div>
        <div class="chat-body" ref="chatBodyRef">
          <div class="chat-bubble system">
            你好，小侦探！我是这里的数学管家。做题遇到变号困难或者负数计算迷茫了吗？把题目发给我，我来引导你破解它！
          </div>
          <div v-for="(msg, index) in chatMessages" :key="index" class="chat-bubble" :class="msg.role">
            {{ msg.content }}
          </div>
          <div v-if="isAiLoading" class="chat-bubble system loading">
            管家正在翻阅法典，请稍候...
          </div>
        </div>
        <div class="chat-footer">
          <input 
            type="text" 
            v-model="userMessage" 
            @keyup.enter="sendMessage" 
            placeholder="问问管家：为什么这里要变号？"
            :disabled="isAiLoading"
          >
          <button @click="sendMessage" :disabled="isAiLoading">发送</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'

// 前面的答题状态、getRandomInt、generateQuiz、gradeQuiz 逻辑完美保留
const selectedCount = ref(5)
const currentQuestions = ref([])
const userSteps = ref([])      
const userAnswers = ref([])    
const feedbacks = ref([])
const isGraded = ref(false)
const finalScore = ref(0)

function getRandomInt(min, max) { return Math.floor(Math.random() * (max - min + 1)) + min }

function generateQuiz() {
  currentQuestions.value = []; userSteps.value = []; userAnswers.value = []; feedbacks.value = []; isGraded.value = false; finalScore.value = 0;
  while (currentQuestions.value.length < selectedCount.value) {
    const type = getRandomInt(1, 2); let a = getRandomInt(10, 25); if (Math.random() < 0.5) { a = -a }; const b = getRandomInt(5, 12); const c = getRandomInt(1, 4);
    let questionText = ''; let correctStep = ''; let answer = 0;
    if (type === 1) { questionText = `${a} - (${b} - ${c})`; correctStep = `${a}-${b}+${c}`; answer = a - b + c } 
    else { questionText = `${a} - (${b} + ${c})`; correctStep = `${a}-${b}-${c}`; answer = a - b - c }
    currentQuestions.value.push({ questionText, correctStep, answer })
  }
}

function gradeQuiz() {
  let correctCount = 0; const count = currentQuestions.value.length; feedbacks.value = [];
  for (let i = 0; i < count; i++) {
    const userStepClean = String(userSteps.value[i] || '').replace(/\s+/g, '').replace(/\+\-/g, '-').replace(/\-\+/g, '-')
    const userAnsClean = parseInt(userAnswers.value[i])
    const targetStep = currentQuestions.value[i].correctStep
    const targetAns = currentQuestions.value[i].answer
    if (userStepClean === targetStep && userAnsClean === targetAns) { correctCount++; feedbacks.value[i] = { text: '● 成功破译机关！', isCorrect: true } } 
    else if (userStepClean !== targetStep && userAnsClean === targetAns) { feedbacks.value[i] = { text: `✕ 偷懒警告：你没正常去括号！应填: ${targetStep}`, isCorrect: false } } 
    else { feedbacks.value[i] = { text: `✕ 触发机关！正确步骤: ${targetStep} = ${targetAns}`, isCorrect: false } }
  }
  finalScore.value = Math.round((correctCount / count) * 100); isGraded.value = true;
}

// ================= 💥 明天新增：AI 核心交互信令管道 💥 =================
const isChatOpen = ref(false)
const isAiLoading = ref(false)
const userMessage = ref('')
const chatMessages = ref([])
const chatBodyRef = ref(null)

function toggleChat() {
  isChatOpen.value = !isChatOpen.value
}

async function sendMessage() {
  if (!userMessage.value.trim() || isAiLoading.value) return
  
  const textToSend = userMessage.value
  chatMessages.value.push({ role: 'user', content: textToSend })
  userMessage.value = ''
  isAiLoading.value = true
  
  await nextTick()
  if (chatBodyRef.value) chatBodyRef.value.scrollTop = chatBodyRef.value.scrollHeight

  // 从本地环境变量中安全读取 API KEY
  const apiKey = import.meta.env.VITE_DEEPSEEK_API_KEY
  
  try {
    // 建立标准 HTTP POST 链路，直连 DeepSeek 官方网关
    const response = await fetch('https://api.deepseek.com/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`
      },
      body: JSON.stringify({
        model: 'deepseek-chat',
        messages: [
          {
            role: 'system',
            // 💡 极其硬核的提示词限制：强制 AI 变成温柔老师，决不能直接给答案，只能启发引导！
            content: `你现在是欧利蒂丝庄园的神秘数学管家。你的任务是辅导一位小学五年级升初中的小女孩（小侦探）搞懂"初中去括号与正负数加减法"的原理。
            你的说话风格要温柔、充满鼓励、带有一点点庄园解密的新奇感。
            🚨核心庄园法则：当她问你某道题怎么做时，你绝对不能直接告诉她这道题的完整步骤和最终答案！你必须一次只引导一步，通过提问或者打比方（比如：减号就像魔术师披风，脱掉小括号衣服时，里面的加减号会害怕得‘反转身体’）来启发她自己说出答案。`
          },
          ...chatMessages.value
        ],
        temperature: 0.7
      })
    })

    const data = await response.json()
    if (data.choices && data.choices[0]) {
      chatMessages.value.push({
        role: 'system', // 前端显示为 AI 气泡
        content: data.choices[0].message.content
      })
    } else {
      chatMessages.value.push({ role: 'system', content: '💥 管家思绪乱了，请稍后再试。' })
    }
  } catch (error) {
    console.error(error)
    chatMessages.value.push({ role: 'system', content: '⚠️ 庄园信号塔连线失败，请检查网络或密钥配置。' })
  } finally {
    isAiLoading.value = false
    await nextTick()
    if (chatBodyRef.value) chatBodyRef.value.scrollTop = chatBodyRef.value.scrollHeight
  }
}

onMounted(() => {
  generateQuiz()
})
</script>

<style scoped>
/* 保持原有羊皮纸样式不变... */
.v5-body { background-color: #1a1612; padding: 15px; border-radius: 12px; margin: 20px 0; position: relative; }
.container { max-width: 750px; margin: 10px auto; background-color: #f4ecd8; padding: 25px; border-radius: 8px; border: 6px double #4a0404; color: #333; }
.rule-banner { background: #e6ceb8; border: 1px solid #4a0404; padding: 10px; border-radius: 4px; margin-bottom: 20px; color: #4a0404; font-size: 14px; }
.menu-box { display: flex; justify-content: space-between; align-items: center; background: #e2d6b5; padding: 12px 20px; border-radius: 6px; margin-bottom: 25px; border: 1px solid #c4b593; }
.quiz-container { display: grid; grid-template-columns: 1fr; gap: 20px; }
@media(min-width: 600px) { .quiz-container { grid-template-columns: 1fr 1fr; } }
.quiz-item { background: rgba(74, 4, 4, 0.04); padding: 15px; border-radius: 6px; border: 1px solid #c4b593; display: flex; flex-direction: column; gap: 10px; }
.q-title { font-size: 15px; font-weight: bold; color: #4a0404; }
.origin-q { font-size: 20px; color: #111; font-family: monospace; font-weight: bold; }
.step-line { display: flex; align-items: center; justify-content: space-between; gap: 10px; }
.input-text { width: 150px; } .input-ans { width: 80px; text-align: center; }
.input-text, .input-ans { padding: 5px; font-size: 16px; border: 2px solid #4a0404; background: #fffaf0; color: #4a0404; border-radius: 4px; font-weight: bold; }
.feedback { font-size: 13px; font-weight: bold; }
.correct { color: #2d5a27; } .wrong { color: #b80d0d; }

/* 🦉 ================= 智能 AI 聊天组件专属精美样式 ================= */
.ai-assistant-wrapper { position: fixed; bottom: 30px; right: 30px; z-index: 9999; font-family: sans-serif; }
.ai-badge { width: 70px; height: 70px; background: #4a0404; border: 3px solid #f4ecd8; border-radius: 50%; box-shadow: 0 4px 15px rgba(0,0,0,0.4); display: flex; flex-direction: column; align-items: center; justify-content: center; cursor: pointer; transition: transform 0.2s; }
.ai-badge:hover { transform: scale(1.1) rotate(5deg); }
.badge-icon { font-size: 26px; }
.badge-text { font-size: 10px; color: #f4ecd8; font-weight: bold; margin-top: 2px; }

.ai-chat-window { width: 350px; height: 450px; background: #f4ecd8; border: 4px solid #4a0404; border-radius: 8px; box-shadow: 0 8px 30px rgba(0,0,0,0.6); display: flex; flex-direction: column; overflow: hidden; position: absolute; bottom: 85px; right: 0; }
.chat-header { background: #4a0404; color: #f4ecd8; padding: 10px; font-size: 14px; font-weight: bold; display: flex; justify-content: space-between; align-items: center; }
.close-btn { cursor: pointer; padding: 0 5px; }
.chat-body { flex: 1; padding: 15px; overflow-y: auto; background: rgba(74, 4, 4, 0.02); display: flex; flex-direction: column; gap: 12px; }

.chat-bubble { max-width: 85%; padding: 10px 12px; font-size: 14px; line-height: 1.4; border-radius: 8px; word-wrap: break-word; }
.chat-bubble.user { background: #4a0404; color: #f4ecd8; align-self: flex-end; border-bottom-right-radius: 1px; }
.chat-bubble.system { background: #e2d6b5; color: #333; align-self: flex-start; border-bottom-left-radius: 1px; border: 1px solid #c4b593; }
.chat-bubble.loading { opacity: 0.7; font-style: italic; }

.chat-footer { display: flex; padding: 10px; background: #e2d6b5; border-top: 2px solid #4a0404; gap: 8px; }
.chat-footer input { flex: 1; padding: 8px; border: 1px solid #4a0404; border-radius: 4px; background: #fffaf0; font-size: 14px; }
.chat-footer button { padding: 8px 15px; background: #4a0404; color: #f4ecd8; border: none; border-radius: 4px; font-weight: bold; cursor: pointer; }
.chat-footer button:hover { background: #720606; }
</style>