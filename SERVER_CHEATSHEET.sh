#!/bin/bash
# 🔧 Reste-Rampe Server Management Cheat Sheet

# ==================== QUICK SSH ====================
# Verbindung zum Server (kein Passwort nötig!)
ssh reste-rampe

# ==================== DOCKER COMMANDS ====================
cd /home/newuser/Reste-Rampe

# Status aller Container
docker-compose ps

# Logs anschauen
docker-compose logs -f backend    # Backend in Echtzeit
docker-compose logs -f frontend   # Frontend in Echtzeit
docker-compose logs -f db         # Database in Echtzeit
docker-compose logs backend | tail -100  # Letzte 100 Zeilen Backend

# Container neustarten
docker-compose restart backend
docker-compose restart frontend
docker-compose restart db
docker-compose restart              # Alle neustarten

# Container stoppen
docker-compose down

# Container starten
docker-compose up -d

# Neu bauen und starten
docker-compose up -d --build

# ==================== DATABASE COMMANDS ====================

# In die Datenbank einsteigen
docker-compose exec db psql -U reste -d reste-rampe-db

# SQL Befehl ausführen
docker-compose exec db psql -U reste -d reste-rampe-db -c "SELECT * FROM users;"

# Alle Benutzer anschauen
docker-compose exec db psql -U reste -d reste-rampe-db -c "SELECT id, username, email, is_admin FROM users;"

# Benutzer löschen
docker-compose exec db psql -U reste -d reste-rampe-db -c "DELETE FROM users WHERE username = 'testuser';"

# Tabelle Struktur anschauen
docker-compose exec db psql -U reste -d reste-rampe-db -c "\\d users"

# Backup erstellen
docker-compose exec db pg_dump -U reste reste-rampe-db > backup_$(date +%Y%m%d_%H%M%S).sql

# Backup einspielen
docker-compose exec db psql -U reste reste-rampe-db < backup.sql

# ==================== BACKEND COMMANDS ====================

# In Backend Container einsteigen
docker-compose exec backend bash

# Python Shell im Container
docker-compose exec backend python

# Abhängigkeiten installieren (neu)
docker-compose exec backend pip install -r requirements.txt

# ==================== GIT COMMANDS ====================

# Neuesten Code vom Remote holen
git pull origin main

# Alle Änderungen anschauen
git status

# Änderungen committen
git add -A
git commit -m "description"
git push origin main

# Force Update (wenn lokale Änderungen überschrieben werden sollen)
git fetch origin
git reset --hard origin/main

# ==================== NGINX / FRONTEND ====================

# Nginx Config überprüfen
docker-compose exec frontend nginx -t

# Nginx neu laden
docker-compose exec frontend nginx -s reload

# Nginx Logs
docker-compose logs -f frontend | grep error

# ==================== MONITORING ====================

# CPU / Memory Auslastung
docker stats

# Container Events
docker events --filter type=container

# Disk Usage
df -h

# ==================== HÄUFIGE PROBLEME ====================

# Backend zeigt Fehler
docker-compose logs backend | tail -50

# Frontend lädt nicht
# 1. Prüfen ob Nginx läuft: docker-compose ps
# 2. Prüfen ob Port 80/443 frei ist: sudo netstat -tlnp | grep :80
# 3. Logs checken: docker-compose logs frontend

# Datenbank Connection Problem
docker-compose logs backend | grep "connection"
docker-compose exec db pg_isready -U reste

# ==================== MAINTENANCE ====================

# Cache löschen
docker system prune -f

# Ungenutzte Images löschen
docker image prune -f

# Ungenutzte Volumes löschen
docker volume prune -f

# Alles löschen (VORSICHT!)
docker system prune -af

# ==================== API TESTS ====================

# API Health Check
curl http://84.46.241.104:8000/api/health

# Benutzer registrieren
curl -X POST http://84.46.241.104:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"password123"}'

# Login
curl -X POST http://84.46.241.104:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"password123"}'

# ==================== WICHTIGE DATEIEN ====================

# Environment Variablen
/home/newuser/Reste-Rampe/.env

# Docker Compose Konfiguration
/home/newuser/Reste-Rampe/docker-compose.yml

# Backend Source
/home/newuser/Reste-Rampe/backend/app/

# Frontend Source
/home/newuser/Reste-Rampe/frontend/src/

# Database
/home/newuser/Reste-Rampe/backend/alembic/ (Migrations)

# ==================== SCHNELLE LINKS ====================

# Frontend: http://84.46.241.104
# API Docs: http://84.46.241.104:8000/docs
# Database Admin: docker-compose exec db psql
# Mailcow: https://mailcow.reste-rampe.tech (separate installation)
