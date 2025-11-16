#!/bin/bash
set -e

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Installing Node dependencies and building frontend..."
cd frontend
npm install --production
npm run build
cd ..

echo "Build completed successfully!"
