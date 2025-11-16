#!/bin/bash
set -e

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Installing Node dependencies..."
cd frontend
npm install
npm run build
cd ..

echo "Deployment complete!"
