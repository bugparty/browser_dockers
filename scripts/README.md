# Docker Chrome 自动化脚本

Python 自动化脚本集合，用于控制 Docker 容器中运行的 Chrome 浏览器。

## 📁 脚本说明

### 1. chrome_automation.py（推荐）
**功能完整的自动化测试工具**

- ✅ 连接 Docker Chrome
- ✅ 页面导航和截图
- ✅ WebGL 检测
- ✅ 浏览器指纹检测
- ✅ 反爬虫特征测试

**使用方法：**
```bash
python scripts/chrome_automation.py
```

**功能演示：**
```python
from chrome_automation import ChromeAutomation

automation = ChromeAutomation()
await automation.connect()
await automation.goto("https://www.example.com")
await automation.screenshot("test.png")
webgl_info = await automation.check_webgl()
fingerprint = await automation.check_fingerprint()
```

### 2. test_webgl.py
**WebGL 快速测试工具**

快速检测 Chrome 的 WebGL 支持情况。

**使用方法：**
```bash
python scripts/test_webgl.py
```

**输出示例：**
```
🎨 WebGL 测试结果:
  ✅ Vendor: Google Inc. (Google)
  ✅ Renderer: ANGLE (Google, Vulkan 1.3.0 (SwiftShader))
  ✅ Version: WebGL 1.0 (OpenGL ES 2.0 Chromium)
  ✅ Max Texture Size: 8192
```

## 🔧 环境要求

### Python 依赖
```bash
pip install playwright
```

### Docker 容器要求
1. Chrome 容器正在运行
2. 端口映射：`localhost:9222` → `container:9223`
3. VNC 端口（可选）：`localhost:5900` → `container:5900`

## 🚀 快速开始

### 1. 启动 Docker 容器
```bash
docker run -d -p 5900:5900 -p 9222:9223 --name chrome-test chrome-webgl:latest
```

### 2. 验证连接
```bash
curl http://localhost:9222/json/version
```

### 3. 运行自动化脚本
```bash
python scripts/chrome_automation.py
```

## 🎯 核心功能

### 浏览器特征
- ✅ `navigator.webdriver = false`（反检测）
- ✅ WebGL 软件渲染（无需 GPU）
- ✅ 自定义 User-Agent
- ✅ 隐藏自动化控制特征

### 技术栈
- **Playwright** - 浏览器自动化
- **Chrome DevTools Protocol (CDP)** - 远程调试
- **SwiftShader + ANGLE** - WebGL 软件渲染
- **socat** - 端口转发

## 📊 测试站点

推荐测试网站：
- https://bot.sannysoft.com - 反爬虫检测
- https://www.example.com - 基础测试
- https://get.webgl.org - WebGL 测试

## ⚠️ 常见问题

### 连接失败
```bash
# 检查容器状态
docker ps | findstr chrome

# 检查端口
docker port chrome-test

# 测试端点
curl http://localhost:9222/json/version
```

### WebGL 不可用
确保 Dockerfile 包含：
```dockerfile
CMD ["google-chrome", \
     "--use-angle=swiftshader", \
     "--use-gl=angle", \
     "--enable-webgl"]
```

### 端口冲突
```bash
# 停止现有容器
docker stop chrome-test
docker rm chrome-test

# 使用不同端口
docker run -d -p 5901:5900 -p 9223:9223 --name chrome-test chrome-webgl:latest
```

## 📝 旧脚本

以下脚本已弃用（保留在主目录作为参考）：
- `test_chrome.py` - Selenium 版本（ChromeDriver 版本问题）
- `test_chrome_playwright.py` - 早期 Playwright 版本
- `test_in_container.py` - 容器内执行版本

建议使用 `chrome_automation.py` 替代所有旧脚本。
