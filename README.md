#  OpenClaw and Chrome  OneKey  Containerization Solution

how to setup

```bash
./setup_env.sh 
docker compose pull
docker compose up -d
docker compose exec openclaw openclaw onboard
# you need to restart openclaw gateway to make configuration take effects.
docker compose restart openclaw
# then you can enter the bash environment
docker compose exec openclaw  bash
```