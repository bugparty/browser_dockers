#!/bin/bash
set -euo pipefail

export HOME="${HOME:-/home/node}"
export HOMEBREW_PREFIX="${HOMEBREW_PREFIX:-/home/linuxbrew/.linuxbrew}"
export PATH="${HOMEBREW_PREFIX}/bin:${HOMEBREW_PREFIX}/sbin:${PATH}"
export NONINTERACTIVE=1
export CI=1
export COREPACK_ENABLE_DOWNLOAD_PROMPT=0

BREW_BIN="${HOMEBREW_PREFIX}/bin/brew"
NPM_BIN="${HOMEBREW_PREFIX}/bin/npm"

mkdir -p /home/linuxbrew "${HOME}" "${HOME}/.openclaw"

if [ ! -x "${BREW_BIN}" ]; then
  echo "Installing Homebrew into ${HOMEBREW_PREFIX}"
  curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh -o /tmp/brew-install.sh
  /bin/bash /tmp/brew-install.sh
  rm -f /tmp/brew-install.sh
fi

eval "$("${BREW_BIN}" shellenv)"
"${BREW_BIN}" analytics off >/dev/null 2>&1 || true

if ! command -v node >/dev/null 2>&1; then
  echo "Installing node via Homebrew"
  "${BREW_BIN}" install node
fi

if ! command -v corepack >/dev/null 2>&1; then
  echo "Installing corepack"
  "${NPM_BIN}" install -g corepack
fi
corepack enable >/dev/null 2>&1 || true

if ! command -v openclaw >/dev/null 2>&1; then
  echo "Installing openclaw"
  "${NPM_BIN}" install -g openclaw@latest
fi

exec "$@"
