# 🐮 Mailcow REST API Monitoring Tools

> Professional monitoring suite for Mailcow REST API

---

## 📋 Overview

Diese Monitoring Tools ermöglichen:

- ✅ Real-time API Health Checks
- ✅ Mailbox Quota Monitoring
- ✅ Forwarding Rules Tracking
- ✅ Performance Metrics
- ✅ Email Alerts (optional)
- ✅ JSON Reports Export
- ✅ Live Dashboard
- ✅ Historical Data

---

## 🛠️ Available Tools

### 1. **mailcow_monitor.py** - Python Monitoring Client

**Features:**
- Professional Python API client
- Real-time health checks
- Color-coded terminal output
- JSON export
- Watch mode (continuous monitoring)
- Full error handling

**Installation:**

```bash
# Python 3 required (usually preinstalled)
python3 --version

# No external dependencies needed (uses built-in requests)
# If requests not installed:
pip3 install requests
```

**Usage:**

```bash
# Single report
python3 mailcow_monitor.py

# Watch mode (updates every 60 seconds)
python3 mailcow_monitor.py --watch 60

# Export to JSON
python3 mailcow_monitor.py --export report.json

# With custom config
python3 mailcow_monitor.py --config /path/to/.env

# Debug mode
python3 mailcow_monitor.py --debug
```

**Output Example:**

```
════════════════════════════════════════════════════════════════════════════
🐮 MAILCOW MONITORING REPORT
Time: 2025-11-05T12:34:56.789123

API Health:
  Status: HEALTHY
  Response Time: 245.32ms

Overall Status: HEALTHY

Mailboxes:
Name                           Domain               Usage              Status
────────────────────────────────────────────────────────────────────────────
user1                          rest-rampe.tech      124MB / 5120MB [██░░░░░░░░] 2.4%   HEALTHY
user2                          rest-rampe.tech      4089MB / 5120MB [█████████░] 79.8% WARNING

Summary:
  Total Mailboxes: 2
  Total Forwarding Rules: 3
  Healthy Mailboxes: 1
  Warning Mailboxes: 1
  Critical Mailboxes: 0

════════════════════════════════════════════════════════════════════════════
```

---

### 2. **mailcow_dashboard.sh** - Interactive Bash Dashboard

**Features:**
- Interaktives Menu-Interface
- Einfache Navigation
- Live Monitor Mode
- Configuration View
- Log Viewer
- JSON Export

**Usage:**

```bash
# Interactive Menu
bash mailcow_dashboard.sh

# Direct Commands
bash mailcow_dashboard.sh health       # Health check
bash mailcow_dashboard.sh mailboxes    # List mailboxes
bash mailcow_dashboard.sh quota        # Quota usage
bash mailcow_dashboard.sh forwarding   # Forwarding rules
bash mailcow_dashboard.sh export       # Export report
bash mailcow_dashboard.sh logs         # View logs
bash mailcow_dashboard.sh config       # Show config
bash mailcow_dashboard.sh live         # Live monitor
```

**Menu Options:**

```
1. 📊 View System Status
2. 📮 View All Mailboxes
3. 📈 View Quota Usage
4. 📤 View Forwarding Rules
5. 🏥 Health Check
6. 📡 Live Monitor (updates every 60s)
7. 💾 Export Report (JSON)
8. 📜 View Logs
9. 🔧 Configuration
0. ❌ Exit
```

---

## 📊 Monitoring Status Levels

### Status Meanings

| Status | Color | Meaning | Action |
|--------|-------|---------|--------|
| **HEALTHY** | 🟢 Green | Everything OK | None |
| **WARNING** | 🟡 Yellow | Quota > 75% | Monitor |
| **CRITICAL** | 🔴 Red | API Down or Quota > 90% | Immediate Action |
| **UNKNOWN** | 🔵 Blue | Cannot determine | Check logs |

### Quota Thresholds

- **0-75%**: HEALTHY ✅
- **75-90%**: WARNING ⚠️ (Alert user to clean up)
- **>90%**: CRITICAL ❌ (Block new emails)

---

## 🔧 Configuration

### Prerequisites

The tools read from your `.env` file on the server:

```bash
MAILCOW_API_URL=https://mailcow.rest-rampe.tech:1443/api/v1
MAILCOW_API_KEY=your_actual_api_key_here
MAILCOW_VERIFY_SSL=false
```

### Setup

1. **SSH to Server:**
   ```bash
   ssh reste-rampe
   cd /home/newuser/Reste-Rampe
   ```

2. **Make scripts executable:**
   ```bash
   chmod +x mailcow_monitor.py
   chmod +x mailcow_dashboard.sh
   ```

3. **Test configuration:**
   ```bash
   python3 mailcow_monitor.py
   # or
   bash mailcow_dashboard.sh health
   ```

---

## 🚀 Quick Start Guide

### For Beginners (Use Dashboard)

```bash
ssh reste-rampe
cd /home/newuser/Reste-Rampe

# Interactive menu
bash mailcow_dashboard.sh

# Then select options 1-9
```

### For Developers (Use Python Script)

```bash
ssh reste-rampe
cd /home/newuser/Reste-Rampe

# Single check
python3 mailcow_monitor.py

# Continuous monitoring (Ctrl+C to stop)
python3 mailcow_monitor.py --watch 60

# Export report
python3 mailcow_monitor.py --export report.json
```

### For Automation (Cron Jobs)

```bash
# Add to crontab
crontab -e

# Monitor every 5 minutes
*/5 * * * * cd /home/newuser/Reste-Rampe && python3 mailcow_monitor.py --export /tmp/mailcow_report_$(date +\%s).json

# Alert check every hour
0 * * * * cd /home/newuser/Reste-Rampe && bash mailcow_dashboard.sh quota | grep -i critical && echo "CRITICAL QUOTA ALERT" | mail -s "Mailcow Alert" admin@example.com
```

---

## 📈 Use Cases

### Use Case 1: Daily Health Check

```bash
# SSH to server and run
cd /home/newuser/Reste-Rampe
python3 mailcow_monitor.py
```

### Use Case 2: Monitor Quota in Real-Time

```bash
# Watch quota every minute
watch -n 60 'cd /home/newuser/Reste-Rampe && bash mailcow_dashboard.sh quota'
```

### Use Case 3: Export Daily Reports

```bash
# Create reports directory
mkdir -p reports

# Run daily at 8 AM
0 8 * * * cd /home/newuser/Reste-Rampe && python3 mailcow_monitor.py --export reports/report_$(date +\%Y-\%m-\%d).json
```

### Use Case 4: Alert on Critical Issues

```bash
#!/bin/bash
# save as: /home/newuser/Reste-Rampe/check_critical.sh

cd /home/newuser/Reste-Rampe
python3 mailcow_monitor.py --export /tmp/report.json

# Check for critical status
if grep -q '"CRITICAL"' /tmp/report.json; then
    echo "CRITICAL ALERT: Mailcow has critical issues!" | \
    mail -s "🚨 Mailcow Critical Alert" admin@rest-rampe.tech
fi
```

---

## 🔍 Troubleshooting

### Problem: "API Key not configured"

**Solution:**

```bash
ssh reste-rampe
cd /home/newuser/Reste-Rampe

# Check .env
cat .env | grep MAILCOW_API_KEY

# If empty or "your_api_key_here", configure it:
nano .env
# Find MAILCOW_API_KEY and set the real key

# Restart backend
docker-compose restart backend
```

### Problem: "Connection refused"

**Cause:** Mailcow API not running or URL wrong

**Solution:**

```bash
# Check if Mailcow is running
curl https://mailcow.rest-rampe.tech:1443/api/v1/status/version

# Check URL in .env
cat .env | grep MAILCOW_API_URL

# Should be something like:
# MAILCOW_API_URL=https://mailcow.rest-rampe.tech:1443/api/v1
```

### Problem: SSL Certificate Error

**Cause:** MAILCOW_VERIFY_SSL=true but cert invalid

**Solution:**

```bash
# Edit .env
nano .env

# Find and set:
MAILCOW_VERIFY_SSL=false

# Restart
docker-compose restart backend
```

### Problem: "No mailboxes found"

**Cause:** API Key may not have permission

**Solution:**

```bash
# Verify API Key in Mailcow Admin:
# 1. Log in to https://mailcow.rest-rampe.tech
# 2. System → API
# 3. Copy the correct API Key
# 4. Update .env
# 5. Restart backend

docker-compose restart backend
```

---

## 📊 JSON Export Format

**Example report.json:**

```json
{
  "timestamp": "2025-11-05T12:34:56.789123",
  "api_health": {
    "status": "HEALTHY",
    "response_time_ms": 245.32,
    "last_check": "2025-11-05T12:34:56.789123",
    "error_message": null
  },
  "mailboxes": [
    {
      "name": "user1",
      "domain": "rest-rampe.tech",
      "quota_mb": 5120,
      "used_mb": 124,
      "quota_percent": 2.4,
      "status": "HEALTHY",
      "timestamp": "2025-11-05T12:34:56.789123"
    }
  ],
  "forwardings": 3,
  "overall_status": "HEALTHY"
}
```

---

## 🔐 Security Best Practices

### API Key Safety

```bash
# ❌ DON'T: Hardcode API keys
API_KEY="your-key-here"  # Bad!

# ✅ DO: Read from .env
API_KEY=$(grep MAILCOW_API_KEY .env | cut -d= -f2)

# ✅ DO: Use environment variables
export MAILCOW_API_KEY="your-key"
```

### Log Security

```bash
# Ensure logs don't contain sensitive data
tail -f /home/newuser/Reste-Rampe/logs/mailcow/*

# If logs contain API keys, delete them
rm -f /home/newuser/Reste-Rampe/logs/mailcow/*
```

### SSL Verification

```bash
# ⚠️ Only use VERIFY_SSL=false for self-signed certs
# In production with valid certs:
MAILCOW_VERIFY_SSL=true
```

---

## 📞 Support & Help

### Quick Commands

```bash
# SSH to server
ssh reste-rampe
cd /home/newuser/Reste-Rampe

# Run monitoring
python3 mailcow_monitor.py

# Interactive dashboard
bash mailcow_dashboard.sh

# View logs
tail -50 /home/newuser/Reste-Rampe/logs/mailcow/*.json

# Check .env
grep MAILCOW .env

# Restart backend
docker-compose restart backend
```

### Health Check Commands

```bash
# API Status
curl -H "X-API-Key: YOUR_KEY" \
  https://mailcow.rest-rampe.tech:1443/api/v1/status/version

# List Mailboxes
curl -H "X-API-Key: YOUR_KEY" \
  https://mailcow.rest-rampe.tech:1443/api/v1/mailbox/all

# Get Quota
curl -H "X-API-Key: YOUR_KEY" \
  https://mailcow.rest-rampe.tech:1443/api/v1/mailbox/quota/user@rest-rampe.tech
```

---

## 🎯 Integration Examples

### Grafana Integration

```python
# Export Prometheus-compatible metrics
# (Can be extended to provide metrics for Grafana)
```

### Slack Notifications

```bash
# Add to check_critical.sh to send Slack notifications
SLACK_WEBHOOK="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
curl -X POST $SLACK_WEBHOOK \
  -H 'Content-type: application/json' \
  -d '{"text":"🚨 Mailcow Alert: Critical Status"}'
```

### Email Alerts

```bash
# Send email on critical status
if [ "$STATUS" = "CRITICAL" ]; then
  echo "Mailcow status is CRITICAL!" | \
  mail -s "🚨 Mailcow Alert" admin@rest-rampe.tech
fi
```

---

## 📝 Maintenance Schedule

### Daily
- Run health check manually or via cron

### Weekly
- Review quota usage
- Check for warning status mailboxes
- Export and archive reports

### Monthly
- Analyze trends
- Plan capacity upgrades if needed
- Clean old logs

---

## 🔄 Version History

- **v1.0** (Nov 5, 2025) - Initial release
  - API Health monitoring
  - Mailbox quota tracking
  - Forwarding rule management
  - JSON export
  - Interactive dashboard
  - Watch mode support

---

## 📚 References

- [Mailcow Admin Panel](https://mailcow.rest-rampe.tech)
- [REST API Documentation](SSL_SETUP.md)
- [System Health Check](health_check.sh)
- [Production Checklist](PRODUCTION_READINESS_CHECKLIST.md)

---

**Status:** 🟢 Production Ready  
**Last Updated:** November 5, 2025  
**Maintained by:** GitHub Copilot  
**License:** MIT
