#!/bin/bash

echo "🚀 Starting deployment to aiapp.nasadef.com.my..."

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

# Run the deployment script
echo "📤 Deploying files via FTP..."
node deploy.js

if [ $? -eq 0 ]; then
    echo "✅ Deployment successful!"
    echo "🌐 App available at: https://aiapp.nasadef.com.my"
else
    echo "❌ Deployment failed!"
    exit 1
fi