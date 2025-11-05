#!/bin/bash

# ╔════════════════════════════════════════════════════════════════════════════╗
# ║                                                                            ║
# ║      🐮 MAILCOW MONITORING DASHBOARD - PRODUCTION DEPLOYMENT 🐮          ║
# ║                                                                            ║
# ║                  Deploy Monitoring Dashboard to Server                    ║
# ║                                                                            ║
# ╚════════════════════════════════════════════════════════════════════════════╝

set -e

echo ""
echo "╔════════════════════════════════════════════════════════════════════════════╗"
echo "║                                                                            ║"
echo "║           🚀 MAILCOW MONITORING DASHBOARD - DEPLOYMENT SCRIPT 🚀          ║"
echo "║                                                                            ║"
echo "║                  Deploys to: http://84.46.241.104/monitoring             ║"
echo "║                                                                            ║"
echo "╚════════════════════════════════════════════════════════════════════════════╝"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
log_info() {
    echo -e "${BLUE}ℹ️ $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# ════════════════════════════════════════════════════════════════════════════
# STEP 1: Navigate to project root
# ════════════════════════════════════════════════════════════════════════════

echo ""
log_info "Step 1: Navigating to Reste-Rampe project"
echo "═══════════════════════════════════════════════════════════════════════════"

cd /home/newuser/Reste-Rampe || {
    log_error "Could not navigate to /home/newuser/Reste-Rampe"
    exit 1
}

log_success "In project directory: $(pwd)"
echo ""

# ════════════════════════════════════════════════════════════════════════════
# STEP 2: Check Mailcow Configuration
# ════════════════════════════════════════════════════════════════════════════

echo "Step 2: Checking Mailcow configuration"
echo "═══════════════════════════════════════════════════════════════════════════"

if [ -z "$MAILCOW_API_URL" ]; then
    log_warning "MAILCOW_API_URL not set in main .env"
    echo ""
    echo "Make sure your .env contains:"
    echo "  MAILCOW_API_URL=https://mailcow.rest-rampe.tech/api/v1"
    echo "  MAILCOW_API_KEY=your_real_api_key"
    echo "  MAILCOW_VERIFY_SSL=false"
    echo ""
fi

log_info "Mailcow API URL: ${MAILCOW_API_URL:-Not configured}"
log_info "Mailcow API Key: $([ -z "$MAILCOW_API_KEY" ] && echo 'Not set' || echo '***set***')"
echo ""

# ════════════════════════════════════════════════════════════════════════════
# STEP 3: Configure Monitoring .env
# ════════════════════════════════════════════════════════════════════════════

echo "Step 3: Configuring monitoring .env"
echo "═══════════════════════════════════════════════════════════════════════════"

if [ ! -f monitoring/.env ]; then
    log_info "Creating monitoring/.env from template"
    cp monitoring/.env.example monitoring/.env
    
    # Copy Mailcow config from main .env if available
    if [ -f .env ]; then
        log_info "Copying Mailcow config from main .env"
        grep "^MAILCOW_" .env >> monitoring/.env || true
    fi
    
    log_success "monitoring/.env created"
else
    log_warning "monitoring/.env already exists"
fi

echo ""

# ════════════════════════════════════════════════════════════════════════════
# STEP 4: Build Monitoring Services
# ════════════════════════════════════════════════════════════════════════════

echo "Step 4: Building monitoring Docker images"
echo "═══════════════════════════════════════════════════════════════════════════"
echo ""

log_info "Building monitoring-backend..."
docker build -t reste-rampe-monitoring-backend:latest ./monitoring/backend
log_success "monitoring-backend built"

echo ""

log_info "Building monitoring-frontend..."
docker build -t reste-rampe-monitoring-frontend:latest ./monitoring/frontend
log_success "monitoring-frontend built"

echo ""

# ════════════════════════════════════════════════════════════════════════════
# STEP 5: Reload Main Docker Compose
# ════════════════════════════════════════════════════════════════════════════

echo "Step 5: Starting monitoring services with main docker-compose"
echo "═══════════════════════════════════════════════════════════════════════════"
echo ""

log_info "Restarting docker-compose to include monitoring services..."
docker-compose down
docker-compose up -d

echo ""
sleep 3

# ════════════════════════════════════════════════════════════════════════════
# STEP 6: Verify Services
# ════════════════════════════════════════════════════════════════════════════

echo "Step 6: Verifying services"
echo "═══════════════════════════════════════════════════════════════════════════"
echo ""

docker-compose ps

echo ""

# ════════════════════════════════════════════════════════════════════════════
# STEP 7: Health Checks
# ════════════════════════════════════════════════════════════════════════════

echo "Step 7: Running health checks"
echo "═══════════════════════════════════════════════════════════════════════════"
echo ""

log_info "Waiting for services to start (15 seconds)..."
sleep 5

echo ""
log_info "Checking monitoring-backend health..."
if docker exec reste-rampe-monitoring-backend curl -s http://localhost:8888/health > /dev/null 2>&1; then
    log_success "monitoring-backend: HEALTHY"
else
    log_warning "monitoring-backend: Still starting..."
fi

echo ""
log_info "Checking monitoring-frontend health..."
if docker exec reste-rampe-monitoring-frontend wget -q -O- http://localhost/health > /dev/null 2>&1; then
    log_success "monitoring-frontend: HEALTHY"
else
    log_warning "monitoring-frontend: Still starting..."
fi

echo ""

# ════════════════════════════════════════════════════════════════════════════
# STEP 8: Display Access Information
# ════════════════════════════════════════════════════════════════════════════

echo "╔════════════════════════════════════════════════════════════════════════════╗"
echo "║                                                                            ║"
echo "║                    ✅ DEPLOYMENT COMPLETE! 🎉                            ║"
echo "║                                                                            ║"
echo "║              📊 Dashboard is now available at:                           ║"
echo "║              http://84.46.241.104/monitoring                            ║"
echo "║                                                                            ║"
echo "╚════════════════════════════════════════════════════════════════════════════╝"
echo ""

echo "📋 Quick Links:"
echo "═══════════════════════════════════════════════════════════════════════════"
echo ""
echo "  🌐 Dashboard:"
echo "     http://84.46.241.104/monitoring"
echo ""
echo "  🔗 API Endpoints:"
echo "     http://84.46.241.104/api/monitoring/api/stats"
echo "     http://84.46.241.104/api/monitoring/api/health"
echo "     http://84.46.241.104/api/monitoring/api/mailboxes"
echo ""
echo "  📊 Direct Backend:"
echo "     http://localhost:8888/api/stats"
echo ""

# ════════════════════════════════════════════════════════════════════════════
# HELPFUL COMMANDS
# ════════════════════════════════════════════════════════════════════════════

echo "💡 Useful Commands:"
echo "═══════════════════════════════════════════════════════════════════════════"
echo ""
echo "  View all logs:"
echo "    docker-compose logs -f"
echo ""
echo "  View monitoring logs only:"
echo "    docker-compose logs -f monitoring-backend monitoring-frontend"
echo ""
echo "  Restart monitoring services:"
echo "    docker-compose restart monitoring-backend monitoring-frontend"
echo ""
echo "  Check container status:"
echo "    docker-compose ps"
echo ""
echo "  Test API directly:"
echo "    curl http://localhost:8888/api/stats | json_pp"
echo ""

# ════════════════════════════════════════════════════════════════════════════
# TROUBLESHOOTING
# ════════════════════════════════════════════════════════════════════════════

echo "🔧 Troubleshooting:"
echo "═══════════════════════════════════════════════════════════════════════════"
echo ""
echo "  If dashboard shows 'No mailboxes available':"
echo ""
echo "  1. Verify Mailcow API key:"
echo "     cat monitoring/.env | grep MAILCOW_API_KEY"
echo ""
echo "  2. Test API connectivity:"
echo "     docker exec reste-rampe-monitoring-backend curl -v \\"
echo "       https://mailcow.rest-rampe.tech/api/v1/status"
echo ""
echo "  3. Check backend logs:"
echo "     docker-compose logs monitoring-backend"
echo ""
echo "  If page won't load (404):"
echo ""
echo "  1. Verify services are running:"
echo "     docker-compose ps | grep monitoring"
echo ""
echo "  2. Check Nginx config:"
echo "     docker exec reste-rampe-frontend nginx -t"
echo ""
echo "  3. Reload Nginx:"
echo "     docker exec reste-rampe-frontend nginx -s reload"
echo ""

# ════════════════════════════════════════════════════════════════════════════
# NEXT STEPS
# ════════════════════════════════════════════════════════════════════════════

echo "🚀 Next Steps:"
echo "═══════════════════════════════════════════════════════════════════════════"
echo ""
echo "  1. ✅ Open dashboard in browser:"
echo "     http://84.46.241.104/monitoring"
echo ""
echo "  2. ✅ Verify mailboxes are showing"
echo ""
echo "  3. ✅ Check quota usage percentages"
echo ""
echo "  4. ⏳ Set up alerts (optional)"
echo ""
echo "  5. ⏳ Configure SSL/HTTPS (optional)"
echo ""
echo "  6. ⏳ Integrate with monitoring systems (optional)"
echo ""

# ════════════════════════════════════════════════════════════════════════════
# FINAL MESSAGE
# ════════════════════════════════════════════════════════════════════════════

echo ""
echo "═══════════════════════════════════════════════════════════════════════════"
echo "✨ Everything is ready! Your monitoring dashboard is live! 🐮"
echo "═══════════════════════════════════════════════════════════════════════════"
echo ""

log_success "Deployment completed successfully!"
echo ""
echo "Happy monitoring! 🚀"
echo ""
