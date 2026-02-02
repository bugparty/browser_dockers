# 🐳 Browser Docker - Chrome & Brave 浏览器容器化方案

一个完整的浏览器容器化解决方案，支持 Chrome 和 Brave 浏览器在 Docker 中运行，并提供 VNC 可视化和自动化控制能力。

## 🌟 特性

- ✅ **双浏览器支持** - Chrome 和 Brave 两个独立镜像
- ✅ **多架构支持** - 支持 AMD64 和 ARM64 平台
- ✅ **VNC 可视化** - 通过 VNC 远程查看浏览器界面
- ✅ **远程调试** - Chrome DevTools Protocol (CDP) 端口开放
- ✅ **WebGL 支持** - 使用 SwiftShader 软件渲染 WebGL
- ✅ **反自动化检测** - 隐藏自动化控制特征
- ✅ **中文支持** - 内置中文字体和表情符号
- ✅ **自动化脚本** - 提供 Python 自动化示例

## 📦 镜像说明

### Chrome 镜像 (Dockerfile.chrome)

基于 Ubuntu 24.04 构建，特性：

- **AMD64**: 安装官方 Google Chrome Stable
- **ARM64**: 使用 Chromium Browser
- **WebGL 加速**: 使用 ANGLE + SwiftShader 软件渲染
- **调试端口**: 9222 (可通过 CDP 协议连接)
- **VNC 端口**: 5900 (X11 远程桌面)

**启动参数：**
```dockerfile
--user-data-dir=/home/appuser/chrome-data
--remote-debugging-port=9222
--no-sandbox
--use-angle=swiftshader
--use-gl=angle
--enable-webgl
--disable-blink-features=AutomationControlled
```

### Brave 镜像 (Dockerfile.barve)

与 Chrome 镜像配置相似，区别：

- **GPU 禁用**: 使用 `--disable-gpu` 参数
- **调试地址**: 绑定 `0.0.0.0` 允许外部访问
- **入口脚本**: 使用独立的 `entrypoint.sh`

## 🚀 快速开始

### 1. 获取镜像

#### 方式一：直接下载预构建镜像（推荐）

从 GitHub Container Registry 拉取最新版本：

```bash
# 拉取 Chrome 镜像
docker pull ghcr.io/bugparty/browserdocker-chrome:main

# 拉取 Brave 镜像
docker pull ghcr.io/bugparty/browserdocker-brave:main
```

#### 方式二：本地构建镜像

##### 构建 Chrome 镜像
```bash
docker build -f Dockerfile.chrome -t chrome-docker:latest .
```

##### 构建 Brave 镜像
```bash
docker build -f Dockerfile.barve -t brave-docker:latest .
```

##### 多架构构建
```bash
# Chrome 镜像
docker buildx build --platform linux/amd64,linux/arm64 -f Dockerfile.chrome -t chrome-docker:latest .

# Brave 镜像
docker buildx build --platform linux/amd64,linux/arm64 -f Dockerfile.barve -t brave-docker:latest .
```

### 2. 运行容器

#### 使用 Docker Compose（推荐）
```bash
docker-compose up -d
```

#### 手动运行 Chrome
```bash
# 使用预构建镜像
docker run -d \
  --name chrome-browser \
  -p 5900:5900 \
  -p 9222:9222 \
  -v $(pwd)/appuser:/home/appuser \
  ghcr.io/bugparty/browserdocker-chrome:main

# 或使用本地构建镜像
docker run -d \
  --name chrome-browser \
  -p 5900:5900 \
  -p 9222:9222 \
  -v $(pwd)/appuser:/home/appuser \
  chrome-docker:latest
```

#### 手动运行 Brave
```bash
# 使用预构建镜像
docker run -d \
  --name brave-browser \
  -p 5901:5900 \
  -p 9223:9222 \
  -v $(pwd)/appuser:/home/appuser \
  ghcr.io/bugparty/browserdocker-brave:main

# 或使用本地构建镜像
docker run -d \
  --name brave-browser \
  -p 5901:5900 \
  -p 9223:9222 \
  -v $(pwd)/appuser:/home/appuser \
  brave-docker:latest
```

### 3. 连接方式

#### VNC 连接
使用 VNC 客户端连接到容器的图形界面：

```bash
# Chrome 容器
vnc://localhost:5900

# Brave 容器
vnc://localhost:5901
```

推荐的 VNC 客户端：
- Windows: TightVNC Viewer, RealVNC
- macOS: Screen Sharing, RealVNC
- Linux: Remmina, TigerVNC

#### CDP 远程调试

Chrome DevTools Protocol 连接：

```bash
# 获取调试信息
curl http://localhost:9222/json/version

# 打开调试面板
google-chrome --remote-debugging-port=9222
```

在 Chrome 浏览器中访问：
```
chrome://inspect/#devices
```
点击 "Configure" 添加 `localhost:9222`

## 🔧 配置说明

### 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `DISPLAY` | `:99` | X11 显示编号 |

### 端口映射

| 容器端口 | 主机端口 | 用途 |
|----------|----------|------|
| 5900 | 5900 | VNC 远程桌面 |
| 9222 | 9222 | Chrome DevTools Protocol |

### 数据持久化

项目使用 volume 挂载 `./appuser` 目录到容器内的 `/home/appuser`，包含：

- `mlx/` - MLX 应用配置和日志
- `chrome-data/` - Chrome 用户数据目录
- `profiles/` - 浏览器配置文件

## 🎯 自动化脚本

项目提供了完整的 Python 自动化脚本，位于 `scripts/` 目录。

### 安装依赖

```bash
pip install playwright
playwright install
```

### 运行示例

#### 1. 完整功能测试 (chrome_automation.py)

```bash
python scripts/chrome_automation.py
```

功能包括：
- 连接 Docker 容器中的 Chrome
- 页面导航和截图
- WebGL 检测
- 浏览器指纹检测
- 反爬虫特征测试

#### 2. WebGL 快速测试 (test_webgl.py)

```bash
python scripts/test_webgl.py
```

输出示例：
```
🎨 WebGL 测试结果:
  ✅ Vendor: Google Inc. (Google)
  ✅ Renderer: ANGLE (Google, Vulkan 1.3.0 (SwiftShader))
  ✅ Version: WebGL 1.0 (OpenGL ES 2.0 Chromium)
  ✅ Max Texture Size: 8192
```

#### 3. Selenium 示例 (selenium_example.py)

```bash
python scripts/selenium_example.py
```

查看 [scripts/README.md](scripts/README.md) 获取更多详细信息。

## 📊 技术栈

### 系统组件

- **Ubuntu 24.04** - 基础操作系统
- **Xvfb** - 虚拟 X11 显示服务器
- **X11VNC** - VNC 服务器
- **Fluxbox** - 轻量级窗口管理器

### 浏览器技术

- **Google Chrome Stable** (AMD64) / **Chromium** (ARM64)
- **Chrome DevTools Protocol** - 远程调试协议
- **ANGLE + SwiftShader** - WebGL 软件渲染引擎

### 字体支持

- Noto CJK (中日韩统一字体)
- Noto Color Emoji (彩色表情符号)
- WenQuanYi (文泉驿中文字体)
- Roboto, DejaVu, Liberation 等西文字体

### 自动化工具

- **Playwright** - 现代浏览器自动化框架
- **Selenium** - 经典自动化测试工具

## 🛠️ 高级用法

### 自定义启动参数

修改 Dockerfile 中的 CMD 指令来自定义浏览器启动参数：

```dockerfile
CMD ["chrome", \
     "--user-data-dir=/home/appuser/chrome-data", \
     "--remote-debugging-port=9222", \
     "--window-size=1920,1080", \
     "--start-maximized", \
     # 添加你的自定义参数
     ]
```

### 添加浏览器扩展

1. 将扩展文件放入 `./appuser/extensions/` 目录
2. 在 CMD 中添加参数：
```dockerfile
--load-extension=/home/appuser/extensions/your-extension
```

### 配置代理

在启动参数中添加：
```dockerfile
--proxy-server=http://proxy-server:port
```

或通过环境变量：
```yaml
environment:
  - HTTP_PROXY=http://proxy-server:port
  - HTTPS_PROXY=http://proxy-server:port
```

## 📁 目录结构

```
browserdocker/
├── Dockerfile.chrome          # Chrome 镜像构建文件
├── Dockerfile.barve           # Brave 镜像构建文件
├── docker-compose.yml         # Docker Compose 配置
├── entrypoint-chrome.sh       # Chrome 启动脚本
├── entrypoint.sh              # Brave 启动脚本
├── requirements.txt           # Python 依赖
├── appuser/                   # 用户数据目录（持久化）
│   └── mlx/                   # MLX 应用数据
│       ├── configs/           # 配置文件
│       ├── logs/              # 日志文件
│       └── profiles/          # 浏览器配置
└── scripts/                   # 自动化脚本
    ├── chrome_automation.py   # 完整自动化脚本
    ├── test_webgl.py          # WebGL 测试
    ├── selenium_example.py    # Selenium 示例
    └── README.md              # 脚本使用说明
```

## 🐛 故障排查

### 容器无法启动

检查端口占用：
```bash
netstat -ano | findstr "5900"
netstat -ano | findstr "9222"
```

查看容器日志：
```bash
docker logs chrome-browser
```

### VNC 无法连接

1. 确认容器正在运行：`docker ps`
2. 检查端口映射：`docker port chrome-browser`
3. 尝试重启容器：`docker restart chrome-browser`

### WebGL 不工作

确认启动参数包含：
```
--use-angle=swiftshader
--use-gl=angle
--enable-webgl
```

测试 WebGL：
```bash
python scripts/test_webgl.py
```

### CDP 连接失败

检查调试端口是否开放：
```bash
curl http://localhost:9222/json/version
```

确认防火墙规则允许访问 9222 端口。

## 🔒 安全建议

1. **不要在生产环境中使用** `--no-sandbox` 参数
2. 限制容器网络访问（使用 Docker 网络隔离）
3. 定期更新基础镜像和浏览器版本
4. 不要在公网暴露 VNC 和 CDP 端口
5. 使用 VNC 密码保护（修改 entrypoint 脚本）

## 📝 许可证

本项目仅供学习和研究使用。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📞 支持

如有问题，请在 GitHub Issues 中提出。

---

**注意**: Dockerfile.barve 应该是 Dockerfile.brave 的拼写错误，建议重命名文件。
