#!/bin/bash

################################################################################
# SSL/TLS & Custom Domain Setup Automation Script
# Automatisiert das komplette SSL Setup mit Let's Encrypt & Certbot
# Usage: bash ssl_setup.sh
################################################################################

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
DOMAIN="rest-rampe.tech"
EMAIL="admin@rest-rampe.tech"
NGINX_SITE="/etc/nginx/sites-available/$DOMAIN"
CERTBOT_PATH="/etc/letsencrypt/live/$DOMAIN"

################################################################################
# Functions
################################################################################

print_header() {
    echo -e "\n${BLUE}════════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}\n"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

check_prerequisites() {
    print_header "🔍 Checking Prerequisites"
    
    # Check if running as root or with sudo
    if [[ $EUID -ne 0 ]]; then
        print_error "This script must be run as root or with sudo"
        exit 1
    fi
    print_success "Running with sudo privileges"
    
    # Check DNS
    print_info "Checking DNS resolution for $DOMAIN..."
    if ping -c 1 "$DOMAIN" &> /dev/null; then
        print_success "DNS resolves correctly"
    else
        print_warning "DNS resolution might not be working yet. Continuing..."
    fi
    
    # Check firewall
    print_info "Checking if ports 80 and 443 are open..."
    if nc -zv 84.46.241.104 80 2>/dev/null && nc -zv 84.46.241.104 443 2>/dev/null; then
        print_success "Ports 80 and 443 are open"
    else
        print_warning "Ports might not be fully accessible. Continuing..."
    fi
}

update_system() {
    print_header "📦 Updating System Packages"
    
    apt update -qq
    print_success "Package list updated"
}

install_certbot() {
    print_header "🔒 Installing Certbot & Dependencies"
    
    if command -v certbot &> /dev/null; then
        print_success "Certbot already installed"
    else
        apt install -y certbot python3-certbot-nginx > /dev/null 2>&1
        print_success "Certbot and python3-certbot-nginx installed"
    fi
    
    certbot --version
}

request_certificate() {
    print_header "📜 Requesting Let's Encrypt Certificate"
    
    # Check if certificate already exists
    if [ -d "$CERTBOT_PATH" ]; then
        print_warning "Certificate for $DOMAIN already exists at $CERTBOT_PATH"
        read -p "Do you want to renew it? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            certbot renew --force-renewal
            print_success "Certificate renewed"
        else
            print_info "Skipping certificate request"
            return 0
        fi
    else
        print_info "Requesting new certificate for $DOMAIN..."
        certbot certonly --standalone \
            -d "$DOMAIN" \
            -d "www.$DOMAIN" \
            --email "$EMAIL" \
            --agree-tos \
            --non-interactive
        
        if [ -d "$CERTBOT_PATH" ]; then
            print_success "Certificate created successfully"
        else
            print_error "Failed to create certificate"
            exit 1
        fi
    fi
    
    # Show certificate details
    print_info "Certificate Details:"
    openssl x509 -in "$CERTBOT_PATH/fullchain.pem" -noout -dates
}

configure_nginx() {
    print_header "🌐 Configuring Nginx"
    
    # Backup existing config if it exists
    if [ -f "$NGINX_SITE" ]; then
        print_info "Backing up existing Nginx config..."
        cp "$NGINX_SITE" "${NGINX_SITE}.backup.$(date +%s)"
        print_success "Backup created"
    fi
    
    # Create new Nginx config
    print_info "Creating Nginx configuration..."
    
    cat > "$NGINX_SITE" << 'EOF'
# HTTP → HTTPS Redirect
server {
    listen 80;
    listen [::]:80;
    server_name rest-rampe.tech www.rest-rampe.tech;

    # Allow Certbot challenge
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    # Redirect all HTTP to HTTPS
    location / {
        return 301 https://$server_name$request_uri;
    }
}

# HTTPS Server
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name rest-rampe.tech www.rest-rampe.tech;

    # SSL Certificates from Let's Encrypt
    ssl_certificate /etc/letsencrypt/live/rest-rampe.tech/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/rest-rampe.tech/privkey.pem;

    # SSL Configuration (Mozilla Recommended)
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;

    # Frontend (Nginx - Port 80 in docker)
    location / {
        proxy_pass http://localhost:80;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # API Proxy (FastAPI - Port 8000)
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Error Pages
    error_page 404 /index.html;
}
EOF
    
    print_success "Nginx configuration created"
}

enable_nginx_site() {
    print_header "🚀 Enabling Nginx Site"
    
    # Enable site
    if [ ! -L "/etc/nginx/sites-enabled/$DOMAIN" ]; then
        ln -s "$NGINX_SITE" "/etc/nginx/sites-enabled/$DOMAIN"
        print_success "Site enabled"
    else
        print_info "Site already enabled"
    fi
    
    # Disable default site
    if [ -L "/etc/nginx/sites-enabled/default" ]; then
        rm "/etc/nginx/sites-enabled/default"
        print_success "Default site disabled"
    fi
    
    # Test Nginx config
    print_info "Testing Nginx configuration..."
    if nginx -t > /dev/null 2>&1; then
        print_success "Nginx configuration is valid"
    else
        print_error "Nginx configuration test failed"
        nginx -t
        exit 1
    fi
    
    # Reload Nginx
    print_info "Reloading Nginx..."
    systemctl reload nginx
    print_success "Nginx reloaded"
}

setup_auto_renewal() {
    print_header "🔄 Setting Up Auto-Renewal"
    
    # Enable certbot timer
    if systemctl is-enabled certbot.timer > /dev/null 2>&1; then
        print_info "Certbot timer already enabled"
    else
        systemctl enable certbot.timer
        print_success "Certbot timer enabled"
    fi
    
    # Start timer
    systemctl start certbot.timer
    print_success "Certbot timer started"
    
    # Show status
    print_info "Timer Status:"
    systemctl status certbot.timer --no-pager
}

test_ssl() {
    print_header "🧪 Testing SSL Configuration"
    
    print_info "Testing HTTPS connection..."
    if curl -s -I https://"$DOMAIN" | head -1; then
        print_success "HTTPS connection successful"
    else
        print_warning "HTTPS connection test failed (might be DNS related)"
    fi
    
    print_info "Testing HTTP redirect..."
    if curl -s -I http://"$DOMAIN" | grep -q "301\|302\|307"; then
        print_success "HTTP to HTTPS redirect working"
    else
        print_warning "HTTP redirect test inconclusive"
    fi
    
    print_info "Checking certificate..."
    openssl x509 -in "$CERTBOT_PATH/fullchain.pem" -noout -subject -issuer -dates
}

print_summary() {
    print_header "📊 Setup Complete Summary"
    
    echo "Domain: $DOMAIN"
    echo "Certificate Location: $CERTBOT_PATH"
    echo "Nginx Config: $NGINX_SITE"
    echo ""
    echo "Next Steps:"
    echo "1. Update DNS Records if not already done:"
    echo "   - A Record: rest-rampe.tech → 84.46.241.104"
    echo "   - CNAME Record: www → rest-rampe.tech"
    echo ""
    echo "2. Verify SSL on SSLLabs:"
    echo "   https://www.ssllabs.com/ssltest/analyze.html?d=$DOMAIN"
    echo ""
    echo "3. Check certificate renewal:"
    echo "   sudo certbot certificates"
    echo ""
    echo "4. Manual renewal test:"
    echo "   sudo certbot renew --dry-run"
    echo ""
}

print_dns_info() {
    print_header "🌐 DNS Configuration Required"
    
    echo "Set these DNS records in your domain provider:"
    echo ""
    echo "1. A Record:"
    echo "   Name: @ (or leave empty)"
    echo "   Type: A"
    echo "   Value: 84.46.241.104"
    echo "   TTL: 3600"
    echo ""
    echo "2. CNAME Record (for www):"
    echo "   Name: www"
    echo "   Type: CNAME"
    echo "   Value: rest-rampe.tech"
    echo "   TTL: 3600"
    echo ""
    echo "Verify with:"
    echo "  dig rest-rampe.tech"
    echo "  dig www.rest-rampe.tech"
    echo ""
}

################################################################################
# Main Execution
################################################################################

main() {
    print_header "🔒 SSL/TLS Setup for Reste-Rampe Production"
    
    print_dns_info
    
    read -p "Have you configured DNS records? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_error "Please configure DNS records first"
        exit 1
    fi
    
    check_prerequisites
    update_system
    install_certbot
    request_certificate
    configure_nginx
    enable_nginx_site
    setup_auto_renewal
    test_ssl
    print_summary
    
    print_success "SSL/TLS setup completed successfully! 🎉"
}

# Run main function
main "$@"
