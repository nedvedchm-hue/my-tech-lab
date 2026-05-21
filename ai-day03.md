# AI Day 03：从“本地”走向“全网”

https://nedvedchm-hue.github.io/my-tech-lab/

---

你的网站目前只能在自己的电脑（localhost）上看，这怎么行？

- **核心任务**：使用 **GitHub Pages** 或 **Vercel**，把你的网站一键发布到公网。
- **实战意义**：以后你只需要执行一个 `git push`，全世界（包括你手机上）都能看到你实时更新的学习笔记。
- **AI 辅助**：我会教你如何让 AI 帮你写自动化部署脚本（GitHub Actions），实现真正的“一键发布”。

------

## 🛰️ 第一阶段：建立远程“机房”（GitHub 仓库）

首先，我们需要一个存放代码的远程空间。

1. 登录你的 [GitHub](https://github.com/) 账号。
2. 点击右上角的 **+** -> **New repository**。
3. **Repository name**：建议起个有意义的名字，比如 `my-tech-lab`。
4. **Public/Private**：选择 **Public**（这样别人才能看到你的技术输出）。
5. 点击 **Create repository**，先不要关这个页面，一会儿我们要用它的 URL。

------

### 🛠️ 第一步：下载并安装 Git

1. **前往官网**：打开 [Git for Windows 官网](https://git-scm.com/download/win)。(国内安装地址：https://mirrors.huaweicloud.com/git-for-windows/v2.54.0.windows.1/)
2. **点击下载**：通常选择 `64-bit Git for Windows Setup`。
3. **安装选项（重点）**：
   - 安装过程基本一路点 `Next` 即可。
   - **唯一要注意的地方**：在 **"Adjusting your PATH environment"** 这一步，确保选择的是中间那个选项：**"Git from the command line and also from 3rd-party software"**（这是默认选中的，它会自动帮你把“路由”配好）。

------

### 🧪 第二步：激活环境

安装完后，**必须重启 VS Code**。

这就好比你给交换机加了一块板卡，得重启或者刷一下接口才能识别。

1. 关闭所有 VS Code 窗口。
2. 重新打开你的 `my-ai-lab` 文件夹。
3. 再次按下 `Ctrl + ~` 打开终端。

------

### ✅ 第三步：验证与初始化

在终端输入以下命令验证。如果看到版本号，就说明链路通了：

PowerShell

```
git --version
```

如果成功看到类似 `git version 2.x.x` 的输出，请立即执行你刚才失败的那个命令：

PowerShell

```
git init
```

------

### 💡 为什么会这样？（网络工程师视角）

在 Windows 里，当你输入一个命令（如 `git`），系统会去一张名为 `Path` 的表里查这个命令对应的“物理地址”（可执行文件路径）。

- **报错原因**：你的 `Path` 表里现在没有 Git 的记录。
- **解决方案**：安装程序会自动把 `C:\Program Files\Git\bin` 写入这条路由。



## 🔗 第二阶段：本地与远程的“链路打通”

回到你的 VS Code 终端，我们需要把本地的代码“推”上去。

PowerShell

```
# 1. 初始化 Git 仓库
git init

# 2. 将所有文件加入暂存区
git add .

# 3. 提交到本地仓库
git commit -m "feat: 网站基础架子与 Day01-03 笔记"

# 4. 关联远程仓库 (请把下面 URL 换成你刚才创建的那个)
git remote add origin https://github.com/你的用户名/my-tech-lab.git

# 5. 推送代码
git branch -M main
git push -u origin main
```

------

## 🤖 第三阶段：配置自动部署“脚本”（GitHub Actions）

这是最关键的一步。我们要告诉 GitHub：*“每当我推送代码，请帮我编译成网页并发布。”*

1. 在你的项目根目录下，新建一个文件夹路径：`.github/workflows/`（**注意前面有个点**）。
2. 在该文件夹下新建一个文件：`deploy.yml`。
3. 将以下代码完整复制进去：

YAML

```
name: Deploy VitePress site to Pages

on:
  push:
    branches: [main]

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'
      - name: Install dependencies
        run: npm install
      - name: Build with VitePress
        run: npm run build
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: .vitepress/dist

  deploy:
    environment:
      name: github-pages
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

------

## 🚀 第四阶段：见证奇迹的时刻

1. **再次提交：** 在 VS Code 终端输入：

   PowerShell

   ```
   git add .
   git commit -m "chore: add deployment workflow"
   git push
   ```

2. **开启 Pages 服务：**

   - 回到 GitHub 网页，点击仓库上方的 **Settings** -> **Pages**。
   - 在 **Build and deployment** 下的 **Source** 下拉菜单中，选择 **GitHub Actions**。

3. **观察进度：**

   - 点击仓库上方的 **Actions** 标签，你会看到一个正在转圈的任务。

------



其他：推送到giuhub失败解决方案

### 🛠️ 终极方案：配置 SSH 密钥（像配置管理口一样稳定）

按照以下步骤操作，我们要给你的电脑和 GitHub 建立一个“专线”：

#### 第一步：生成 SSH 密钥对

在 VS Code 终端输入：

PowerShell

```
ssh-keygen -t ed25519 -C "qzchenhm@gmail.com"
```

- **注意**：看到提示直接**按三次回车**，不要设置密码，直到看到一串字符画出现。

#### 第二步：获取公钥并“备案”到 GitHub

1. 在终端输入以下命令直接查看公钥内容：

   PowerShell

   ```
   cat ~/.ssh/id_ed25519.pub
   ```

2. **复制**以 `ssh-ed25519` 开头的那一长串字符。

3. 打开浏览器进入 GitHub：**Settings** -> **SSH and GPG keys** -> 点击 **New SSH key**。

4. **Title** 随便起（如 `Office-PC`），**Key** 粘贴刚才复制的内容，点击 **Add SSH key**。

#### 第三步：修改仓库“路由”为 SSH 协议

我们要告诉 Git 以后别走 `https` 了，改走 `git@github.com`。在终端运行：

PowerShell

```
git remote set-url origin git@github.com:nedvedchm-hue/my-tech-lab.git
```

#### 第四步：发起最后一次推送

PowerShell

```
git push -u origin main
```

- **提示**：第一次推送会问你 `Are you sure you want to continue connecting (yes/no/[fingerprint])?`，请输入 **`yes`** 并回车。



总结：

# 1. 把修改后的 MathGame.vue 放入暂存区
git add .

# 2. 提交更新，并写好你的“破译备注”
git commit -m "feat: 完美上线第五人格羊皮纸风格数学练习器"

# 3. 走 SSH 专线，一键推送到 GitHub 云端
git push



