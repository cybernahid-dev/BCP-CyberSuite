#!/bin/bash
# BCP-CyberSuite Docker Installation Script

set -e

echo "🚀 BCP-CyberSuite Docker Installation"
echo "====================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed!"
    echo "📦 Please install Docker first:"
    echo "   Linux: https://docs.docker.com/engine/install/"
    echo "   macOS: https://docs.docker.com/desktop/mac/install/"
    echo "   Windows: https://docs.docker.com/desktop/windows/install/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "⚠️ Docker Compose not found, using Docker only..."
    USE_COMPOSE=false
else
    USE_COMPOSE=true
fi

# Create necessary directories
mkdir -p {reports,databases,config}

echo "📦 Building BCP-CyberSuite Docker image..."
docker build -t bcp-cybersuite:latest .

if [ "$USE_COMPOSE" = true ]; then
    echo "🚀 Starting with Docker Compose..."
    docker-compose up -d
    echo "✅ BCP-CyberSuite is running in background!"
    echo "📁 Reports directory: ./reports"
    echo "📁 Databases directory: ./databases"
    echo ""
    echo "🔧 Commands:"
    echo "   docker-compose logs -f    # View logs"
    echo "   docker-compose stop       # Stop container"
    echo "   docker-compose start      # Start container"
    echo "   docker-compose down       # Remove container"
else
    echo "🚀 Starting with Docker..."
    docker run -it --rm \
        --name bcp-cybersuite \
        -v "$(pwd)/reports:/app/reports" \
        -v "$(pwd)/databases:/app/databases" \
        -v "$(pwd)/config:/app/config" \
        bcp-cybersuite:latest
    
    echo "✅ BCP-CyberSuite session completed!"
fi

echo ""
echo "🌐 GitHub: https://github.com/cybernahid-dev/BCP-CyberSuite"
echo "🐛 Issues: https://github.com/cybernahid-dev/BCP-CyberSuite/issues"
