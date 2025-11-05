# 🚀 Complete SSL/TLS & Custom Domain Setup Guide

> Step-by-step Instructions für Production Deployment

---

## 📋 Overview

Diese Anleitung führt dich durch:

1. ✅ **DNS Configuration** - Domain zu Server
2. ✅ **SSL/TLS Setup** - Let's Encrypt Zertifikat
3. ✅ **Nginx Configuration** - HTTPS aktivieren
4. ✅ **Auto-Renewal** - Automatische Zertifikat-Erneuerung
5. ✅ **Verification** - Alles funktioniert

**Benötigte Zeit:** ~20 Minuten (plus DNS Propagation)  
**Kosten:** €0 (Let's Encrypt ist kostenlos!)

---

## 🌐 Schritt 1: DNS Setup (5 Minuten)

### Was ist DNS?
DNS (Domain Name System) übersetzt deine Domain (rest-rampe.tech) zu deiner Server-IP (84.46.241.104).

### Records die du hinzufügen musst:

#### 1.1️⃣ A Record (für root domain)

```
Name/Host:   @ (oder leer)
Type:        A
Value:       84.46.241.104
TTL:         3600 (oder so kurz wie möglich)
```

#### 2️⃣ CNAME Record (für www subdomain) - Optional

```
Name/Host:   www
Type:        CNAME
Value:       rest-rampe.tech
TTL:         3600
```

### Wie man DNS Records hinzufügt:

#### Option A: Namecheap (am populärsten)

```
1. Gehe zu https://www.namecheap.com
2. Log in zu deinem Account
3. Gehe zu "Manage Domains"
4. Klicke auf deine Domain (rest-rampe.tech)
5. Klicke auf "Manage DNS"
6. Scrolle zu "DNS Records"
7. Bearbeite/Füge hinzu:
   - Type: A, Name: @, Value: 84.46.241.104, TTL: 3600
   - Type: CNAME, Name: www, Value: rest-rampe.tech, TTL: 3600
8. Speichern
```

#### Option B: GoDaddy

```
1. Gehe zu https://www.godaddy.com
2. Log in zu deinem Account
3. Wähle deine Domain
4. Gehe zu "Manage DNS"
5. Bearbeite/Füge die A und CNAME Records wie oben hinzu
6. Speichern
```

#### Option C: Cloudflare (Kostenlos + Faster!)

```
1. Gehe zu https://www.cloudflare.com
2. Registriere kostenlos
3. Füge deine Domain hinzu
4. Cloudflare zeigt dir die neuen Nameserver
5. Gehe zu deinem Domain-Registrar (z.B. Namecheap)
6. Ändere die Nameserver auf Cloudflares Nameserver
7. In Cloudflare: Füge DNS Records hinzu
   - Type: A, Name: @, Content: 84.46.241.104
   - Type: CNAME, Name: www, Content: rest-rampe.tech
8. Fertig!
```

### DNS Verifikation

Nach dem Setup warten auf Propagation (normalerweise 5 Minuten, max 48 Stunden):

```bash
# Auf lokalem Computer oder Server testen

# Option 1: dig verwenden
dig rest-rampe.tech

# Output sollte zeigen:
# rest-rampe.tech. 3600 IN A 84.46.241.104

# Option 2: nslookup verwenden
nslookup rest-rampe.tech

# Option 3: Online-Tool
# https://mxtoolbox.com/ → DNS Lookup → rest-rampe.tech
```

---

## 🔒 Schritt 2: SSL/TLS Setup mit Let's Encrypt (10 Minuten)

### Automatisches Setup (Empfohlen!)

```bash
# SSH zum Server
ssh reste-rampe

# Navigiere zum Projektverzeichnis
cd /home/newuser/Reste-Rampe

# Führe das SSL Setup Script aus (mit sudo)
sudo bash ssl_setup.sh

# Das Script wird:
# ✅ Certbot installieren
# ✅ Zertifikat anfordern
# ✅ Nginx konfigurieren
# ✅ Auto-Renewal einrichten
# ✅ Alles testen
```

### Manuelles Setup (für Fortgeschrittene)

Falls du es lieber manuell machen möchtest:

```bash
# SSH zum Server
ssh reste-rampe

# Update System
sudo apt update
sudo apt install -y certbot python3-certbot-nginx

# Certbot ausführen (Nginx muss laufen!)
sudo certbot certonly --standalone \
  -d rest-rampe.tech \
  -d www.rest-rampe.tech \
  --email admin@rest-rampe.tech \
  --agree-tos \
  --non-interactive

# Zertifikat verifizieren
ls -la /etc/letsencrypt/live/rest-rampe.tech/

# Nginx neu konfigurieren
sudo nano /etc/nginx/sites-available/rest-rampe.tech
# → Siehe: SSL_SETUP.md für Nginx Config

# Nginx testen und aktivieren
sudo nginx -t
sudo systemctl reload nginx

# Auto-Renewal aktivieren
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer
```

---

## ✅ Schritt 3: Verifikation (2 Minuten)

### Verifikation durchführen

```bash
# SSH zum Server
ssh reste-rampe

# 1. Certbot Status prüfen
sudo certbot certificates

# Expected Output:
# Certificate Name: rest-rampe.tech
# Domains: rest-rampe.tech, www.rest-rampe.tech
# Valid: True
```

### HTTPS Test

```bash
# Von deinem lokalen Computer

# Test 1: HTTP Redirect zu HTTPS
curl -I http://rest-rampe.tech
# Sollte: HTTP/1.1 301 Moved Permanently
# Location: https://rest-rampe.tech

# Test 2: HTTPS Connection
curl -I https://rest-rampe.tech
# Sollte: HTTP/2 200 (oder HTTP/1.1 200)

# Test 3: In Browser öffnen
# https://rest-rampe.tech
# → Sollte 🔒 Padlock zeigen (sicher)
```

### SSL Grade prüfen

Gehe zu: https://www.ssllabs.com/ssltest/analyze.html?d=rest-rampe.tech

Sollte eine **A oder A+** sein! 🎯

---

## 🔄 Schritt 4: Auto-Renewal Verification

### Status prüfen

```bash
ssh reste-rampe

# Certbot Timer Status
sudo systemctl status certbot.timer

# Expected:
# ● certbot.timer - Run certbot twice daily
# Loaded: loaded (...; enabled; ...)
# Active: active (waiting)

# Renewal Test durchführen
sudo certbot renew --dry-run

# Expected:
# (...) Congratulations, all renewals succeeded
```

### Renewal Logs anschauen

```bash
# Letzte 50 Zeilen
sudo journalctl -u certbot.timer -n 50

# Follow mode (live updates)
sudo journalctl -u certbot.timer -f
```

---

## 🎯 Complete Verification Checklist

Nach allem Setup diese Checkpoints durchgehen:

### DNS
- [ ] A Record eingestellt: rest-rampe.tech → 84.46.241.104
- [ ] CNAME Record eingestellt: www → rest-rampe.tech
- [ ] DNS propagiert: `dig rest-rampe.tech` zeigt korrekte IP
- [ ] Port 80 öffnet: `curl -I http://rest-rampe.tech`
- [ ] Port 443 öffnet: `curl -I https://rest-rampe.tech`

### SSL Certificate
- [ ] Zertifikat vorhanden: `ls /etc/letsencrypt/live/rest-rampe.tech/`
- [ ] Zertifikat gültig: `sudo certbot certificates` zeigt "Valid: True"
- [ ] Zertifikat läuft nicht bald ab: Expiry Date > 30 Tage
- [ ] Browser zeigt 🔒 Padlock (kein Fehler)

### Nginx
- [ ] HTTP → HTTPS Redirect funktioniert
- [ ] HTTPS Connection erfolgreich
- [ ] Security Headers vorhanden: `curl -I https://rest-rampe.tech`
- [ ] API erreichbar: `curl https://rest-rampe.tech/api/health`
- [ ] Frontend lädt: Browser zeigt keine Fehler

### Auto-Renewal
- [ ] Certbot Timer aktiv: `systemctl status certbot.timer`
- [ ] Renewal Test erfolgreich: `certbot renew --dry-run` says "succeeded"

### Browser Test (Desktop)
- [ ] Browser: Gehe zu https://rest-rampe.tech
- [ ] Sollte: ✅ Keine Warnungen, 🔒 Padlock sichtbar
- [ ] Login-Seite: Sollte laden
- [ ] API Docs: Gehe zu https://rest-rampe.tech/api/docs
- [ ] Sollte: Swagger UI laden mit allen Endpoints

---

## 🔧 Troubleshooting

### Problem: "Connection refused" auf Port 443

**Lösung:**

```bash
ssh reste-rampe

# Prüfe ob Nginx läuft
sudo systemctl status nginx

# Falls nicht:
sudo systemctl start nginx

# Prüfe Ports
sudo netstat -tlnp | grep ":443"

# Falls Port in Benutzung:
sudo netstat -tlnp | grep LISTEN
```

### Problem: "Zertifikat nicht gefunden"

**Lösung:**

```bash
# Prüfe Zertifikat Location
sudo ls -la /etc/letsencrypt/live/rest-rampe.tech/

# Falls leer, Certbot re-run:
sudo certbot certonly --standalone \
  -d rest-rampe.tech \
  -d www.rest-rampe.tech
```

### Problem: "Mixed Content Warning"

**Ursache:** Frontend-Ressourcen von HTTP nicht HTTPS  
**Lösung:** Prüfe .env → VITE_API_URL sollte `https://` sein

```bash
cat /home/newuser/Reste-Rampe/.env | grep VITE_API_URL
# Sollte zeigen: VITE_API_URL=https://rest-rampe.tech/api
```

### Problem: DNS propagiert nicht

**Warten:** Bis zu 48 Stunden (normalerweise 5 Minuten)

```bash
# Immer wieder prüfen
watch -n 5 "dig rest-rampe.tech +short"

# Oder Online-Tool verwenden:
# https://dnschecker.org/ → rest-rampe.tech

# Von Cloudflare nameserver direkt prüfen:
dig rest-rampe.tech @1.1.1.1
dig rest-rampe.tech @8.8.8.8
```

---

## 🎉 Success Indicators

Nach erfolgreichem Setup solltest du sehen:

```bash
✅ HTTPS funktionstüchtig
✅ Browser zeigt 🔒 Padlock
✅ SSL Lab Grade A oder A+
✅ HTTP auto-redirect zu HTTPS
✅ API erreichbar unter https://rest-rampe.tech/api
✅ Frontend lädt alle Ressourcen über HTTPS
✅ Certbot Timer läuft
✅ Zertifikat automatische Erneuerung aktiv
```

---

## 📚 Helper Scripts auf dem Server

Du hast jetzt auf dem Server:

| Script | Zweck |
|--------|-------|
| `ssl_setup.sh` | Automatisiertes SSL Setup |
| `dns_helper.sh` | DNS Konfiguration und Verifikation |
| `health_check.sh` | System Health Monitoring |
| `SSL_SETUP.md` | Detaillierte SSL Dokumentation |

### Scripts ausführen

```bash
ssh reste-rampe
cd /home/newuser/Reste-Rampe

# DNS Helper (interaktiv)
bash dns_helper.sh

# SSL Setup (automatisiert)
sudo bash ssl_setup.sh

# Health Check
bash health_check.sh
```

---

## 🔑 Quick Reference Commands

```bash
# SSH zum Server
ssh reste-rampe

# Zertifikat Status
sudo certbot certificates

# Renewal Test
sudo certbot renew --dry-run

# HTTPS Test
curl -I https://rest-rampe.tech

# DNS Test
dig rest-rampe.tech

# Nginx Logs
sudo tail -50 /var/log/nginx/error.log

# Certbot Logs
sudo tail -50 /var/log/letsencrypt/letsencrypt.log

# Nginx neustarten
sudo systemctl restart nginx

# Timer Status
sudo systemctl status certbot.timer
```

---

## 📞 Support

**Probleme?** Überprüfe in dieser Reihenfolge:

1. **DNS nicht propagiert?** 
   - Warte 5-48 Stunden
   - Test: `dig rest-rampe.tech @8.8.8.8`

2. **Certbot Fehler?**
   - Logs: `sudo tail -50 /var/log/letsencrypt/letsencrypt.log`
   - Manual: `sudo certbot certonly --standalone -d rest-rampe.tech`

3. **Nginx Fehler?**
   - Logs: `sudo tail -50 /var/log/nginx/error.log`
   - Test: `sudo nginx -t`

4. **HTTPS funktioniert aber Browser-Fehler?**
   - Browserkasche: Ctrl+Shift+Delete
   - Prüfe Mixed Content: Browser F12 → Console
   - Check: .env → VITE_API_URL muss `https://` sein

---

**Status:** ✅ Ready to Deploy  
**Last Updated:** November 5, 2025  
**Next Step:** Nach DNS Setup + SSL → Mailcow API Key konfigurieren!
