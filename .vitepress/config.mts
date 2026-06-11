import { defineConfig } from 'vitepress'
import { withMermaid } from 'vitepress-plugin-mermaid' // 1. 引入画图插件

// 2. 用 withMermaid 包裹原来的配置
export default withMermaid(defineConfig({
  base: '/my-tech-lab/',
  title: "AI & 网络实验室",
  description: "电信人从菜鸟到专家的 AI 进化记录",
  
  themeConfig: {
    siteTitle: 'AI & 网络实验室',
    search: {
      provider: 'local'
    },
    nav: [
      { text: '首页', link: '/' },
      { text: 'IP技术', link: '/ospf-day01' },
      { text: 'AI历程', link: '/ai-day01' }
    ],
    // 侧边栏配置（整合了前两天内容）
    sidebar: [
      {
        text: '🤖 AI 学习历程',
        items: [
          { text: 'Day 01: 环境搭建与避坑', link: '/ai-day01' },
          { text: 'Day 02: 学会用 Mermaid 画网络拓扑图', link: '/ai-day02' },
          { text: 'Day 03: 从“本地”走向“全网”', link: '/ai-day03' },
          { text: 'Day 04: 庄园解密练习”', link: '/ai-day04' },
          { text: 'Day 05: 庄园解密练习升级版”', link: '/ai-day05' },
          { text: 'Day 06: 庄园解密练习升级再升级版”', link: '/ai-day06' },
          { text: 'Day 07: 世界杯前线战术情报看板”', link: '/world-cup-analysis' }
        ]
      },
      {
        text: '🌐 IP 网络技术 30 天',
        collapsed: false,
        items: [
          { text: 'Day 01: OSPF 状态机原理', link: '/ospf-day01' },
          { text: 'Day 02: 状态机故障复现', link: '/ospf-day02' },
          { text: 'Day 03: LSDB 中的秘密', link: '/ospf-day03' } ,
          { text: 'Day 04: 特殊区域与路由汇总', link: '/ospf-day04' } 
        ]
      }
    ]
  }
}))