# 全球硬通货情报局 | 绝密资源库 v3.0

一个极客风的完全私密的「全球互联网硬通货」资源自动抓取与展示系统。采用前端 AES-256 解密架构，让你在保持 GitHub 仓库公开的情况下，也能实现数据的绝对私密。

![Version](https://img.shields.io/badge/version-3.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## ✨ v3.0 核心特性

- 🌍 **全球硬通货抓取**: 自动获取最新的虚拟信用卡（Visa/Mastercard/U卡）、AI大模型白嫖渠道、全球接码平台、优质邮箱资源等。
- 📂 **智能分类整理**: 新增前端分类筛选功能，按“金融黑卡”、“AI白嫖”、“接码神器”、“账号资源”等维度自动整理展示。
- 🔐 **高强度加密**: 沿用 AES-256-CBC 加密架构，确保只有持有密钥的用户才能查看敏感资源链接。
- 🎨 **增强版 UI**: 保持 Cyberpunk 风格的同时，优化了加载动画和卡片交互体验。
- ⚡ **全自动运维**: 通过 GitHub Actions 实现每日两次自动更新数据，无需人工干预。

## 🏗️ 架构图

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│ 全球资源数据源  │ --> │  Python 爬虫    │ --> │  AES-256 加密   │
│ (API/Web/Repo)  │     │  (scraper.py)   │     │  (data.enc)     │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                         │
                                                         v
                                              ┌─────────────────┐
                                              │   GitHub Pages  │
                                              │    (index.html) │
                                              └─────────────────┘
                                                         │
                                                         v
                                              ┌─────────────────┐
                                              │   浏览器端解密  │
                                              │ (分类筛选/展示) │
                                              └─────────────────┘
```

## 🚀 快速开始

### 1. 本地测试
```bash
# 克隆仓库
git clone https://github.com/your-username/my-ai-site.git
cd my-ai-site

# 安装依赖
pip install -r requirements.txt

# 运行爬虫 (使用默认密码 "资源风888" 测试)
python scraper.py
```

### 2. 生产部署 (GitHub Actions)
1. **Fork 本仓库** 到你的 GitHub 账号。
2. **设置密钥**: 
   - 进入仓库 **Settings** -> **Secrets and variables** -> **Actions**。
   - 点击 **New repository secret**。
   - Name: `SECRET_KEY`，Value: `你自己设定的解密密码`。
3. **开启 Pages**:
   - **Settings** -> **Pages** -> Source 选择 **Deploy from a branch**。
   - 分支选择 **main**，文件夹 **/(root)**。
4. **手动触发首次更新**:
   - 点击 **Actions** -> **自动抓取零撸情报** -> **Run workflow**。

## 📦 监控数据源 (v3.0)

| 分类 | 包含内容 | 抓取频率 |
|------|----------|----------|
| **金融黑卡** | Bybit/RedotPay/Dupay等U卡、虚拟Visa/Mastercard渠道 | 12h/次 |
| **AI白嫖** | Gemini学生认证、GitHub Copilot、免费API额度、限免Pro会员 | 12h/次 |
| **接码神器** | 全球实体卡接码平台、免费临时号码、API自动化接码 | 12h/次 |
| **账号资源** | 优质邮箱(Proton/Outlook)、批量注册工具、临时身份 | 12h/次 |
| **开源黑科技** | GitHub Trending 最新的自动化脚本与工具 | 12h/次 |

## 🔧 自定义扩展
你可以通过修改 `scraper.py` 中的 `get_*` 函数来添加你自己的私藏资源源。

## ⚠️ 注意事项
1. **密码安全**: 请务必在 GitHub Secrets 中设置 `SECRET_KEY`，不要在代码中硬编码真实密码。
2. **合法合规**: 本工具仅用于资源收集与技术研究，请在法律允许的范围内使用相关资源。

## 📄 许可证
MIT License

## 🙏 致谢
- [CryptoJS](https://github.com/brix/crypto-js) - 核心加密库
- [Unsplash](https://unsplash.com/) - 背景图资源
