# 🍽️ Reste-Rampe - Production Deployment

> Nachhaltig kochen, Lebensmittel retten - jetzt mit vollständiger Mailcow Integration!

## 🚀 Status: Live on Production

**Server:** 84.46.241.104  
**Deployment Date:** November 5, 2025  
**Status:** ✅ **LIVE**

---

## 📱 Zugriff

| Komponente | Link | Status |
|-----------|------|--------|
| **Frontend** | http://84.46.241.104 | ✅ Live |
| **API** | http://84.46.241.104:8000 | ✅ Live |
| **API Docs** | http://84.46.241.104:8000/docs | ✅ Live |
| **Custom Domain** | https://rest-rampe.tech | ⏳ Domain Setup |

---

## ✨ Neue Features (Deployed)

### 📧 Email Verification System
- User Registration mit Email-Bestätigung
- Token-basierte Verification
- Automatische Email über Mailcow SMTP
- **Status:** ✅ Ready to test

### 📮 Mailcow REST API Integration
- ✅ Mailbox erstellen/löschen
- ✅ Email Forwarding verwalten
- ✅ Quota Management
- ✅ Admin Dashboard
- **Status:** ⏳ Braucht Mailcow API Key

### 🗄️ Database Erweiterung
- 5 neue Spalten für Mailbox Management
- Email Verification Fields
- Admin Features
- **Status:** ✅ Applied

### 🎨 Frontend Updates
- Mailbox Management UI (Vue3)
- Email Verification Flow
- i18n (German/English)
- **Status:** ✅ Deployed

---

## 🔧 Quick Start für Admins

### SSH verbinden (ohne Passwort!)
```bash
ssh reste-rampe
cd /home/newuser/Reste-Rampe
```

### Container Status prüfen
```bash
docker-compose ps
```

### Health Check ausführen
```bash
bash health_check.sh
```

### Logs anschauen
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f db
```

---

## ⚙️ Was ist noch zu tun?

### 🔑 Priority 1: Mailcow API Key
1. Log in zu Mailcow Admin Panel
2. Gehe zu: System > API
3. Kopiere den API Key
4. Öffne `.env` Datei auf dem Server
5. Ersetze `your_api_key_here` mit deinem Key
6. Starte Backend neu: `docker-compose restart backend`

**Datei:** `MAILCOW_API_KEY_SETUP.md`

### 🔒 Priority 2: SSL Certificate
- Benötigt: Certbot + Let's Encrypt
- Domain: rest-rampe.tech
- Datei: `DEPLOYMENT_COMPLETE.md`

### 🌐 Priority 3: Custom Domain
- DNS Records updaten
- Nginx Config anpassen
- Datei: `DEPLOYMENT_COMPLETE.md`

---

## 📊 System Info

### Docker Services
```
Frontend  (Nginx)     → Port 80, 443
Backend   (FastAPI)   → Port 8000
Database  (PostgreSQL) → Port 5432
```

### Stack
- **Frontend:** Vue3 + Tailwind CSS
- **Backend:** FastAPI + SQLAlchemy
- **Database:** PostgreSQL 15
- **Email:** Mailcow + REST API
- **Auth:** JWT + Argon2

---

## 📚 Dokumentation

| Datei | Beschreibung |
|-------|-------------|
| `DEPLOYMENT_COMPLETE.md` | 📊 Vollständiger Deployment-Report |
| `MAILCOW_API_KEY_SETUP.md` | 🔧 Mailcow Integration Guide |
| `SERVER_CHEATSHEET.sh` | ⚡ Quick Reference Commands |
| `health_check.sh` | 🏥 Monitoring Script |
| `MAILCOW_API_SETUP.md` | 📖 API Documentation |

---

## 🧪 Testing

### API Health
```bash
curl http://84.46.241.104:8000/api/health
```

### Register User
```bash
curl -X POST http://84.46.241.104:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username":"testuser",
    "email":"test@example.com",
    "password":"password123"
  }'
```

### Frontend
Öffne im Browser: http://84.46.241.104

---

## 🛠️ Häufige Commands

```bash
# SSH verbinden
ssh reste-rampe

# Container neustarten
docker-compose restart backend

# Logs anschauen
docker-compose logs backend | tail -50

# In Datenbank
docker-compose exec db psql -U reste -d reste-rampe-db

# Backup erstellen
docker-compose exec db pg_dump -U reste reste-rampe-db > backup.sql

# Health Check
bash health_check.sh
```

---

## 🔐 Security

- ✅ SSH Key Authentication (kein Passwort!)
- ✅ Database Password gesetzt
- ✅ CORS konfiguriert
- ✅ API Key Authentication ready
- ⏳ SSL/TLS (zu konfigurieren)
- ⏳ Firewall Rules (nach Bedarf)

---

## 📞 Support

**Probleme?**
1. Logs anschauen: `docker-compose logs backend`
2. Health Check: `bash health_check.sh`
3. Siehe `SERVER_CHEATSHEET.sh` für Commands

**Fehler Messages?**
Siehe `DEPLOYMENT_COMPLETE.md` - Troubleshooting Section

---

## 🎯 Nächste Schritte

1. **Mailcow API Key konfigurieren** (Priority!)
2. SSL Zertifikat einrichten
3. Custom Domain setup
4. Comprehensive testing
5. Monitoring einrichten (optional)

---

**Made with ❤️ by GitHub Copilot**  
**Deployment:** November 5, 2025
