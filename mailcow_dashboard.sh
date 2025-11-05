#!/bin/bash

################################################################################
# 🐮 Mailcow REST API Dashboard
# Interaktives Monitoring Dashboard für Mailcow
# Features:
#   - Real-time Status Updates
#   - Mailbox Quota Monitoring
#   - Forwarding Rules Display
#   - Performance Metrics
#   - Email Alert Configuration
#   - Logs & History
################################################################################

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
BOLD='\033[1m'
NC='\033[0m'

# Configuration
DOMAIN="rest-rampe.tech"
SERVER="84.46.241.104"
MAILCOW_URL="https://mailcow.rest-rampe.tech:1443/api/v1"
LOG_DIR="/home/newuser/Reste-Rampe/logs/mailcow"
REPORT_FILE="$LOG_DIR/latest_report.json"

# ============================================================================
# Utility Functions
# ============================================================================

print_header() {
    clear
    echo -e "${CYAN}${BOLD}"
    echo "╔════════════════════════════════════════════════════════════════════╗"
    echo "║                 🐮 MAILCOW MONITORING DASHBOARD 🐮                ║"
    echo "║                      rest-rampe.tech Status                        ║"
    echo "╚════════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

print_menu() {
    echo -e "\n${BOLD}Main Menu:${NC}"
    echo "  1. 📊 View System Status"
    echo "  2. 📮 View All Mailboxes"
    echo "  3. 📈 View Quota Usage"
    echo "  4. 📤 View Forwarding Rules"
    echo "  5. 🏥 Health Check"
    echo "  6. 📡 Live Monitor (updates every 60s)"
    echo "  7. 💾 Export Report (JSON)"
    echo "  8. 📜 View Logs"
    echo "  9. 🔧 Configuration"
    echo "  0. ❌ Exit"
    echo ""
}

print_section() {
    echo -e "\n${BLUE}${BOLD}═══ $1 ═══${NC}\n"
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
    echo -e "${CYAN}ℹ️  $1${NC}"
}

# ============================================================================
# System Status Functions
# ============================================================================

get_api_key() {
    grep "MAILCOW_API_KEY=" /home/newuser/Reste-Rampe/.env | cut -d'=' -f2 | tr -d '"'
}

check_api_health() {
    print_section "API Health Check"
    
    API_KEY=$(get_api_key)
    
    if [ -z "$API_KEY" ] || [ "$API_KEY" = "your_api_key_here" ]; then
        print_error "Mailcow API Key not configured!"
        echo "Run option 9 to configure"
        return 1
    fi
    
    local start_time=$(date +%s%N)
    
    # Try to connect to API
    local response=$(curl -s -o /dev/null -w "%{http_code}" \
        -H "X-API-Key: $API_KEY" \
        -H "Content-Type: application/json" \
        "$MAILCOW_URL/status/version" 2>/dev/null || echo "000")
    
    local end_time=$(date +%s%N)
    local response_time=$(( ($end_time - $start_time) / 1000000 ))  # Convert to ms
    
    if [ "$response" = "200" ]; then
        print_success "API is responding"
        echo "Response Code: $response"
        echo "Response Time: ${response_time}ms"
        return 0
    else
        print_error "API Error (HTTP $response)"
        return 1
    fi
}

get_mailboxes() {
    print_section "All Mailboxes"
    
    API_KEY=$(get_api_key)
    
    if [ -z "$API_KEY" ] || [ "$API_KEY" = "your_api_key_here" ]; then
        print_error "Mailcow API Key not configured!"
        return 1
    fi
    
    echo "Fetching mailboxes..."
    
    local mailboxes=$(curl -s \
        -H "X-API-Key: $API_KEY" \
        -H "Content-Type: application/json" \
        "$MAILCOW_URL/mailbox/all" 2>/dev/null | jq '.' 2>/dev/null || echo "[]")
    
    if [ "$mailboxes" = "[]" ]; then
        print_warning "No mailboxes found or API error"
        return 1
    fi
    
    echo "$mailboxes" | jq -r '.[] | "\(.name) (@\(.domain)) - Status: \(.active)"' 2>/dev/null || echo "Error parsing mailboxes"
}

get_quota_usage() {
    print_section "Quota Usage"
    
    API_KEY=$(get_api_key)
    
    if [ -z "$API_KEY" ] || [ "$API_KEY" = "your_api_key_here" ]; then
        print_error "Mailcow API Key not configured!"
        return 1
    fi
    
    echo "Mailbox                              Used / Total       Percent"
    echo "────────────────────────────────────────────────────────────────"
    
    local mailboxes=$(curl -s \
        -H "X-API-Key: $API_KEY" \
        -H "Content-Type: application/json" \
        "$MAILCOW_URL/mailbox/all" 2>/dev/null | jq -r '.[].name' 2>/dev/null || echo "")
    
    if [ -z "$mailboxes" ]; then
        print_error "Could not fetch mailboxes"
        return 1
    fi
    
    for mailbox in $mailboxes; do
        local quota=$(curl -s \
            -H "X-API-Key: $API_KEY" \
            -H "Content-Type: application/json" \
            "$MAILCOW_URL/mailbox/quota/$mailbox" 2>/dev/null | jq '.' 2>/dev/null || echo "{}")
        
        if [ "$quota" != "{}" ]; then
            local max_quota=$(echo "$quota" | jq -r '.max_new_mailbox_quota // "0"' 2>/dev/null)
            local bytes_used=$(echo "$quota" | jq -r '.bytes // "0"' 2>/dev/null)
            
            # Convert to MB
            local mb_used=$((bytes_used / 1024 / 1024))
            local mb_total=$((max_quota / 1024 / 1024))
            
            if [ "$mb_total" -gt 0 ]; then
                local percent=$((100 * mb_used / mb_total))
                printf "%-35s %5dMB / %5dMB   %3d%%\n" "$mailbox" "$mb_used" "$mb_total" "$percent"
            fi
        fi
    done
}

get_forwarding_rules() {
    print_section "Forwarding Rules"
    
    API_KEY=$(get_api_key)
    
    if [ -z "$API_KEY" ] || [ "$API_KEY" = "your_api_key_here" ]; then
        print_error "Mailcow API Key not configured!"
        return 1
    fi
    
    local mailboxes=$(curl -s \
        -H "X-API-Key: $API_KEY" \
        -H "Content-Type: application/json" \
        "$MAILCOW_URL/mailbox/all" 2>/dev/null | jq -r '.[].name' 2>/dev/null || echo "")
    
    local total_forwardings=0
    
    for mailbox in $mailboxes; do
        local forwardings=$(curl -s \
            -H "X-API-Key: $API_KEY" \
            -H "Content-Type: application/json" \
            "$MAILCOW_URL/forwarding/get/$mailbox" 2>/dev/null | jq 'length' 2>/dev/null || echo "0")
        
        if [ "$forwardings" -gt 0 ]; then
            echo -e "${CYAN}$mailbox:${NC}"
            curl -s \
                -H "X-API-Key: $API_KEY" \
                -H "Content-Type: application/json" \
                "$MAILCOW_URL/forwarding/get/$mailbox" 2>/dev/null | \
                jq -r '.[] | "  → \(.destination)"' 2>/dev/null || true
            
            total_forwardings=$((total_forwardings + forwardings))
        fi
    done
    
    echo ""
    print_info "Total Forwarding Rules: $total_forwardings"
}

live_monitor() {
    print_section "Live Monitor (Ctrl+C to stop)"
    
    echo "Updates every 60 seconds..."
    echo ""
    
    while true; do
        echo "Last update: $(date '+%Y-%m-%d %H:%M:%S')"
        echo ""
        
        # API Health
        print_info "Checking API Health..."
        check_api_health || true
        
        # Mailbox Count
        API_KEY=$(get_api_key)
        if [ -n "$API_KEY" ] && [ "$API_KEY" != "your_api_key_here" ]; then
            local count=$(curl -s \
                -H "X-API-Key: $API_KEY" \
                -H "Content-Type: application/json" \
                "$MAILCOW_URL/mailbox/all" 2>/dev/null | jq 'length' 2>/dev/null || echo "?")
            
            print_info "Active Mailboxes: $count"
        fi
        
        echo ""
        echo "Next update in 60 seconds... (Ctrl+C to exit)"
        sleep 60
    done
}

export_report() {
    print_section "Export Report"
    
    mkdir -p "$LOG_DIR"
    
    API_KEY=$(get_api_key)
    
    if [ -z "$API_KEY" ] || [ "$API_KEY" = "your_api_key_here" ]; then
        print_error "Mailcow API Key not configured!"
        return 1
    fi
    
    echo "Generating report..."
    
    local timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    local report="{\"timestamp\":\"$timestamp\",\"mailboxes\":[]}"
    
    local mailboxes=$(curl -s \
        -H "X-API-Key: $API_KEY" \
        -H "Content-Type: application/json" \
        "$MAILCOW_URL/mailbox/all" 2>/dev/null | jq '.' 2>/dev/null || echo "[]")
    
    echo "$mailboxes" | jq "{timestamp:\"$timestamp\",mailboxes:.}" > "$REPORT_FILE"
    
    print_success "Report exported to: $REPORT_FILE"
    echo "Size: $(du -h $REPORT_FILE | cut -f1)"
}

view_logs() {
    print_section "Mailcow Logs"
    
    if [ -d "$LOG_DIR" ] && [ "$(ls -A $LOG_DIR)" ]; then
        echo "Recent log entries:"
        ls -1t "$LOG_DIR"/* | head -10 | while read file; do
            echo ""
            echo "File: $(basename $file)"
            head -5 "$file"
        done
    else
        print_warning "No logs found yet"
        echo "Logs will be created when you run reports"
    fi
}

view_configuration() {
    print_section "Mailcow Configuration"
    
    echo "Current Configuration:"
    echo ""
    
    grep -E "^MAILCOW_|^VITE_API_URL|^FROM_EMAIL" /home/newuser/Reste-Rampe/.env | while read line; do
        key=$(echo "$line" | cut -d'=' -f1)
        value=$(echo "$line" | cut -d'=' -f2 | cut -c1-30)
        
        if echo "$key" | grep -q "KEY\|PASSWORD"; then
            echo "  $key: ${value:0:5}...***"
        else
            echo "  $key: $value"
        fi
    done
    
    echo ""
    echo -e "${YELLOW}To update configuration:${NC}"
    echo "  ssh reste-rampe"
    echo "  cd /home/newuser/Reste-Rampe"
    echo "  nano .env"
    echo "  docker-compose restart backend"
}

# ============================================================================
# Main Loop
# ============================================================================

main_loop() {
    while true; do
        print_header
        print_menu
        
        read -p "Select option: " choice
        
        case $choice in
            1) check_api_health; read -p "Press Enter..." ;;
            2) get_mailboxes; read -p "Press Enter..." ;;
            3) get_quota_usage; read -p "Press Enter..." ;;
            4) get_forwarding_rules; read -p "Press Enter..." ;;
            5) check_api_health; read -p "Press Enter..." ;;
            6) live_monitor ;;
            7) export_report; read -p "Press Enter..." ;;
            8) view_logs; read -p "Press Enter..." ;;
            9) view_configuration; read -p "Press Enter..." ;;
            0)
                echo -e "${CYAN}Goodbye!${NC}"
                exit 0
                ;;
            *)
                print_error "Invalid option"
                read -p "Press Enter..."
                ;;
        esac
    done
}

# ============================================================================
# Entry Point
# ============================================================================

# Check if we have .env
if [ ! -f "/home/newuser/Reste-Rampe/.env" ]; then
    echo -e "${RED}Error: .env file not found at /home/newuser/Reste-Rampe/.env${NC}"
    exit 1
fi

# Run main loop or command
if [ $# -eq 0 ]; then
    main_loop
else
    case $1 in
        health) check_api_health ;;
        mailboxes) get_mailboxes ;;
        quota) get_quota_usage ;;
        forwarding) get_forwarding_rules ;;
        export) export_report ;;
        logs) view_logs ;;
        config) view_configuration ;;
        live) live_monitor ;;
        *)
            echo "Usage: $0 [health|mailboxes|quota|forwarding|export|logs|config|live]"
            exit 1
            ;;
    esac
fi
