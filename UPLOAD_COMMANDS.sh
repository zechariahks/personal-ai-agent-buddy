#!/bin/bash

# Personal AI Agent Buddy - GitHub Upload Commands
# Run these commands one by one in your terminal

echo "🚀 Starting GitHub upload process..."

# Step 1: Navigate to project directory
cd "/Users/z/My Drive/1A/articles/mcp/agentic-ai/personal-ai-agent-buddy"

# Step 2: Initialize git repository
echo "📁 Initializing git repository..."
git init

# Step 3: Add all files
echo "📝 Adding files to git..."
git add .

# Step 4: Create initial commit
echo "💾 Creating initial commit..."
git commit -m "🤖 Initial commit: Personal AI Agent Buddy with multi-domain intelligence

Features:
- 🌤️ Real-time weather analysis with schedule impact
- 📧 Gmail integration for email sending  
- 📅 Google Calendar management with OAuth2
- 🐦 X (Twitter) integration with AI summaries
- 🧠 Multi-agent architecture with context awareness
- 🔒 Security features and error handling
- 🎯 Proactive intelligence and decision making"

# Step 5: Add remote origin (REPLACE 'yourusername' with your GitHub username)
echo "🔗 Adding GitHub remote..."
echo "⚠️  IMPORTANT: Replace 'yourusername' with your actual GitHub username!"
echo "git remote add origin https://github.com/yourusername/personal-ai-agent-buddy.git"

# Step 6: Push to GitHub
echo "📤 Ready to push to GitHub..."
echo "Run these commands after creating your GitHub repository:"
echo "git branch -M main"
echo "git push -u origin main"

echo "✅ Setup complete! Follow the GitHub upload guide for next steps."
