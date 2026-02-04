# 🚀 OpenClaw Docker One-Click Installation Solution

## Introduction
This is an **incredibly simple** OpenClaw Docker containerization solution. Deploy and start your entire environment with just a few commands.

## ⚡ Quick Start (3 Steps)

```bash
# 1. Initialize environment
./setup_env.sh 

# 2. Start containers
docker compose pull
docker compose up -d

# 3. Configure openclaw
docker compose exec openclaw openclaw onboard
docker compose restart openclaw
```

## 🔧 Browser Configuration

Add this configuration to your OpenClaw config file (`/home/node/.openclaw/openclaw.json`) to connect to the local browser service:
You can ask OpenClaw to add this too.

```json
{
  "browser": {
    "enabled": true,
    "defaultProfile": "local-browser",
    "remoteCdpTimeoutMs": 2000,
    "remoteCdpHandshakeTimeoutMs": 4000,
    "profiles": {
      "local-browser": {
        "cdpUrl": "http://browser:9223",
        "color": "#00AA00"
      }
    }
  }
}
```

## enter openclaw cli/tui

```bash
docker compose exec openclaw bash
```

## 🎯 Key Features

- ✅ **One-Click Deployment** - Complex Docker configuration is already prepared for you
- ✅ **Out-of-the-Box** - No manual configuration needed, everything is automated
- ✅ **Developer-Friendly** - Built-in bash environment for quick container access


## 📦 What's Included

- Complete OpenClaw environment
- Integrated Chrome browser
- Automated configuration scripts
- Docker Compose orchestration

**That's it!** Whether you're a beginner or expert, you can quickly set up your OpenClaw development environment.