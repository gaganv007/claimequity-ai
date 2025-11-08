#!/bin/bash
# Quick script to set xAI API key as environment variable

if [ -z "$1" ]; then
    echo "Usage: ./set_xai_key.sh 'xai-your-key-here'"
    echo ""
    echo "Or set it manually:"
    echo "  export XAI_API_KEY='xai-your-key-here'"
    exit 1
fi

export XAI_API_KEY="$1"
echo "✅ xAI API key set for this session"
echo "   To make it permanent, add to your ~/.zshrc or ~/.bashrc:"
echo "   export XAI_API_KEY='$1'"

