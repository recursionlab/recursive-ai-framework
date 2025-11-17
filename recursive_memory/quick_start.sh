#!/bin/bash
# Recursive Memory Engine - Quick Start
# One-command setup and test

set -e

echo "═══════════════════════════════════════════════════════════════"
echo "RECURSIVE MEMORY ENGINE - QUICK START"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# Get user ID
if [ -z "$1" ]; then
    echo "Usage: ./quick_start.sh <your_name>"
    echo ""
    echo "Example: ./quick_start.sh kory"
    exit 1
fi

USER_ID=$1

echo "🚀 Setting up recursive memory for: $USER_ID"
echo ""

# 1. Initialize
echo "Step 1: Initializing memory graph..."
python3 cli/memory_cli.py init "$USER_ID"
echo ""

# 2. Analyze example
echo "Step 2: Analyzing example conversation..."
python3 cli/memory_cli.py analyze example_conversation.json --user "$USER_ID"
echo ""

# 3. Show stats
echo "Step 3: Your memory stats..."
python3 cli/memory_cli.py stats "$USER_ID"
echo ""

# 4. Generate integration prompt
echo "Step 4: Generating integration prompt..."
python3 cli/memory_cli.py resume "$USER_ID" --output integration_prompt.txt
echo ""

echo "═══════════════════════════════════════════════════════════════"
echo "✓ SETUP COMPLETE"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "Your recursive memory is active!"
echo ""
echo "Next steps:"
echo "1. cat integration_prompt.txt"
echo "2. Copy the prompt"
echo "3. Start a conversation with ANY LLM (Claude, GPT, etc.)"
echo "4. Paste the integration prompt to begin"
echo "5. You'll start from φ5 instead of φ0"
echo ""
echo "After your conversation:"
echo "- Export to conversation.json"
echo "- Run: python3 cli/memory_cli.py analyze conversation.json --user $USER_ID"
echo "- Your depth will accumulate: φ5 → φ15 → φ30 → ..."
echo ""
echo "═══════════════════════════════════════════════════════════════"
