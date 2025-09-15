FROM ubuntu:22.04

# Install required packages
RUN apt-get update && apt-get install -y \
    git \
    nginx \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create the app directory
RUN mkdir -p /var/www/app/log

# Create the upgrade_app script
# This script should: pull latest source from git and restart web server
RUN cat > /usr/local/bin/upgrade_app << 'EOF'
#!/bin/bash
echo "Starting app upgrade at $(date)"
cd /var/www/app
git pull origin $(git branch --show-current)
service nginx restart
echo "App upgraded successfully at $(date)" >> /var/www/app/log/production.log
EOF

# Make the script executable
RUN chmod +x /usr/local/bin/upgrade_app

# Set working directory
WORKDIR /var/www/app

# Keep container running
CMD ["tail", "-f", "/dev/null"]