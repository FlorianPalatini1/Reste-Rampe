#!/bin/bash

# ╔════════════════════════════════════════════════════════════════════════════╗
# ║                                                                            ║
# ║         🎉 MAILCOW MONITORING DASHBOARD - QUICK START 🎉                 ║
# ║                                                                            ║
# ║              Deploy & Setup in Minutes (Copy & Paste Ready!)              ║
# ║                                                                            ║
# ╚════════════════════════════════════════════════════════════════════════════╝

echo "
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║              📊 MAILCOW MONITORING DASHBOARD - SETUP GUIDE                ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝

✨ This guide will help you deploy the monitoring dashboard in 5 minutes!

"

# ════════════════════════════════════════════════════════════════════════════
# STEP 1: Navigate to monitoring directory
# ════════════════════════════════════════════════════════════════════════════

echo "📁 Step 1: Navigate to monitoring directory"
echo "═══════════════════════════════════════════════════════════════════════════"
echo ""
echo "Command:"
echo "  cd /home/newuser/Reste-Rampe/monitoring"
echo ""
read -p "Press enter to continue..."

cd /home/newuser/Reste-Rampe/monitoring || exit 1

echo "✅ In monitoring directory!"
echo ""

# ════════════════════════════════════════════════════════════════════════════
# STEP 2: Configure .env
# ════════════════════════════════════════════════════════════════════════════

echo "⚙️ Step 2: Configure environment variables"
echo "═══════════════════════════════════════════════════════════════════════════"
echo ""

if [ ! -f .env ]; then
    echo "📝 Creating .env from template..."
    cp .env.example .env
    echo "✅ .env created!"
else
    echo "ℹ️ .env already exists"
fi

echo ""
echo "📋 Required configuration:"
echo ""
echo "  1. Get your Mailcow API URL:"
echo "     Usually: https://mailcow.rest-rampe.tech/api/v1"
echo ""
echo "  2. Get your Mailcow API Key:"
echo "     - Login to Mailcow admin panel"
echo "     - Go to: System → API"
echo "     - Copy the API key"
echo ""
echo "  3. Edit .env file:"
echo "     nano .env"
echo ""
echo "  Replace:"
echo "    MAILCOW_API_URL=https://mailcow.rest-rampe.tech/api/v1"
echo "    MAILCOW_API_KEY=your_real_api_key_here"
echo "    MAILCOW_VERIFY_SSL=false (or true if you have valid SSL)"
echo ""

read -p "Have you configured .env? (y/n) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "Please edit .env first:"
    echo "  nano .env"
    echo ""
    exit 1
fi

# ════════════════════════════════════════════════════════════════════════════
# STEP 3: Build Docker images
# ════════════════════════════════════════════════════════════════════════════

echo ""
echo "🐳 Step 3: Build Docker images"
echo "═══════════════════════════════════════════════════════════════════════════"
echo ""
echo "This might take 2-3 minutes..."
echo ""

docker-compose build

if [ $? -eq 0 ]; then
    echo "✅ Docker images built successfully!"
else
    echo "❌ Error building Docker images"
    exit 1
fi

echo ""

# ════════════════════════════════════════════════════════════════════════════
# STEP 4: Start services
# ════════════════════════════════════════════════════════════════════════════

echo "🚀 Step 4: Start services"
echo "═══════════════════════════════════════════════════════════════════════════"
echo ""

docker-compose up -d

echo ""
echo "Waiting for services to start..."
sleep 3

docker-compose ps

echo ""

# ════════════════════════════════════════════════════════════════════════════
# STEP 5: Verify services
# ════════════════════════════════════════════════════════════════════════════

echo "✅ Step 5: Verify services"
echo "═══════════════════════════════════════════════════════════════════════════"
echo ""

# Check backend health
echo "Checking backend health..."
if docker-compose exec -T monitoring-backend curl -s http://localhost:8888/health > /dev/null 2>&1; then
    echo "✅ Backend API: HEALTHY"
else
    echo "⚠️ Backend API: Starting (may take a few seconds)"
fi

# Check frontend
echo "Checking frontend..."
if docker-compose exec -T monitoring-frontend curl -s http://localhost/health > /dev/null 2>&1; then
    echo "✅ Frontend: HEALTHY"
else
    echo "⚠️ Frontend: Starting (may take a few seconds)"
fi

echo ""

# ════════════════════════════════════════════════════════════════════════════
# STEP 6: Display access information
# ════════════════════════════════════════════════════════════════════════════

echo "🎉 Step 6: Access your dashboard"
echo "═══════════════════════════════════════════════════════════════════════════"
echo ""
echo "📊 Dashboard URL:"
echo "   → http://84.46.241.104/monitoring"
echo ""
echo "🔗 Direct API access (for testing):"
echo "   → http://84.46.241.104/api/monitoring/api/stats"
echo ""
echo "📱 Open in browser:"
echo "   1. Open your web browser"
echo "   2. Navigate to: http://84.46.241.104/monitoring"
echo "   3. You should see the monitoring dashboard!"
echo ""

# ════════════════════════════════════════════════════════════════════════════
# HELPFUL COMMANDS
# ════════════════════════════════════════════════════════════════════════════

echo "💡 Helpful commands:"
echo "═══════════════════════════════════════════════════════════════════════════"
echo ""
echo "View logs:"
echo "  docker-compose logs -f"
echo ""
echo "View backend logs:"
echo "  docker-compose logs -f monitoring-backend"
echo ""
echo "View frontend logs:"
echo "  docker-compose logs -f monitoring-frontend"
echo ""
echo "Stop services:"
echo "  docker-compose down"
echo ""
echo "Restart services:"
echo "  docker-compose restart"
echo ""
echo "Check status:"
echo "  docker-compose ps"
echo ""

# ════════════════════════════════════════════════════════════════════════════
# TROUBLESHOOTING
# ════════════════════════════════════════════════════════════════════════════

echo "🔧 Troubleshooting:"
echo "═══════════════════════════════════════════════════════════════════════════"
echo ""
echo "If you see 'No mailboxes available':"
echo ""
echo "  1. Check your Mailcow API key in .env"
echo "  2. Verify the API URL is correct"
echo "  3. Test with curl:"
echo "     docker exec monitoring-backend curl -X GET \\"
echo "       https://mailcow.rest-rampe.tech/api/v1/mailbox \\"
echo "       -H 'X-API-Key: your_key_here'"
echo ""
echo "If the page won't load:"
echo ""
echo "  1. Check if services are running:"
echo "     docker-compose ps"
echo "  2. Check logs:"
echo "     docker-compose logs"
echo "  3. Restart:"
echo "     docker-compose restart"
echo ""
echo "If you see SSL errors:"
echo ""
echo "  1. Set MAILCOW_VERIFY_SSL=false in .env (for self-signed certs)"
echo "  2. Or use true for valid SSL certificates"
echo "  3. Restart after changing:"
echo "     docker-compose up -d"
echo ""

# ════════════════════════════════════════════════════════════════════════════
# FINAL SUMMARY
# ════════════════════════════════════════════════════════════════════════════

echo ""
echo "╔════════════════════════════════════════════════════════════════════════════╗"
echo "║                                                                            ║"
echo "║                    ✅ SETUP COMPLETE! 🎉                                 ║"
echo "║                                                                            ║"
echo "║              📊 Dashboard is ready at:                                    ║"
echo "║              http://84.46.241.104/monitoring                             ║"
echo "║                                                                            ║"
echo "║              🔄 Auto-refreshes every 30 seconds                           ║"
echo "║              📧 Shows all mailbox status & usage                          ║"
echo "║              💾 Tracks quotas & storage trends                            ║"
echo "║                                                                            ║"
echo "╚════════════════════════════════════════════════════════════════════════════╝"
echo ""

# ════════════════════════════════════════════════════════════════════════════
# QUICK FEATURES OVERVIEW
# ════════════════════════════════════════════════════════════════════════════

echo "📋 Dashboard Features:"
echo "═══════════════════════════════════════════════════════════════════════════"
echo ""
echo "  ✅ Real-time API health monitoring"
echo "  ✅ Live mailbox quota tracking"
echo "  ✅ Usage trend charts"
echo "  ✅ Storage breakdown by mailbox"
echo "  ✅ Forwarding rules display"
echo "  ✅ Color-coded status (Green/Yellow/Red)"
echo "  ✅ Auto-refresh every 30 seconds"
echo "  ✅ Manual refresh button"
echo "  ✅ Beautiful responsive design"
echo "  ✅ Works on mobile & desktop"
echo ""

echo "🚀 Next steps:"
echo "═══════════════════════════════════════════════════════════════════════════"
echo ""
echo "  1. 📊 Open dashboard: http://84.46.241.104/monitoring"
echo "  2. 🔍 Verify all mailboxes are showing"
echo "  3. 📈 Check quota usage percentages"
echo "  4. 🔄 Test refresh button"
echo "  5. 💡 Bookmark the page!"
echo ""

echo "📞 Need help?"
echo "═══════════════════════════════════════════════════════════════════════════"
echo ""
echo "  1. Check logs:"
echo "     docker-compose logs -f"
echo ""
echo "  2. Read full documentation:"
echo "     cat MONITORING_DASHBOARD_SETUP.md"
echo ""
echo "  3. Test API directly:"
echo "     curl http://localhost/api/monitoring/api/stats | json_pp"
echo ""

echo "✨ Everything is ready to go! Happy monitoring! 🐮"
echo ""
