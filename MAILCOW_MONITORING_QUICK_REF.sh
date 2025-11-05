#!/bin/bash

# 🐮 MAILCOW MONITORING QUICK REFERENCE 🐮
# Copy & Paste Commands for Easy Access

cat << 'EOF'

╔════════════════════════════════════════════════════════════════════════════╗
║            🐮 MAILCOW MONITORING - QUICK REFERENCE 🐮                   ║
╚════════════════════════════════════════════════════════════════════════════╝

📖 TABLE OF CONTENTS:
  1. GETTING STARTED
  2. PYTHON MONITORING TOOL
  3. BASH DASHBOARD
  4. DIRECT API COMMANDS
  5. AUTOMATION (CRON)
  6. TROUBLESHOOTING
  7. INTEGRATION EXAMPLES

════════════════════════════════════════════════════════════════════════════

1️⃣  GETTING STARTED
════════════════════════════════════════════════════════════════════════════

# SSH to server (no password needed!)
ssh reste-rampe

# Navigate to project
cd /home/newuser/Reste-Rampe

# List available monitoring tools
ls -lh mailcow_* MAILCOW_MONITORING.md

# Check if tools are executable
file mailcow_monitor.py mailcow_dashboard.sh


════════════════════════════════════════════════════════════════════════════

2️⃣  PYTHON MONITORING TOOL
════════════════════════════════════════════════════════════════════════════

# Single monitoring report
python3 mailcow_monitor.py

# Continuous monitoring (every 60 seconds)
python3 mailcow_monitor.py --watch 60

# Export to JSON file
python3 mailcow_monitor.py --export report.json

# Custom config file
python3 mailcow_monitor.py --config /path/to/.env

# Debug mode
python3 mailcow_monitor.py --debug

# Combine options
python3 mailcow_monitor.py --watch 30 --export /tmp/report.json --debug

# Kill watch mode
# Press: Ctrl+C


════════════════════════════════════════════════════════════════════════════

3️⃣  BASH DASHBOARD
════════════════════════════════════════════════════════════════════════════

# Open interactive dashboard menu
bash mailcow_dashboard.sh

# Direct commands (non-interactive)
bash mailcow_dashboard.sh health          # API health check
bash mailcow_dashboard.sh mailboxes       # List all mailboxes
bash mailcow_dashboard.sh quota           # Show quota usage
bash mailcow_dashboard.sh forwarding      # Show forwarding rules
bash mailcow_dashboard.sh export          # Export report
bash mailcow_dashboard.sh logs            # View logs
bash mailcow_dashboard.sh config          # Show configuration
bash mailcow_dashboard.sh live            # Live monitor (Ctrl+C to stop)


════════════════════════════════════════════════════════════════════════════

4️⃣  DIRECT API COMMANDS (curl)
════════════════════════════════════════════════════════════════════════════

# Get API Key from .env
API_KEY=$(grep MAILCOW_API_KEY /home/newuser/Reste-Rampe/.env | cut -d= -f2)

# Test API connection
curl -H "X-API-Key: $API_KEY" \
  https://mailcow.rest-rampe.tech:1443/api/v1/status/version

# Get all mailboxes
curl -H "X-API-Key: $API_KEY" \
  https://mailcow.rest-rampe.tech:1443/api/v1/mailbox/all | jq '.'

# Get mailbox quota
curl -H "X-API-Key: $API_KEY" \
  https://mailcow.rest-rampe.tech:1443/api/v1/mailbox/quota/user@rest-rampe.tech

# Get forwarding rules for mailbox
curl -H "X-API-Key: $API_KEY" \
  https://mailcow.rest-rampe.tech:1443/api/v1/forwarding/get/user@rest-rampe.tech

# Pretty print (requires jq)
curl -s -H "X-API-Key: $API_KEY" \
  https://mailcow.rest-rampe.tech:1443/api/v1/mailbox/all | jq '.'


════════════════════════════════════════════════════════════════════════════

5️⃣  AUTOMATION WITH CRON
════════════════════════════════════════════════════════════════════════════

# Edit crontab
crontab -e

# Add these lines:

# Monitor every 5 minutes, export to file
*/5 * * * * cd /home/newuser/Reste-Rampe && \
  python3 mailcow_monitor.py --export /tmp/mailcow_report_$(date +\%s).json

# Daily health report at 8 AM
0 8 * * * cd /home/newuser/Reste-Rampe && \
  python3 mailcow_monitor.py --export reports/report_$(date +\%Y-\%m-\%d).json

# Hourly check with alert
0 * * * * cd /home/newuser/Reste-Rampe && \
  python3 mailcow_monitor.py --export /tmp/report.json && \
  grep -q "\"status\": \"CRITICAL\"" /tmp/report.json && \
  echo "CRITICAL: Mailcow has issues!" | mail -s "Mailcow Alert" admin@rest-rampe.tech

# Every 15 minutes check quota
*/15 * * * * cd /home/newuser/Reste-Rampe && \
  bash mailcow_dashboard.sh quota >> /var/log/mailcow_quota.log

# View cron logs
grep CRON /var/log/syslog | tail -20

# List current cron jobs
crontab -l


════════════════════════════════════════════════════════════════════════════

6️⃣  TROUBLESHOOTING
════════════════════════════════════════════════════════════════════════════

# Problem: "API Key not configured"
# Solution:
cat .env | grep MAILCOW_API_KEY
# If shows "your_api_key_here" then:
nano .env
# Edit and set real API key
docker-compose restart backend

# Problem: "Connection refused"
# Solution:
curl https://mailcow.rest-rampe.tech:1443/api/v1/status/version
# Check Mailcow is running and accessible

# Problem: SSL certificate error
# Solution:
cat .env | grep MAILCOW_VERIFY_SSL
# Set to "false" for self-signed certs:
nano .env
# Change: MAILCOW_VERIFY_SSL=false

# Problem: "No mailboxes found"
# Solution:
python3 mailcow_monitor.py --debug
# Check error messages
# Verify API key has proper permissions

# Get detailed debug info
python3 mailcow_monitor.py --debug 2>&1 | head -50

# Check backend logs
docker-compose logs backend | tail -50

# Check if containers running
docker-compose ps

# Restart all services
docker-compose restart

# View environment
grep MAILCOW .env


════════════════════════════════════════════════════════════════════════════

7️⃣  INTEGRATION EXAMPLES
════════════════════════════════════════════════════════════════════════════

# EXAMPLE 1: Send Alert Email on Critical Status
cat > /home/newuser/Reste-Rampe/alert_critical.sh << 'SCRIPT'
#!/bin/bash
cd /home/newuser/Reste-Rampe
python3 mailcow_monitor.py --export /tmp/report.json

if grep -q '"status": "CRITICAL"' /tmp/report.json; then
  BODY=$(cat /tmp/report.json | jq -r '.overall_status')
  echo "Mailcow Status: $BODY" | \
  mail -s "🚨 CRITICAL: Mailcow Alert" admin@rest-rampe.tech
fi
SCRIPT

chmod +x /home/newuser/Reste-Rampe/alert_critical.sh
# Run: bash alert_critical.sh

# EXAMPLE 2: Slack Notification on Warning
cat > /home/newuser/Reste-Rampe/slack_alert.sh << 'SCRIPT'
#!/bin/bash
WEBHOOK="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
STATUS=$(cd /home/newuser/Reste-Rampe && \
  python3 mailcow_monitor.py --export /tmp/report.json && \
  cat /tmp/report.json | jq -r '.overall_status')

if [ "$STATUS" != "HEALTHY" ]; then
  curl -X POST $WEBHOOK \
    -H 'Content-type: application/json' \
    -d "{\"text\":\"⚠️ Mailcow Status: $STATUS\"}"
fi
SCRIPT

chmod +x /home/newuser/Reste-Rampe/slack_alert.sh
# Run: bash slack_alert.sh

# EXAMPLE 3: Create Daily Report
cat > /home/newuser/Reste-Rampe/daily_report.sh << 'SCRIPT'
#!/bin/bash
DIR="/home/newuser/Reste-Rampe/reports"
mkdir -p $DIR
DATE=$(date +%Y-%m-%d)
python3 /home/newuser/Reste-Rampe/mailcow_monitor.py \
  --export $DIR/mailcow_$DATE.json
echo "Report saved to: $DIR/mailcow_$DATE.json"
SCRIPT

chmod +x /home/newuser/Reste-Rampe/daily_report.sh
# Add to cron: 0 8 * * * /home/newuser/Reste-Rampe/daily_report.sh

# EXAMPLE 4: Archive Old Reports
find /home/newuser/Reste-Rampe/reports -name "*.json" -mtime +30 -delete
# Add to cron: 0 3 1 * * find /home/newuser/Reste-Rampe/reports -name "*.json" -mtime +30 -delete

# EXAMPLE 5: Parse JSON Report
python3 << 'PYTHON'
import json
with open('/tmp/mailcow_report.json') as f:
  data = json.load(f)
  print(f"API Status: {data['api_health']['status']}")
  print(f"Mailboxes: {len(data['mailboxes'])}")
  for mb in data['mailboxes']:
    print(f"  {mb['name']}: {mb['quota_percent']:.1f}%")
PYTHON


════════════════════════════════════════════════════════════════════════════

📊 USEFUL ONE-LINERS
════════════════════════════════════════════════════════════════════════════

# Count total users
ssh reste-rampe 'cd /home/newuser/Reste-Rampe && \
  python3 mailcow_monitor.py --export /tmp/r.json && \
  cat /tmp/r.json | jq ".mailboxes | length"'

# Get highest quota usage
ssh reste-rampe 'cd /home/newuser/Reste-Rampe && \
  bash mailcow_dashboard.sh quota | \
  sort -t/ -k1 -nr | head -5'

# Export and compress
ssh reste-rampe 'cd /home/newuser/Reste-Rampe && \
  python3 mailcow_monitor.py --export /tmp/report.json && \
  gzip -c /tmp/report.json > /tmp/report_$(date +%s).json.gz'

# Check API response time trend
ssh reste-rampe 'cd /home/newuser/Reste-Rampe && \
  for i in {1..5}; do \
    python3 mailcow_monitor.py --export /tmp/r.json && \
    cat /tmp/r.json | jq ".api_health.response_time_ms"; \
    sleep 5; \
  done'

# List all critical issues
ssh reste-rampe 'grep -r "CRITICAL" /tmp/mailcow_*.json | wc -l'


════════════════════════════════════════════════════════════════════════════

🎯 TYPICAL WORKFLOW
════════════════════════════════════════════════════════════════════════════

1. SSH to server
   ssh reste-rampe

2. Navigate to project
   cd /home/newuser/Reste-Rampe

3. Check status
   python3 mailcow_monitor.py

4. If problems, open dashboard
   bash mailcow_dashboard.sh

5. Export for records
   python3 mailcow_monitor.py --export report_$(date +%Y%m%d).json

6. Set up monitoring
   # Add cron job
   crontab -e
   # Add: 0 8 * * * cd /home/newuser/Reste-Rampe && ...


════════════════════════════════════════════════════════════════════════════

📚 MORE DOCUMENTATION
════════════════════════════════════════════════════════════════════════════

# Read full monitoring guide
cat MAILCOW_MONITORING.md

# View monitoring tool help
python3 mailcow_monitor.py --help

# Check other tools
ls -la *.sh *.py *.md | grep -i "mail\|monitor\|health"

# See all documentation
cat README_PRODUCTION.md


════════════════════════════════════════════════════════════════════════════

✅ QUICK CHECKLIST
════════════════════════════════════════════════════════════════════════════

Before monitoring, ensure:
☑ SSH working without password (ssh reste-rampe)
☑ .env configured with real Mailcow API key
☑ Backend container running (docker-compose ps)
☑ Mailcow API accessible (curl to API endpoint)
☑ Python 3 installed (python3 --version)
☑ Scripts executable (ls -l mailcow_*.py)


════════════════════════════════════════════════════════════════════════════

🆘 HELP & SUPPORT
════════════════════════════════════════════════════════════════════════════

# View documentation
cat MAILCOW_MONITORING.md | less

# Check logs
docker-compose logs backend | grep -i mailcow

# Debug mode
python3 mailcow_monitor.py --debug

# Test API directly
curl -v -H "X-API-Key: $API_KEY" \
  https://mailcow.rest-rampe.tech:1443/api/v1/status/version

# Restart services
docker-compose restart backend

# Validate configuration
grep "^MAILCOW" .env

════════════════════════════════════════════════════════════════════════════

That's it! You now have everything you need to monitor Mailcow! 🐮

EOF
