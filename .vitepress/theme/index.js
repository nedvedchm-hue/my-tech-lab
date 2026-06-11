import DefaultTheme from 'vitepress/theme'
import MathGame from './components/MathGame.vue' 
import MathGameV2 from './components/MathGameV2.vue' 
import MathGameV3 from './components/MathGameV3.vue' 

export default {
  ...DefaultTheme,
  enhanceApp({ app }) {
    app.component('MathGame', MathGame)
    app.component('MathGameV2', MathGameV2)
    app.component('MathGameV3', MathGameV3) 
  }
}