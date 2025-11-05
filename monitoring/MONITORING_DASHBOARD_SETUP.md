# Mailcow Monitoring Dashboard Setup Guide

## 🎯 Overview

A professional, real-time monitoring dashboard for Mailcow that runs as a separate Docker container and is accessible via `http://server-ip/monitoring`.

**Features:**
- ✅ Real-time API health monitoring
- ✅ Live mailbox quota tracking
- ✅ Beautiful interactive dashboard
- ✅ Usage trend charts
- ✅ Automatic data refresh (every 30 seconds)
- ✅ Forwarding rules display
- ✅ Status indicators (HEALTHY/WARNING/CRITICAL)
- ✅ No external dependencies

---

## 📦 Architecture

```
monitoring/
├── backend/
│   ├── main.py              # FastAPI backend (port 8888)
│   ├── requirements.txt      # Python dependencies
│   └── Dockerfile           # Container definition
├── frontend/
│   ├── index.html           # Dashboard UI (standalone)
│   ├── Dashboard.vue        # Vue3 component (alternative)
│   ├── nginx.conf           # Nginx proxy config
│   └── Dockerfile           # Container definition
└── docker-compose.yml       # Orchestration

Nginx (port 80) → Routes requests
├── / → Static HTML Dashboard
└── /api/monitoring/* → Backend API
```

---

## 🚀 Quick Start

### Step 1: Copy Configuration

```bash
cd /home/newuser/Reste-Rampe/monitoring
cp .env.example .env
```

### Step 2: Configure Mailcow API

Edit `.env` and add your Mailcow credentials:

```bash
# Get API URL (usually https://mailcow.example.com/api/v1)
MAILCOW_API_URL=https://mailcow.rest-rampe.tech/api/v1

# Get API Key from Mailcow Admin Panel:
# 1. Login to Mailcow admin
# 2. Go to System → API
# 3. Copy your API key
MAILCOW_API_KEY=your_real_api_key_here

# For production with SSL
MAILCOW_VERIFY_SSL=true
```

### Step 3: Build & Start Containers

```bash
# Navigate to monitoring directory
cd /home/newuser/Reste-Rampe/monitoring

# Build images
docker-compose build

# Start services
docker-compose up -d

# Check status
docker-compose ps
```

### Step 4: Access Dashboard

Open your browser and navigate to:
```
http://84.46.241.104/monitoring
```

---

## 🎨 Dashboard Features

### Header Section
- 🔄 **Refresh Button** - Manual data refresh
- 📊 **Last Update** - Shows when data was last updated
- Auto-refresh every 30 seconds

### Status Cards
```
┌─────────────────────────┐
│ API Health: HEALTHY     │  ✅ (with response time)
│ Mailboxes: 5            │  📧 (total count)
│ Avg Usage: 45.2%        │  📊 (average quota)
│ Total Usage: 125.5 GB   │  💾 (total storage)
└─────────────────────────┘
```

### Mailbox Table
Shows detailed breakdown:
- Mailbox address
- Used space (MB)
- Total quota (MB)
- Usage percentage with visual bar
- Status badge (HEALTHY/WARNING/CRITICAL)

### Charts
- **Usage Trend** - Line chart showing usage over time
- **Distribution** - Pie chart of top 5 mailboxes

### Forwarding Rules
- Lists all active forwarding rules
- Shows source and destinations
- Active/inactive status

---

## 🔧 API Endpoints

### Backend API (`/api/monitoring/api/...`)

```
GET /health
  → Check backend health
  ← {"status": "ok", "timestamp": "2024-11-05..."}

GET /api/health
  → Check Mailcow API health
  ← {
      "status": "HEALTHY",
      "response_time_ms": 45.2,
      "timestamp": "..."
    }

GET /api/mailboxes
  → Get all mailboxes and quota
  ← {
      "total_mailboxes": 5,
      "total_quota_mb": 5000,
      "total_used_mb": 1250,
      "average_usage_percent": 25.0,
      "status": "HEALTHY",
      "mailboxes": [...]
    }

GET /api/forwarding
  → Get forwarding rules
  ← [
      {
        "source": "user@domain.com",
        "destinations": ["forward@example.com"],
        "active": true
      }
    ]

GET /api/stats
  → Get complete system statistics
  ← {
      "api_health": {...},
      "mailbox_summary": {...},
      "forwarding_rules": [...],
      "collection_timestamp": "..."
    }

GET /api/history?limit=100
  → Get historical trend data
  ← [
      {
        "timestamp": "...",
        "total_used_mb": 1250,
        "average_usage_percent": 25.0,
        "mailbox_count": 5
      }
    ]

GET /api/status
  → Quick status summary
  ← {
      "overall_status": "HEALTHY",
      "total_mailboxes": 5,
      "average_usage": 25.0,
      "api_health": "HEALTHY",
      "timestamp": "..."
    }
```

---

## 📊 Status Levels

| Status | Color | Condition | Action |
|--------|-------|-----------|--------|
| HEALTHY | 🟢 Green | 0-75% quota | None needed |
| WARNING | 🟡 Yellow | 75-90% quota | Monitor user |
| CRITICAL | 🔴 Red | >90% quota | Alert user |

---

## 🔐 Security Considerations

1. **API Key Security**
   - Never commit `.env` to git
   - Keep API key confidential
   - Use strong, unique keys

2. **Network Security**
   - Place behind reverse proxy (Nginx)
   - Use HTTPS in production
   - Restrict access if needed

3. **Data Privacy**
   - Historical data stored in memory (not persisted)
   - Dashboard shows mailbox usage (pseudo-public info)
   - No user credentials exposed

---

## 🐛 Troubleshooting

### Dashboard shows "No mailboxes available"

**Problem:** Mailcow API not responding or key invalid

**Solutions:**
```bash
# Check backend logs
docker-compose logs monitoring-backend

# Verify API key
cat .env | grep MAILCOW_API_KEY

# Test API manually
curl -X GET "https://mailcow.rest-rampe.tech/api/v1/mailbox" \
  -H "X-API-Key: your_api_key_here"

# Verify API URL format
# Should be: https://mailcow.domain.com/api/v1
# NOT: https://mailcow.domain.com/api/v1/
```

### Dashboard won't load (404)

**Problem:** Frontend container not running or Nginx misconfigured

**Solutions:**
```bash
# Check if container is running
docker-compose ps

# Check frontend logs
docker-compose logs monitoring-frontend

# Verify Nginx config
docker exec monitoring-frontend nginx -t

# Restart frontend
docker-compose restart monitoring-frontend
```

### API Health shows CRITICAL

**Problem:** Cannot connect to Mailcow API

**Solutions:**
```bash
# 1. Verify URL is correct
docker exec monitoring-backend curl -I https://mailcow.rest-rampe.tech/api/v1/status

# 2. Check SSL certificate (if MAILCOW_VERIFY_SSL=true)
docker exec monitoring-backend curl -v https://mailcow.rest-rampe.tech/api/v1/status

# 3. For self-signed certs, use MAILCOW_VERIFY_SSL=false
```

### Containers won't start

**Problem:** Port already in use or build error

**Solutions:**
```bash
# Check what's using port 80
sudo lsof -i :80

# Stop conflicting services
docker-compose down

# Clean up and rebuild
docker-compose down --volumes
docker-compose build --no-cache
docker-compose up -d
```

---

## 📈 Performance Tips

1. **Optimize Refresh Rate**
   - Default: 30 seconds
   - Edit: JavaScript in `index.html` (line ~350)
   - Lower = more responsive but more API calls
   - Higher = less API load but stale data

2. **Historical Data**
   - Stored in memory (not persistent)
   - Limited to ~2880 points (24 hours at 30s intervals)
   - Data lost on container restart

3. **Large Deployments**
   - Consider PostgreSQL for historical data
   - Add data persistence layer
   - Implement aggregation for old data

---

## 🔄 Updating

### Update Backend Code

```bash
# 1. Modify backend/main.py
# 2. Rebuild container
docker-compose build monitoring-backend

# 3. Restart
docker-compose up -d monitoring-backend
```

### Update Frontend UI

```bash
# 1. Modify frontend/index.html
# 2. Rebuild container
docker-compose build monitoring-frontend

# 3. Restart
docker-compose up -d monitoring-frontend
```

### Update Both

```bash
docker-compose down
docker-compose build
docker-compose up -d
```

---

## 📋 Environment Variables

```env
# API Configuration
MAILCOW_API_URL=https://mailcow.example.com/api/v1
MAILCOW_API_KEY=your_api_key_here
MAILCOW_VERIFY_SSL=false  # Set to true in production

# Dashboard Settings
UPDATE_INTERVAL=30  # Seconds between API calls
HISTORY_RETENTION=24  # Hours of historical data
```

---

## 📊 Data Flow

```
Dashboard (Frontend)
    ↓ (HTTP Request)
Nginx Reverse Proxy
    ↓
Backend API (FastAPI)
    ↓ (Async Request)
Mailcow API
    ↓ (Response)
Backend Processing
    ↓ (JSON Response)
Frontend Rendering
    ↓
Display Dashboard
```

---

## 🎯 Common Use Cases

### Use Case 1: Daily Monitoring
```bash
# SSH to server
ssh reste-rampe

# Open dashboard in browser
# http://84.46.241.104/monitoring

# Review metrics
```

### Use Case 2: Alert on Critical Usage
```bash
# Create cron job to check status
0 */6 * * * curl -s http://localhost/api/monitoring/api/status | grep -q CRITICAL && \
  mail -s "CRITICAL: Mailcow quota alert" admin@example.com
```

### Use Case 3: Export Daily Report
```bash
# Via API
curl -s http://localhost/api/monitoring/api/stats > \
  /var/backups/mailcow_stats_$(date +%Y-%m-%d).json
```

### Use Case 4: Integration with Nagios/Prometheus
```bash
# Prometheus scrape config
scrape_configs:
  - job_name: 'mailcow-monitoring'
    static_configs:
      - targets: ['localhost:8888']
```

---

## 📞 Support

For issues or questions:

1. Check logs: `docker-compose logs -f`
2. Verify configuration: `cat .env`
3. Test API: `curl -X GET http://localhost:8888/health`
4. Review troubleshooting section above

---

## 🎉 What's Next?

1. ✅ Dashboard running and accessible
2. ⏳ Configure alerts (optional)
3. ⏳ Set up backups for historical data
4. ⏳ Integrate with other monitoring tools
5. ⏳ Deploy to production with SSL/TLS

---

**Created:** November 5, 2024  
**Version:** 1.0.0  
**Status:** Production Ready
