# AI Day 01：从零开始，搭建我的 AI 学习避坑站

作为一名 IP 网络工程师，我习惯了 CLI 和设备配置，但面对 AI 浪潮，我决定亲手搭建一个属于自己的知识库。第一天，我选择了 **VS Code + VitePress**，因为这更符合一个技术人的直觉：**可控、高效、纯净。**

---

## 🛠️ 1. 环境底座：Node.js 安装全记录

VitePress 就像是运行在操作系统上的“应用”，而 **Node.js** 就是它的运行环境。底座不稳，网站乱跑。

### 1.1 版本选择：LTS 才是真爱
前往 [Node.js 官网](https://nodejs.org/) 下载 **LTS (Long Term Support)** 长期支持版。就像华为的受控版本，主打稳定，**强烈建议选这个**，避开 Current 尝鲜版。

### 1.2 安装过程中的“隐藏选项”
在 Windows 安装向导中，会询问是否安装 **"Tools for Native Modules"**。
> **避坑建议**：直接跳过，**不要勾选**。否则它会后台静默下载数 GB 的编译工具，极易导致安装过程卡死或占用大量磁盘空间。

### 1.3 验证环境变量
安装完成后，在终端验证系统路径是否正确配置：
```powershell
node -v  # 期望输出如 v20.x.x
npm -v   # 期望输出如 v10.x.x
```
如果提示“不是内部或外部命令”，需手动将 `C:\Program Files\nodejs\` 添加到系统的 **Path** 环境变量中。 
### 1.4 国内镜像加速

   默认仓库在国外，安装速度极慢，建议切换到国内镜像源：
```powershell
# 设置镜像源（推荐华为云或淘宝镜像）
npm config set registry [https://repo.huaweicloud.com/repository/npm/](https://repo.huaweicloud.com/repository/npm/)
# 验证配置
npm config get registry
```
------

   ## 🚀 2. VitePress 初始化实战

   在 VS Code 的集成终端（`Ctrl + ~`）中开始构建你的站点。

   ### 2.1 运行安装向导

   执行命令 `npx vitepress init`。我的配置清单如下：

   - **Root directory**: `./`
   - **Title**: `AI & 网络实验室`
   - **Theme**: `Default Theme`
   - **TypeScript / Script**: 全部选 `Yes`

   ### 2.2 权限策略调整

   如果在运行 npm 时提示“在此系统上禁止运行脚本”，需以管理员身份打开 PowerShell 执行以下命令：

```powershell

   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

------

   ## ❌ 3. 常见报错排坑：Missing script

   这是初始化中最容易遇到的坑，通常表现为 `npm run dev` 无法启动。

   ### 3.1 故障现象

   终端报错：`npm error Missing script: "dev"`。这说明 `package.json` 文件中缺失了启动指令。

   ### 3.2 修复方案

   手动编辑项目根目录下的 `package.json` 文件，确保包含以下 `scripts` 段落：

   JSON

   ```
   "scripts": {
     "dev": "vitepress dev",
     "build": "vitepress build",
     "preview": "vitepress preview"
   }
   ```

------

   ## 💡 实验心得

   1. **AI 是最佳结对程序员**：遇到报错不要慌，把错误日志丢给 AI，比自己翻文档快得多。
   2. **VS Code 生产力**：左边写 Markdown，底部跑终端，右边实时预览，这才是现代化的工作流。
   3. **结构化思维**：配置 VitePress 其实和配置网络协议很像，底层逻辑都是定义结构、参数和重定向。