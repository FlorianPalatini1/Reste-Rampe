#!/bin/bash

################################################################################
# DNS Configuration & Verification Helper
# Hilft beim DNS Setup und Verifikation
# Usage: bash dns_helper.sh
################################################################################

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

DOMAIN="rest-rampe.tech"
SERVER_IP="84.46.241.104"

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

show_dns_requirements() {
    print_header "📋 DNS Records Required"
    
    cat << EOF
Add these records in your domain provider (e.g., Namecheap, GoDaddy, etc.):

┌─ Primary Domain Record ─────────────────────────────────────────┐
│                                                                  │
│  Name/Host: @ (or leave empty - represents root domain)         │
│  Type:      A                                                   │
│  Value:     $SERVER_IP                                      │
│  TTL:       3600 (1 hour) or as short as possible             │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘

┌─ WWW Subdomain Record ──────────────────────────────────────────┐
│                                                                  │
│  Name/Host: www                                                 │
│  Type:      CNAME (or A, depending on provider)                │
│  Value:     $DOMAIN (or CNAME) / $SERVER_IP (if A)   │
│  TTL:       3600                                               │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘

Optional Email Records (for Mailcow):

┌─ Mail Exchange (MX) ────────────────────────────────────────────┐
│                                                                  │
│  Name/Host: @ (root)                                            │
│  Type:      MX                                                  │
│  Priority:  10                                                  │
│  Value:     mail.$DOMAIN                                    │
│  TTL:       3600                                               │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘

EOF
}

verify_dns_propagation() {
    print_header "🔍 Verifying DNS Propagation"
    
    print_info "Checking if DNS has propagated (might take 24-48 hours)...\n"
    
    # Check A record
    print_info "1️⃣  Checking A record for $DOMAIN..."
    if command -v dig &> /dev/null; then
        A_RECORD=$(dig +short "$DOMAIN" A 2>/dev/null || echo "")
        if [ -z "$A_RECORD" ]; then
            print_error "No A record found for $DOMAIN"
            print_warning "This might take up to 48 hours to propagate"
        else
            if [ "$A_RECORD" = "$SERVER_IP" ]; then
                print_success "A record resolves to $SERVER_IP ✓"
            else
                print_error "A record resolves to $A_RECORD (expected $SERVER_IP)"
            fi
        fi
    else
        print_warning "dig not installed, trying nslookup..."
        nslookup "$DOMAIN" 8.8.8.8 || true
    fi
    
    # Check WWW CNAME
    print_info "\n2️⃣  Checking CNAME record for www.$DOMAIN..."
    if command -v dig &> /dev/null; then
        WWW_RECORD=$(dig +short "www.$DOMAIN" CNAME 2>/dev/null || echo "")
        if [ -z "$WWW_RECORD" ]; then
            print_warning "No CNAME record found for www.$DOMAIN"
            print_info "Some providers use A records instead of CNAME"
        else
            print_success "CNAME record: $WWW_RECORD ✓"
        fi
    fi
    
    # Check if domain resolves locally
    print_info "\n3️⃣  Checking local DNS resolution..."
    if ping -c 1 -W 2 "$DOMAIN" &> /dev/null; then
        print_success "Domain resolves locally ✓"
    else
        print_warning "Domain doesn't resolve locally (DNS might not have propagated yet)"
    fi
}

test_connectivity() {
    print_header "🌐 Testing Connectivity"
    
    print_info "1️⃣  Testing port 80 (HTTP)..."
    if nc -zv -w 3 "$SERVER_IP" 80 2>&1 | grep -q "succeeded"; then
        print_success "Port 80 is accessible ✓"
    else
        print_warning "Port 80 might not be accessible"
    fi
    
    print_info "\n2️⃣  Testing port 443 (HTTPS)..."
    if nc -zv -w 3 "$SERVER_IP" 443 2>&1 | grep -q "succeeded"; then
        print_success "Port 443 is accessible ✓"
    else
        print_warning "Port 443 might not be accessible"
    fi
    
    print_info "\n3️⃣  Testing connection to $DOMAIN..."
    if timeout 5 bash -c "echo > /dev/tcp/$SERVER_IP/80" 2>/dev/null; then
        print_success "Connection to port 80 successful ✓"
    else
        print_warning "Cannot connect to port 80 on server"
    fi
}

check_dns_providers() {
    print_header "🏢 Popular DNS Providers"
    
    cat << EOF
Common Domain Registrars and DNS Providers:

1. Namecheap (namecheap.com)
   - Log in → Manage Domain → Advanced DNS
   - Add DNS records there

2. GoDaddy (godaddy.com)
   - Log in → My Products → Manage DNS
   - Add DNS records there

3. Cloudflare (cloudflare.com)
   - Sign up → Add your domain
   - Change nameservers at your registrar
   - Manage DNS records at Cloudflare

4. DigitalOcean (digitalocean.com)
   - Use DigitalOcean's DNS
   - Set nameservers at your registrar

5. AWS Route53 (aws.amazon.com)
   - Professional DNS hosting
   - More complex setup

Steps for DNS Setup:

1️⃣  Log in to your domain registrar
2️⃣  Find "DNS Settings" or "Advanced DNS"
3️⃣  Add/Edit A record → Point to $SERVER_IP
4️⃣  Add/Edit CNAME record (www) → Point to $DOMAIN
5️⃣  Save changes
6️⃣  Wait for propagation (up to 48 hours)
7️⃣  Run this script again to verify

EOF
}

generate_dns_script() {
    print_header "🤖 DNS Configuration (for Programmers)"
    
    cat << 'EOF'
# Command-line DNS Configuration Examples

# Using CloudFlare API:
ZONE_ID="your_zone_id"
API_TOKEN="your_api_token"

# Add A Record
curl -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records" \
  -H "Authorization: Bearer $API_TOKEN" \
  -d '{
    "type":"A",
    "name":"rest-rampe.tech",
    "content":"84.46.241.104",
    "ttl":3600
  }'

# Add CNAME Record
curl -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records" \
  -H "Authorization: Bearer $API_TOKEN" \
  -d '{
    "type":"CNAME",
    "name":"www",
    "content":"rest-rampe.tech",
    "ttl":3600
  }'

# List DNS Records
curl -X GET "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records" \
  -H "Authorization: Bearer $API_TOKEN"

EOF
}

show_dns_checklist() {
    print_header "✅ DNS Setup Checklist"
    
    cat << EOF
Use this checklist to ensure DNS is correctly configured:

□ Domain purchased and active
□ A record created:
  - Name: @
  - Type: A
  - Value: $SERVER_IP
  - TTL: 3600

□ CNAME record created (optional):
  - Name: www
  - Type: CNAME
  - Value: $DOMAIN
  - TTL: 3600

□ DNS propagation verified with dig/nslookup
□ Port 80 is open and accessible
□ Port 443 is open and accessible
□ Can ping/connect to $DOMAIN

After all checks pass:
├─ Run SSL setup: bash ssl_setup.sh
├─ Verify SSL: https://www.ssllabs.com/ssltest/
└─ Test website: https://$DOMAIN

EOF
}

show_dns_status() {
    print_header "📊 DNS Status Report"
    
    echo "Domain: $DOMAIN"
    echo "Server IP: $SERVER_IP"
    echo ""
    
    if command -v whois &> /dev/null; then
        echo "Registrar Information:"
        whois "$DOMAIN" 2>/dev/null | grep -i "registrar\|name server" | head -5 || true
    fi
    
    echo ""
    echo "Current DNS Records:"
    if command -v dig &> /dev/null; then
        dig "$DOMAIN" +short
    fi
}

main_menu() {
    clear
    print_header "🌐 DNS Configuration Helper"
    
    echo "Options:"
    echo "1. Show DNS Requirements (what records to add)"
    echo "2. Verify DNS Propagation (check if DNS is live)"
    echo "3. Test Connectivity (check ports 80/443)"
    echo "4. Show DNS Provider Instructions"
    echo "5. Show DNS Setup Checklist"
    echo "6. Show DNS Status Report"
    echo "7. Generate DNS API Examples"
    echo "8. Run All Checks"
    echo "9. Exit"
    echo ""
    read -p "Choose an option (1-9): " choice
    
    case $choice in
        1) show_dns_requirements ;;
        2) verify_dns_propagation ;;
        3) test_connectivity ;;
        4) check_dns_providers ;;
        5) show_dns_checklist ;;
        6) show_dns_status ;;
        7) generate_dns_script ;;
        8)
            show_dns_requirements
            verify_dns_propagation
            test_connectivity
            show_dns_checklist
            ;;
        9) print_info "Exiting..."; exit 0 ;;
        *) print_error "Invalid option"; sleep 1; main_menu ;;
    esac
    
    echo ""
    read -p "Press Enter to continue..."
    main_menu
}

# Run menu
main_menu
