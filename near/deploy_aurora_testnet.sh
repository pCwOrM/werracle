#!/bin/bash
# Werracle Aurora Testnet Deployment Script (Ethereum on NEAR)
# NEAR Hackathon 2026 - Track: Unstoppable DeFi

set -e

AURORA_TESTNET_RPC="https://testnet.aurora.dev"
CHAIN_ID="1313161555"

echo "=========================================================="
echo "⚡ Deploying Werracle to Aurora Testnet (Ethereum on NEAR)"
echo "   RPC: $AURORA_TESTNET_RPC"
echo "   Chain ID: $CHAIN_ID"
echo "=========================================================="

if [ -z "$AURORA_PRIVATE_KEY" ]; then
    echo "⚠️ Warning: AURORA_PRIVATE_KEY not set in environment."
    echo "Running dry-run build and bytecode size verification..."
    forge build --sizes
    exit 0
fi

echo "🚀 Broadcasting Werracle.sol deployment..."
forge create contracts/Werracle.sol:Werracle \
    --rpc-url "$AURORA_TESTNET_RPC" \
    --private-key "$AURORA_PRIVATE_KEY" \
    --legacy

echo "🚀 Broadcasting WerracleTripodZMod9.sol deployment..."
forge create contracts/WerracleTripodZMod9.sol:WerracleTripodZMod9 \
    --rpc-url "$AURORA_TESTNET_RPC" \
    --private-key "$AURORA_PRIVATE_KEY" \
    --legacy

echo "✅ Aurora Testnet Deployment Complete!"
