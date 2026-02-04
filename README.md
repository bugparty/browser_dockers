# 🐳 Browser Docker - Chrome & Brave Browser Containerization Solution

A complete browser containerization solution that supports running Chrome and Brave browsers in Docker with VNC visualization and automation control capabilities.

## 🌟 Features

- ✅ **Dual Browser Support** - Separate images for Chrome and Brave
- ✅ **Multi-Architecture Support** - Supports AMD64 and ARM64 platforms
- ✅ **VNC Visualization** - Remote viewing of browser interface via VNC
- ✅ **Remote Debugging** - Chrome DevTools Protocol (CDP) port exposed
- ✅ **WebGL Support** - WebGL software rendering using SwiftShader
- ✅ **Anti-Automation Detection** - Hide automation control features
- ✅ **Chinese Support** - Built-in Chinese fonts and emoji support
- ✅ **Automation Scripts** - Python automation examples provided

## 📦 Image Description

### Chrome Image (Dockerfile.chrome)

Built on Ubuntu 24.04 with features:

- **AMD64**: Official Google Chrome Stable installation
- **ARM64**: Uses Chromium Browser
- **WebGL Acceleration**: ANGLE + SwiftShader software rendering
- **Debug Port**: 9222 (connectable via CDP protocol)
- **VNC Port**: 5900 (X11 remote desktop)

**Startup Parameters:**
```dockerfile
--user-data-dir=/home/appuser/chrome-data
--remote-debugging-port=9222
--no-sandbox
--use-angle=swiftshader
--use-gl=angle
--enable-webgl
--disable-blink-features=AutomationControlled
```

### Brave Image (Dockerfile.barve)

Similar configuration to Chrome image, with differences:

- **GPU Disabled**: Uses `--disable-gpu` parameter
- **Debug Address**: Binds to `0.0.0.0` to allow external access
- **Entry Script**: Uses independent `entrypoint.sh`

## 🚀 Quick Start

### 1. Get Images

#### Option 1: Download Pre-built Images (Recommended)

Pull the latest version from GitHub Container Registry:

```bash
# Pull Chrome image
docker pull ghcr.io/bugparty/browserdocker-chrome:main

# Pull Brave image
docker pull ghcr.io/bugparty/browserdocker-brave:main
```

#### Option 2: Build Images Locally

##### Build Chrome Image
```bash
docker build -f Dockerfile.chrome -t chrome-docker:latest .
```

##### Build Brave Image
```bash
docker build -f Dockerfile.barve -t brave-docker:latest .
```

##### Multi-Architecture Build
```bash
# Chrome image
docker buildx build --platform linux/amd64,linux/arm64 -f Dockerfile.chrome -t chrome-docker:latest .

# Brave image
docker buildx build --platform linux/amd64,linux/arm64 -f Dockerfile.barve -t brave-docker:latest .
```

### 2. Run Containers

#### Using Docker Compose (Recommended)
```bash
docker-compose up -d
```

#### Manually Run Chrome
```bash
# Using pre-built image
docker run -d \
  --name chrome-browser \
  -p 5900:5900 \
  -p 9222:9222 \
  -v $(pwd)/appuser:/home/appuser \
  ghcr.io/bugparty/browserdocker-chrome:main

# Or using locally built image
docker run -d \
  --name chrome-browser \
  -p 5900:5900 \
  -p 9222:9222 \
  -v $(pwd)/appuser:/home/appuser \
  chrome-docker:latest
```

#### Manually Run Brave
```bash
# Using pre-built image
docker run -d \
  --name brave-browser \
  -p 5901:5900 \
  -p 9223:9222 \
  -v $(pwd)/appuser:/home/appuser \
  ghcr.io/bugparty/browserdocker-brave:main

# Or using locally built image
docker run -d \
  --name brave-browser \
  -p 5901:5900 \
  -p 9223:9222 \
  -v $(pwd)/appuser:/home/appuser \
  brave-docker:latest
```

### 3. Connection Methods

#### VNC Connection
Use a VNC client to connect to the container's graphical interface:

```bash
# Chrome container
vnc://localhost:5900

# Brave container
vnc://localhost:5901
```

Recommended VNC clients:
- Windows: TightVNC Viewer, RealVNC
- macOS: Screen Sharing, RealVNC
- Linux: Remmina, TigerVNC

#### CDP Remote Debugging

Chrome DevTools Protocol connection:

```bash
# Get debugging information
curl http://localhost:9222/json/version

# Open debugging panel
google-chrome --remote-debugging-port=9222
```

Visit in Chrome browser:
```
chrome://inspect/#devices
```
Click "Configure" and add `localhost:9222`

## 🔧 Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DISPLAY` | `:99` | X11 display number |

### Port Mapping

| Container Port | Host Port | Purpose |
|----------------|-----------|---------|
| 5900 | 5900 | VNC remote desktop |
| 9222 | 9222 | Chrome DevTools Protocol |

### Data Persistence

The project uses volume mounting of the `./appuser` directory to `/home/appuser` in the container, containing:

- `mlx/` - MLX application configuration and logs
- `chrome-data/` - Chrome user data directory
- `profiles/` - Browser profiles

## 🎯 Automation Scripts

The project provides complete Python automation scripts located in the `scripts/` directory.

### Install Dependencies

```bash
pip install playwright
playwright install
```

### Run Examples

#### 1. Complete Feature Test (chrome_automation.py)

```bash
python scripts/chrome_automation.py
```

Features include:
- Connect to Chrome in Docker container
- Page navigation and screenshots
- WebGL detection
- Browser fingerprint detection
- Anti-bot feature testing

#### 2. WebGL Quick Test (test_webgl.py)

```bash
python scripts/test_webgl.py
```

Example output:
```
🎨 WebGL Test Results:
  ✅ Vendor: Google Inc. (Google)
  ✅ Renderer: ANGLE (Google, Vulkan 1.3.0 (SwiftShader))
  ✅ Version: WebGL 1.0 (OpenGL ES 2.0 Chromium)
  ✅ Max Texture Size: 8192
```

#### 3. Selenium Example (selenium_example.py)

```bash
python scripts/selenium_example.py
```

See [scripts/README.md](scripts/README.md) for more detailed information.

## 📊 Technology Stack

### System Components

- **Ubuntu 24.04** - Base operating system
- **Xvfb** - Virtual X11 display server
- **X11VNC** - VNC server
- **Fluxbox** - Lightweight window manager

### Browser Technology

- **Google Chrome Stable** (AMD64) / **Chromium** (ARM64)
- **Chrome DevTools Protocol** - Remote debugging protocol
- **ANGLE + SwiftShader** - WebGL software rendering engine

### Font Support

- Noto CJK (Chinese, Japanese, Korean unified fonts)
- Noto Color Emoji (color emoji)
- WenQuanYi (Chinese fonts)
- Roboto, DejaVu, Liberation and other Western fonts

### Automation Tools

- **Playwright** - Modern browser automation framework
- **Selenium** - Classic automation testing tool

## 🛠️ Advanced Usage

### Custom Startup Parameters

Modify the CMD instruction in Dockerfile to customize browser startup parameters:

```dockerfile
CMD ["chrome", \
     "--user-data-dir=/home/appuser/chrome-data", \
     "--remote-debugging-port=9222", \
     "--window-size=1920,1080", \
     "--start-maximized", \
     # Add your custom parameters here
     ]
```

### Adding Browser Extensions

1. Place extension files in `./appuser/extensions/` directory
2. Add parameter in CMD:
```dockerfile
--load-extension=/home/appuser/extensions/your-extension
```

### Configure Proxy

Add to startup parameters:
```dockerfile
--proxy-server=http://proxy-server:port
```

Or via environment variables:
```yaml
environment:
  - HTTP_PROXY=http://proxy-server:port
  - HTTPS_PROXY=http://proxy-server:port
```

## 📁 Directory Structure

```
browserdocker/
├── Dockerfile.chrome          # Chrome image build file
├── Dockerfile.barve           # Brave image build file
├── docker-compose.yml         # Docker Compose configuration
├── entrypoint-chrome.sh       # Chrome startup script
├── entrypoint.sh              # Brave startup script
├── requirements.txt           # Python dependencies
├── appuser/                   # User data directory (persistent)
│   └── mlx/                   # MLX application data
│       ├── configs/           # Configuration files
│       ├── logs/              # Log files
│       └── profiles/          # Browser profiles
└── scripts/                   # Automation scripts
    ├── chrome_automation.py   # Complete automation script
    ├── test_webgl.py          # WebGL test
    ├── selenium_example.py    # Selenium example
    └── README.md              # Script usage instructions
```

## 🐛 Troubleshooting

### Container Won't Start

Check port conflicts:
```bash
netstat -ano | findstr "5900"
netstat -ano | findstr "9222"
```

View container logs:
```bash
docker logs chrome-browser
```

### VNC Connection Failed

1. Confirm container is running: `docker ps`
2. Check port mapping: `docker port chrome-browser`
3. Try restarting container: `docker restart chrome-browser`

### WebGL Not Working

Ensure startup parameters include:
```
--use-angle=swiftshader
--use-gl=angle
--enable-webgl
```

Test WebGL:
```bash
python scripts/test_webgl.py
```

### CDP Connection Failed

Check if debug port is open:
```bash
curl http://localhost:9222/json/version
```

Confirm firewall rules allow access to port 9222.

## 🔒 Security Recommendations

1. **Do not use** `--no-sandbox` parameter in production environments
2. Limit container network access (use Docker network isolation)
3. Regularly update base images and browser versions
4. Do not expose VNC and CDP ports to the public internet
5. Use VNC password protection (modify entrypoint script)

## 📝 License

This project is for learning and research purposes only.

## 🤝 Contributing

Issues and Pull Requests are welcome!

## 📞 Support

For questions, please submit issues on GitHub.

---

**Note**: Dockerfile.barve appears to be a typo for Dockerfile.brave, recommend renaming the file.
