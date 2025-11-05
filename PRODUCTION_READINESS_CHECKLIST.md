# ✅ Production Readiness Checklist

> Überprüfe diese Items vor dem Launch

---

## 🚀 Pre-Launch Checklist

### Phase 1: Infrastructure ✓

- [x] Server aufgesetzt (Ubuntu 22.04 LTS)
- [x] SSH Key Authentication konfiguriert
- [x] Docker & Docker Compose installiert
- [x] All 3 Container laufen (backend, frontend, database)
- [x] Database initialized with schema
- [x] Ports 80, 443 offen

### Phase 2: Application Code ✓

- [x] Frontend Vue3 Komponenten kompiliert
- [x] Backend FastAPI Endpoints getestet
- [x] API Dokumentation verfügbar (/docs)
- [x] Error Handling implementiert
- [x] Logging konfiguriert
- [x] Environment Variables gesetzt

### Phase 3: Database ✓

- [x] PostgreSQL 15 läuft
- [x] Database Schema applied
- [x] Mailbox columns added
- [x] Data persistence Volume configured
- [x] Backup procedure ready

### Phase 4: Security

- [ ] SSL/TLS Certificate (Let's Encrypt)
- [ ] HTTPS aktiviert & HTTP redirects
- [ ] Security Headers in Nginx
- [ ] CORS richtig konfiguriert
- [ ] API Rate Limiting
- [ ] Input Validation überall
- [ ] SQL Injection Protection (SQLAlchemy ORM)
- [ ] CSRF Protection (if needed)
- [ ] Secrets nicht in Git
- [ ] Database Password gesetzt
- [ ] Regular Security Updates geplant

### Phase 5: Monitoring & Logging

- [ ] Health Check Endpoint
- [ ] Logging auf Disk
- [ ] Log Rotation konfiguriert
- [ ] Monitoring Script aktiv
- [ ] Alerting konfiguriert (optional)
- [ ] Performance Metrics tracked

### Phase 6: Email & Mailcow

- [ ] Mailcow SMTP funktioniert
- [ ] Mailcow REST API Key konfiguriert
- [ ] Email Verification Flow getestet
- [ ] Mailbox Creation getestet
- [ ] Email Forwarding getestet
- [ ] Admin Features getestet

### Phase 7: Domain & DNS

- [ ] Domain registriert
- [ ] DNS A Record eingestellt
- [ ] DNS CNAME Record eingestellt (optional)
- [ ] DNS Propagation verifiziert
- [ ] Domain resolves zu Server IP

### Phase 8: Documentation

- [x] README_PRODUCTION.md
- [x] SSL_SETUP.md
- [x] SSL_DOMAIN_COMPLETE_GUIDE.md
- [x] DEPLOYMENT_COMPLETE.md
- [x] SERVER_CHEATSHEET.sh
- [x] MAILCOW_API_KEY_SETUP.md
- [ ] User Documentation
- [ ] Admin Documentation
- [ ] API Documentation (auto via /docs)

### Phase 9: Backups & Disaster Recovery

- [ ] Database Backup Plan
- [ ] Backup Testing (Restore Test)
- [ ] Backup Location (off-site)
- [ ] Recovery Time Objective (RTO) defined
- [ ] Recovery Point Objective (RPO) defined

### Phase 10: Compliance & Legal

- [ ] Privacy Policy (if required)
- [ ] Terms of Service (if required)
- [ ] GDPR Compliance (if EU users)
- [ ] Data Retention Policy
- [ ] Cookie Consent (if needed)

---

## 🔐 Security Hardening Checklist

### Network Security

- [ ] Firewall konfiguriert (ufw / iptables)
- [ ] SSH Port ≠ 22 (optional)
- [ ] SSH Key-only auth (no password)
- [ ] SSH root login disabled
- [ ] Fail2ban installiert (optional)

### Application Security

- [ ] Secrets in .env (not in code)
- [ ] API Keys rotated
- [ ] HTTPS enforced
- [ ] Security Headers set (HSTS, etc.)
- [ ] CORS whitelist configured
- [ ] Input Validation on all endpoints
- [ ] Error messages don't leak info
- [ ] No DEBUG mode in production

### Database Security

- [ ] Strong database password
- [ ] Database nicht exposed
- [ ] Only needed ports open
- [ ] Regular backups encrypted
- [ ] Sensitive data encrypted (if needed)

### Infrastructure Security

- [ ] OS Security Updates installed
- [ ] Docker Security Best Practices
- [ ] Regular vulnerability scans
- [ ] Intrusion Detection (optional)
- [ ] Antivirus (if needed)

---

## 🧪 Testing Checklist

### Manual Testing

- [ ] User Registration Flow
- [ ] Email Verification Flow
- [ ] Login/Logout Flow
- [ ] Create Mailbox
- [ ] Delete Mailbox
- [ ] Add Email Forwarding
- [ ] Remove Email Forwarding
- [ ] Admin Dashboard
- [ ] User Profile Management

### API Testing

```bash
# Health Check
curl https://rest-rampe.tech/api/health

# Register User
curl -X POST https://rest-rampe.tech/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@example.com","password":"test123"}'

# Login
curl -X POST https://rest-rampe.tech/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"test123"}'

# Get Mailbox
curl https://rest-rampe.tech/api/mailbox \
  -H "Authorization: Bearer {token}"
```

### Browser Testing

- [ ] Frontend loads without errors
- [ ] Responsive design (mobile/tablet/desktop)
- [ ] All forms work
- [ ] API calls successful
- [ ] No console errors
- [ ] No security warnings
- [ ] Performance acceptable (< 3s load)

### Load Testing (optional)

```bash
# Einfaches Load Test mit Apache Bench
ab -n 100 -c 10 https://rest-rampe.tech/

# Oder mit wrk:
wrk -t4 -c100 -d30s https://rest-rampe.tech/
```

---

## 📊 Performance Checklist

### Frontend Performance

- [ ] Bundle Size < 500KB
- [ ] CSS minified & concatenated
- [ ] Images optimized
- [ ] JavaScript minified
- [ ] Lazy Loading for images
- [ ] Cache Policy set (max-age > 1 year for assets)

### Backend Performance

- [ ] Database Queries optimized
- [ ] No N+1 queries
- [ ] Connection Pooling configured
- [ ] Caching strategy in place (if needed)
- [ ] Response times < 500ms

### Infrastructure Performance

- [ ] CPU usage < 50%
- [ ] Memory usage < 75%
- [ ] Disk usage < 80%
- [ ] Network latency acceptable
- [ ] No hanging processes

---

## 🚨 Incident Response Checklist

### On Error

- [ ] Check Application Logs: `docker-compose logs backend`
- [ ] Check Database: `docker-compose logs db`
- [ ] Check Nginx: `sudo tail -50 /var/log/nginx/error.log`
- [ ] Check Health: `bash health_check.sh`
- [ ] Check Disk Space: `df -h`
- [ ] Check Memory: `free -h`
- [ ] Restart Container: `docker-compose restart backend`
- [ ] Check Certbot: `sudo certbot certificates`

### On Data Loss

- [ ] Stop all containers: `docker-compose down`
- [ ] Restore from backup: `psql < backup.sql`
- [ ] Verify data integrity
- [ ] Restart containers: `docker-compose up -d`

---

## 📋 Day-1 Operations Checklist

Nach Launch:

- [ ] Monitor System Health (health_check.sh)
- [ ] Check Error Logs
- [ ] Verify All Users Can Register
- [ ] Verify Email Verification Works
- [ ] Verify Mailbox Creation
- [ ] Monitor Server Resources
- [ ] Check Certbot Renewal Status
- [ ] Backup Database

---

## 🔄 Ongoing Maintenance Checklist

### Weekly

- [ ] Check system logs for errors
- [ ] Monitor disk usage
- [ ] Verify backups completed
- [ ] Check SSL certificate expiry

### Monthly

- [ ] Update OS packages: `sudo apt update && sudo apt upgrade`
- [ ] Review access logs
- [ ] Check database size
- [ ] Performance review

### Quarterly

- [ ] Security audit
- [ ] Performance optimization
- [ ] Backup restoration test
- [ ] Update Docker images

### Yearly

- [ ] Full security audit
- [ ] Code review
- [ ] Architecture review
- [ ] Capacity planning

---

## ✅ Pre-Launch Final Verification

### 48 Hours Before Launch

```bash
ssh reste-rampe
cd /home/newuser/Reste-Rampe

# 1. System Check
bash health_check.sh

# 2. Database Check
docker-compose exec db psql -U reste -d reste-rampe-db -c "SELECT COUNT(*) FROM \"user\";"

# 3. API Check
curl -I https://rest-rampe.tech/api/health

# 4. Frontend Check
curl -I https://rest-rampe.tech

# 5. SSL Check
sudo certbot certificates

# 6. Disk Space
df -h

# 7. Memory
free -h

# 8. Certbot Timer
sudo systemctl status certbot.timer
```

### Launch Day Checklist

- [ ] Final database backup
- [ ] Final logs rotation
- [ ] Team notified
- [ ] Monitoring active
- [ ] Support team on standby
- [ ] Rollback plan ready

---

## 🎯 Success Criteria

Launch ist erfolgreich wenn:

✅ All Services Up & Running  
✅ 0 Errors in health_check.sh  
✅ SSL Certificate Valid & Auto-Renewal Active  
✅ Users Can Register & Verify Email  
✅ Mailbox Creation Working  
✅ Admin Dashboard Accessible  
✅ API Responding < 500ms  
✅ No Security Warnings  
✅ Monitoring & Backups Automated  

---

## 📞 Emergency Contacts

- **Server Host:** Contabo Support
- **Domain Registrar:** Namecheap / GoDaddy Support
- **Let's Encrypt:** https://letsencrypt.org/contact/
- **Docker Issues:** https://docs.docker.com/

---

## 📝 Launch Sign-Off

**Date:** _______________  
**By:** _______________  
**Server IP:** 84.46.241.104  
**Domain:** rest-rampe.tech  
**Status:** ⬜ Not Ready | 🟡 Partial | 🟢 Ready  

---

**Generated:** November 5, 2025  
**Next Review:** [Schedule Date]
