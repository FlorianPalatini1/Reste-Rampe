# 🔒 SSL/TLS & Custom Domain Setup Guide

> Production-ready HTTPS mit Let's Encrypt

---

## 🎯 Ziele

- ✅ Let's Encrypt SSL Zertifikat einrichten
- ✅ Auto-Renewal mit Certbot
- ✅ Nginx für HTTPS konfigurieren
- ✅ HTTP zu HTTPS Redirect
- ✅ Custom Domain (rest-rampe.tech)

---

## 📋 Voraussetzungen

1. **Domain gekauft** → rest-rampe.tech
2. **DNS konfiguriert** → `A` Record: `rest-rampe.tech → 84.46.241.104`
3. **SSH Zugang** → `ssh reste-rampe`
4. **Ports 80 & 443 offen** → Firewall

---

## 🚀 Quick Start (All-in-One)

```bash
# SSH zum Server
ssh reste-rampe

# Navigiere ins Projektverzeichnis
cd /home/newuser/Reste-Rampe

# Certbot Installation vorbereiten
sudo apt update
sudo apt install -y certbot python3-certbot-nginx

# Zertifikat anfragen
sudo certbot certonly --standalone \
  -d rest-rampe.tech \
  -d www.rest-rampe.tech \
  --email admin@rest-rampe.tech \
  --agree-tos \
  --non-interactive

# Zertifikat Lokation prüfen
ls -la /etc/letsencrypt/live/rest-rampe.tech/

# Nginx Config aktualisieren
sudo nano /etc/nginx/sites-available/rest-rampe.tech
# → Siehe: Nginx Configuration (unten)

# Nginx neu laden
sudo nginx -t
sudo systemctl reload nginx

# Zertifikat Test
curl -I https://rest-rampe.tech

# Auto-Renewal aktivieren
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer

# Auto-Renewal Status prüfen
sudo systemctl status certbot.timer
```

---

## 🌐 DNS Configuration

Setze diese Records in deinem Domain-Provider:

### Für rest-rampe.tech (Domain Root)

```dns
Type: A
Name: @ (oder leer)
Value: 84.46.241.104
TTL: 3600
```

### Für www.rest-rampe.tech (Subdomain)

```dns
Type: CNAME
Name: www
Value: rest-rampe.tech
TTL: 3600
```

### Optional: Mail Exchange (MX)

```dns
Type: MX
Name: @ (oder leer)
Priority: 10
Value: mailcow.rest-rampe.tech
TTL: 3600
```

### Verify DNS

```bash
# Prüfe A Record
dig rest-rampe.tech

# Output sollte sein:
# rest-rampe.tech. 3600 IN A 84.46.241.104

# Prüfe www
dig www.rest-rampe.tech

# Output sollte sein:
# www.rest-rampe.tech. 3600 IN CNAME rest-rampe.tech
```

---

## 📝 Nginx Configuration

### Neue Datei erstellen

```bash
sudo nano /etc/nginx/sites-available/rest-rampe.tech
```

### Content (Copy-Paste)

```nginx
# HTTP → HTTPS Redirect
server {
    listen 80;
    listen [::]:80;
    server_name rest-rampe.tech www.rest-rampe.tech;

    # Allow Certbot challenge
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    # Redirect all HTTP to HTTPS
    location / {
        return 301 https://$server_name$request_uri;
    }
}

# HTTPS Server
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name rest-rampe.tech www.rest-rampe.tech;

    # SSL Certificates from Let's Encrypt
    ssl_certificate /etc/letsencrypt/live/rest-rampe.tech/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/rest-rampe.tech/privkey.pem;

    # SSL Configuration (Mozilla Recommended)
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;

    # Frontend (Vue3 - Port 3000)
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # API Proxy (FastAPI - Port 8000)
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Remove the /api prefix before sending to backend
        rewrite ^/api/(.*) /$1 break;
    }

    # Error Pages
    error_page 404 /index.html;
}
```

### Enable Site

```bash
sudo ln -s /etc/nginx/sites-available/rest-rampe.tech \
  /etc/nginx/sites-enabled/rest-rampe.tech

# Remove default site
sudo rm /etc/nginx/sites-enabled/default 2>/dev/null || true

# Test Config
sudo nginx -t

# Reload Nginx
sudo systemctl reload nginx
```

---

## 🔐 SSL Verification

### Certificate Check

```bash
# Zeige Zertifikat Details
sudo openssl x509 -in /etc/letsencrypt/live/rest-rampe.tech/fullchain.pem -text -noout

# Prüfe Expiration
sudo certbot certificates

# Output:
# Certificate Name: rest-rampe.tech
# Domains: rest-rampe.tech, www.rest-rampe.tech
# Expiry Date: 2026-02-04 (90 Tage gültig)
# Valid: True
```

### Online SSL Test

```bash
# Terminal Test
curl -I https://rest-rampe.tech

# Expected:
# HTTP/2 200
# strict-transport-security: max-age=31536000

# Online Tool (Browser)
https://www.ssllabs.com/ssltest/analyze.html?d=rest-rampe.tech
```

---

## 🔄 Auto-Renewal Setup

### Systemd Timer (Automatic)

```bash
# Prüfe Status
sudo systemctl status certbot.timer

# Enable Auto-Renewal
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer

# Manual Renewal Test
sudo certbot renew --dry-run

# Expected: "congratulations, all renewals succeeded"
```

### Renewal Logs

```bash
# View renewal logs
sudo journalctl -u certbot.timer -n 50

# View all certbot activity
sudo journalctl -u certbot -n 50
```

---

## 🐳 Docker Integration (Optional)

Falls du Certbot in Docker ausführen möchtest:

### docker-compose.yml Erweiterung

```yaml
certbot:
  image: certbot/certbot
  container_name: reste-rampe-certbot
  volumes:
    - ./certs:/etc/letsencrypt
    - ./certbot-data:/var/www/certbot
  entrypoint: "/bin/sh -c 'trap exit TERM; while :; do certbot renew --webroot -w /var/www/certbot; sleep 12h & wait $${!}; done'"
  depends_on:
    - frontend
  networks:
    - reste-rampe-network
```

---

## 🚨 Troubleshooting

### Problem: "Connection refused" auf Port 443

**Lösung:**
```bash
# Prüfe ob Nginx läuft
sudo systemctl status nginx

# Starte Nginx
sudo systemctl start nginx

# Prüfe Ports
sudo netstat -tlnp | grep :443
sudo netstat -tlnp | grep :80
```

### Problem: Certbot sagt "Port 80 already in use"

**Lösung:**
```bash
# Stoppe Nginx temporär
sudo systemctl stop nginx

# Führe Certbot aus
sudo certbot certonly --standalone -d rest-rampe.tech

# Starte Nginx wieder
sudo systemctl start nginx
```

### Problem: Certificate Renewal fehlgeschlagen

**Lösung:**
```bash
# Manual Renewal mit Verbose Output
sudo certbot renew -v

# Force Renewal (nicht empfohlen)
sudo certbot renew --force-renewal

# Check Logs
sudo tail -50 /var/log/letsencrypt/letsencrypt.log
```

### Problem: Mixed Content Warning

**Lösung:**
- Prüfe dass alle URLs in Frontend zu HTTPS konvertiert werden
- Überprüfe API_URL in .env: `https://rest-rampe.tech/api`
- Nginx Headers sollten `X-Forwarded-Proto: https` setzen

---

## ✅ Verification Checklist

Nach dem Setup durchlaufen:

- [ ] DNS `A` Record erstellt: `rest-rampe.tech → 84.46.241.104`
- [ ] DNS `CNAME` Record erstellt: `www → rest-rampe.tech`
- [ ] Certbot installiert: `which certbot`
- [ ] Zertifikat beantragt: `ls /etc/letsencrypt/live/rest-rampe.tech/`
- [ ] Nginx Config aktualisiert
- [ ] Nginx Test erfolgreich: `sudo nginx -t`
- [ ] Nginx reloaded: `sudo systemctl reload nginx`
- [ ] HTTP zu HTTPS Redirect funktioniert: `curl -I http://rest-rampe.tech`
- [ ] HTTPS funktioniert: `curl -I https://rest-rampe.tech`
- [ ] SSL-Grade A+ auf SSLLabs
- [ ] Auto-Renewal aktiv: `sudo systemctl status certbot.timer`
- [ ] Browser zeigt kein Security-Warning

---

## 📊 Quick Reference

| Befehl | Beschreibung |
|--------|-------------|
| `sudo certbot certificates` | Liste alle Zertifikate |
| `sudo certbot renew --dry-run` | Teste Renewal ohne Änderung |
| `sudo certbot delete` | Lösche Zertifikat |
| `sudo systemctl restart nginx` | Nginx neustarten |
| `sudo systemctl status certbot.timer` | Timer Status |

---

## 🔗 Weiterführende Links

- **Let's Encrypt Docs:** https://letsencrypt.org/docs/
- **Certbot Docs:** https://certbot.eff.org/docs/using.html
- **Nginx SSL:** https://nginx.org/en/docs/http/ngx_http_ssl_module.html
- **SSL Labs:** https://www.ssllabs.com/

---

**Status:** 🟢 Ready to Deploy  
**Last Updated:** November 5, 2025
