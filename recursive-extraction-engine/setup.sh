#!/bin/bash

echo "=========================================="
echo "RECURSIVE EXTRACTION ENGINE - SETUP"
echo "=========================================="

# Check for API key
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "⚠️  ANTHROPIC_API_KEY not set!"
    echo "Please run: export ANTHROPIC_API_KEY='your-key-here'"
    echo ""
    read -p "Enter your Anthropic API key now: " api_key
    export ANTHROPIC_API_KEY="$api_key"
fi

echo "✓ API key configured"

# Install dependencies
echo "Installing dependencies..."
pip install anthropic -q

echo "✓ Dependencies installed"
echo ""
echo "=========================================="
echo "READY TO EXTRACT"
echo "=========================================="
echo ""
echo "Usage examples:"
echo ""
echo "# Extract operators from this repo:"
echo "  python cli/extract.py /home/user/recursive-ai-framework --extractors operator"
echo ""
echo "# Extract everything:"
echo "  python cli/extract.py /home/user/recursive-ai-framework --all"
echo ""
echo "# Process another repo:"
echo "  python cli/extract.py /path/to/other/repo --all"
echo ""
