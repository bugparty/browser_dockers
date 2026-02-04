#!/bin/bash

# Script to generate a secure token and create .env file from .env.sample

# Generate a secure random token
TOKEN=$(openssl rand -hex 32)

# Update .env.sample with the generated token
sed -i "s/OPENCLAW_GATEWAY_TOKEN=.*/OPENCLAW_GATEWAY_TOKEN=$TOKEN/" .env.sample

# Copy .env.sample to .env
cp .env.sample .env

# Create openclaw directories
mkdir -p openclaw
# Create Browser directory structure
mkdir -p appuser
# Set ownership and permissions

chown -R 1000:1000 openclaw appuser
chmod -R 700 openclaw

echo "✓ Token generated successfully!"
echo "✓ .env file created from .env.sample"
echo "✓ Created ./openclaw directory"
echo "✓ Set ownership to 1000:1000 and permissions to 700"
echo ""
echo "OPENCLAW_GATEWAY_TOKEN=$TOKEN"
