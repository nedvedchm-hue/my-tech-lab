import DefaultTheme from 'vitepress/theme'
import MathGame from './components/MathGame.vue' // 路径根据实际情况填写

export default {
  ...DefaultTheme,
  enhanceApp({ app }) {
    app.component('MathGame', MathGame)
  }
}