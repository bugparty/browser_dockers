# Docker Chrome 浏览器容器

支持 WebGL、远程调试、VNC 访问的 Chrome 浏览器容器。

## 🚀 快速开始

### 构建镜像
```bash
docker build -t chrome:latest .
```

### 运行容器
```bash
docker run -d \
  -p 5900:5900 \
  -p 9222:9223 \
  --name chrome \
  chrome:latest
```

### 验证运行
```bash
# 检查容器状态
docker ps | findstr chrome

# 测试调试端口
curl http://localhost:9222/json/version

# 查看日志
docker logs chrome
```

## 📦 当前 Dockerfile 说明

### Dockerfile.chrome-webgl（最终版本）
**推荐使用的生产版本**

特性：
- ✅ Google Chrome 稳定版
- ✅ WebGL 支持（SwiftShader + ANGLE）
- ✅ Remote Debugging (CDP) 端口 9222
- ✅ VNC 访问端口 5900
- ✅ socat 端口转发
- ✅ 反爬虫检测优化
- ✅ 中文字体支持

### Dockerfile.chrome（标准版）
与 `Dockerfile.chrome-webgl` 相同，标准命名便于使用。

### Dockerfile（原始版本）
早期测试版本，已过时。

## 🔧 关键配置

### Chrome 启动参数
```dockerfile
CMD ["google-chrome", \
     "--user-data-dir=/home/appuser/chrome-data", \
     "--remote-debugging-port=9222", \
     "--no-sandbox", \
     "--disable-setuid-sandbox", \
     "--disable-dev-shm-usage", \
     "--use-angle=swiftshader", \
     "--use-gl=angle", \
     "--enable-webgl", \
     "--no-first-run", \
     "--no-default-browser-check", \
     "--disable-blink-features=AutomationControlled", \
     "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"]
```

### 端口映射
- **9222** - Chrome DevTools Protocol（通过 socat 转发到容器内 9223）
- **5900** - VNC 远程桌面访问

### 关键依赖
- `socat` - 端口转发
- `xvfb` - 虚拟 X11 显示
- `x11vnc` - VNC 服务器
- `fluxbox` - 轻量级窗口管理器
- `libegl1` - WebGL 渲染支持

## 📁 Dockerfile 版本历史

### 归档文件（在 `dockerfiles_archive/`）

1. **Dockerfile.barve** - 早期 Brave 浏览器版本（已废弃）
2. **Dockerfile.chrome** - 第一版 Chrome（无 WebGL）
3. **Dockerfile.chrome2** - 添加 socat 的版本
4. **Dockerfile.chrome-socat** - socat 测试版本
5. **Dockerfile.chrome-final** - WebGL 早期尝试

### 演进过程
```
Brave 浏览器 → Chrome 基础版 → 添加 socat → 启用 WebGL → 最终优化
```

## 🛠️ 维护命令

### 重新构建
```bash
docker stop chrome
docker rm chrome
docker build -t chrome:latest .
docker run -d -p 5900:5900 -p 9222:9223 --name chrome chrome:latest
```

### 清理旧镜像
```bash
docker images | findstr chrome
docker rmi <旧镜像ID>
```

### 进入容器调试
```bash
docker exec -it chrome bash
```

## 🎯 使用建议

1. **生产环境**：使用 `Dockerfile.chrome-webgl`
2. **开发测试**：可以基于此 Dockerfile 修改
3. **性能优化**：根据需要调整分辨率和资源限制

## 📝 注意事项

- 容器内 Chrome 使用软件渲染（SwiftShader），无需 GPU
- WebGL 性能比原生 GPU 慢，但足够大多数场景
- 首次启动需要等待 10 秒左右
- socat 转发会略微增加延迟
