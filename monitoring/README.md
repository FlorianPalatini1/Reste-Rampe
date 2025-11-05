# 🐮 Mailcow Monitoring Dashboard

**Professional real-time monitoring dashboard for Mailcow REST API**

> Access at: `http://84.46.241.104/monitoring`

---

## 🎯 What's Included?

```
monitoring/
├── 📱 frontend/           # Web Dashboard (Nginx + HTML5)
│   ├── index.html         # Responsive UI with charts
│   ├── nginx.conf         # Reverse proxy config
│   └── Dockerfile         # Container definition
│
├── 🔧 backend/            # API Backend (FastAPI)
│   ├── main.py            # REST API with Mailcow integration
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile         # Container definition
│
├── 🐳 docker-compose.yml  # Services orchestration
├── .env.example           # Configuration template
├── deploy.sh              # Automated setup script
└── MONITORING_DASHBOARD_SETUP.md  # Full documentation
```

---

## ⚡ Quick Start (5 Minutes)

### 1️⃣ Navigate to monitoring folder
```bash
cd /home/newuser/Reste-Rampe/monitoring
```

### 2️⃣ Configure your API credentials
```bash
cp .env.example .env
nano .env

# Edit these values:
MAILCOW_API_URL=https://mailcow.rest-rampe.tech/api/v1
MAILCOW_API_KEY=your_real_api_key_here
MAILCOW_VERIFY_SSL=false
```

### 3️⃣ Deploy with one command
```bash
bash deploy.sh
```

### 4️⃣ Open in browser
```
http://84.46.241.104/monitoring
```

---

## 🎨 Dashboard Features

### 📊 Real-time Metrics
- API Health Status (with response time)
- Total Mailboxes Count
- Average Quota Usage %
- Total Storage Used / Available

### 📬 Mailbox Table
- Mailbox address
- Storage usage (MB)
- Quota limits (MB)
- Usage percentage with visual bar
- Status indicator (HEALTHY/WARNING/CRITICAL)

### 📈 Charts & Analytics
- **Usage Trend** - Line chart of quota usage over time
- **Distribution** - Pie chart of mailbox storage usage

### 🔀 Forwarding Rules
- Source email address
- Destination addresses
- Active/Inactive status

### 🎛️ Status Indicators

| Status | Color | Condition | Icon |
|--------|-------|-----------|------|
| **HEALTHY** | 🟢 Green | 0-75% quota | ✅ |
| **WARNING** | 🟡 Yellow | 75-90% quota | ⚠️ |
| **CRITICAL** | 🔴 Red | >90% quota | ❌ |

---

## 🛠️ Manual Setup (Alternative to `deploy.sh`)

```bash
# Navigate to monitoring
cd /home/newuser/Reste-Rampe/monitoring

# Configure
cp .env.example .env
nano .env  # Add your API credentials

# Build Docker images
docker-compose build

# Start services
docker-compose up -d

# Verify
docker-compose ps

# Check logs
docker-compose logs -f
```

---

## 📋 API Endpoints

Access the backend API directly for integration:

```bash
# Health check
curl http://localhost/api/monitoring/health

# API Health
curl http://localhost/api/monitoring/api/health

# Get all mailboxes
curl http://localhost/api/monitoring/api/mailboxes

# Get forwarding rules
curl http://localhost/api/monitoring/api/forwarding

# Complete system stats
curl http://localhost/api/monitoring/api/stats

# Quick status
curl http://localhost/api/monitoring/api/status

# Historical data
curl http://localhost/api/monitoring/api/history?limit=100
```

---

## 🔐 Security

✅ **No hardcoded credentials** - Uses .env configuration  
✅ **API key from environment** - Never exposed in code  
✅ **CORS enabled** - For cross-origin access  
✅ **SSL/TLS ready** - Supports secure connections  
✅ **Input validation** - Pydantic models for validation  

---

## 🐛 Troubleshooting

### Dashboard won't load?

```bash
# Check if services are running
docker-compose ps

# View logs
docker-compose logs monitoring-frontend

# Restart
docker-compose restart
```

### No mailboxes showing?

```bash
# Verify API configuration
cat .env | grep MAILCOW

# Test API connection
docker exec monitoring-backend curl -v \
  https://mailcow.rest-rampe.tech/api/v1/status

# Check backend logs
docker-compose logs monitoring-backend
```

### Port 80 already in use?

```bash
# Find what's using port 80
sudo lsof -i :80

# Stop conflicting service
# or change port in docker-compose.yml
```

---

## 🚀 Docker Commands

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Restart specific service
docker-compose restart monitoring-backend

# View running containers
docker-compose ps

# Execute command in container
docker-compose exec monitoring-backend bash

# View resource usage
docker stats
```

---

## 📊 Data Retention

- Historical data stored in memory (not persistent)
- ~2880 data points kept (24 hours at 30-second intervals)
- Data resets on container restart
- For persistent storage, integrate with PostgreSQL

---

## 🔄 Auto-Refresh

Dashboard automatically refreshes every **30 seconds**  
Manual refresh available via **🔄 Refresh** button

To change refresh interval, edit `index.html` line ~350:
```javascript
// Refresh every 30 seconds (30000 ms)
setInterval(refreshData, 30000);
```

---

## 📱 Features

- ✅ Responsive design (mobile/tablet/desktop)
- ✅ Real-time data updates
- ✅ Beautiful dark theme
- ✅ Color-coded status indicators
- ✅ Interactive charts (Chart.js)
- ✅ Zero external APIs (self-contained)
- ✅ Fast load time (lightweight)
- ✅ Works offline (after initial load)

---

## 🎯 Use Cases

### Daily Monitoring
```bash
ssh reste-rampe
# Open http://84.46.241.104/monitoring
# Review all metrics
```

### Automated Alerts
```bash
# Check status periodically
0 * * * * curl -s http://localhost/api/monitoring/api/status | \
  grep CRITICAL && mail -s "Alert" admin@example.com
```

### Export Reports
```bash
# Save daily stats
curl -s http://localhost/api/monitoring/api/stats > \
  /var/backups/mailcow-$(date +%Y-%m-%d).json
```

### Integration
```bash
# Prometheus scrape
scrape_configs:
  - job_name: 'mailcow'
    static_configs:
      - targets: ['localhost:8888']
```

---

## 📚 Full Documentation

For detailed setup, configuration, and troubleshooting:

```bash
cat MONITORING_DASHBOARD_SETUP.md
```

---

## 🛠️ Tech Stack

**Frontend:**
- HTML5
- Tailwind CSS
- Chart.js (data visualization)
- Pure JavaScript (no frameworks)

**Backend:**
- FastAPI (Python web framework)
- Uvicorn (ASGI server)
- httpx (async HTTP client)
- Pydantic (data validation)

**Infrastructure:**
- Docker (containerization)
- Docker Compose (orchestration)
- Nginx (reverse proxy)

---

## 🤝 Support

**Having issues?**

1. Check logs: `docker-compose logs -f`
2. Verify .env: `cat .env`
3. Test API: `curl http://localhost:8888/health`
4. Read docs: `MONITORING_DASHBOARD_SETUP.md`

---

## 📝 Configuration

### Required `.env` Variables

```env
# Mailcow API Configuration
MAILCOW_API_URL=https://mailcow.rest-rampe.tech/api/v1
MAILCOW_API_KEY=your_api_key_from_mailcow_admin
MAILCOW_VERIFY_SSL=false  # Set to true for production SSL
```

### Optional Settings

```env
# Dashboard refresh interval (seconds)
UPDATE_INTERVAL=30

# Historical data retention (hours)
HISTORY_RETENTION=24
```

---

## 🎉 Next Steps

1. ✅ Configure .env with your Mailcow credentials
2. ✅ Run `bash deploy.sh` to deploy
3. ✅ Open `http://84.46.241.104/monitoring`
4. ⏳ Set up alerts (optional)
5. ⏳ Integrate with monitoring systems (optional)
6. ⏳ Configure HTTPS/SSL (optional)

---

## 📞 Quick Commands Reference

```bash
# Setup
cd /home/newuser/Reste-Rampe/monitoring
bash deploy.sh

# Manage services
docker-compose up -d
docker-compose down
docker-compose restart

# View status
docker-compose ps
docker-compose logs -f

# Test API
curl http://localhost/api/monitoring/api/health
curl http://localhost/api/monitoring/api/stats

# SSH access
ssh reste-rampe
docker exec -it monitoring-backend bash
```

---

**Version:** 1.0.0  
**Created:** November 5, 2024  
**Status:** ✅ Production Ready

🐮 **Happy Monitoring!**
