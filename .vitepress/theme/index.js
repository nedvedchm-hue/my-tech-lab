import DefaultTheme from 'vitepress/theme'
import MathGame from './components/MathGame.vue' 
import MathGameV2 from './components/MathGameV2.vue' 

export default {
  ...DefaultTheme,
  enhanceApp({ app }) {
    app.component('MathGame', MathGame)
    app.component('MathGameV2', MathGameV2)

  }
}