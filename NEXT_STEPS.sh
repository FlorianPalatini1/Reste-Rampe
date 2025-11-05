#!/bin/bash

################################################################################
# Next Steps Quick Start
# Was macht man jetzt nach dem SSL/Domain Setup?
################################################################################

DOMAIN="rest-rampe.tech"
SERVER="84.46.241.104"

cat << 'EOF'

╔════════════════════════════════════════════════════════════════════════════╗
║                     🎉 NÄCHSTE SCHRITTE ZUM LAUNCH 🎉                     ║
╚════════════════════════════════════════════════════════════════════════════╝

Glückwunsch! Du hast die meisten Schritte erledigt. Hier ist was noch zu tun:

═════════════════════════════════════════════════════════════════════════════

📋 SCHRITT 1: DNS & SSL Setup (Du bist hier!)
   
   Status: ⏳ TODO - Folge diesem Guide:
   ├─ 1. DNS Records hinzufügen (Namecheap/GoDaddy/Cloudflare)
   │  └─ A Record: @ → 84.46.241.104
   │  └─ CNAME Record: www → rest-rampe.tech
   │
   ├─ 2. DNS Propagation warten (5 Minuten - 48 Stunden)
   │  └─ Test: dig rest-rampe.tech @8.8.8.8
   │
   ├─ 3. SSL Setup automatisieren
   │  └─ ssh reste-rampe
   │  └─ cd /home/newuser/Reste-Rampe
   │  └─ sudo bash ssl_setup.sh
   │
   └─ 4. Verifizieren
      └─ curl -I https://rest-rampe.tech
      └─ https://www.ssllabs.com/ssltest/?d=rest-rampe.tech

   📖 Detaillierte Anleitung:
   └─ Lies: SSL_DOMAIN_COMPLETE_GUIDE.md

═════════════════════════════════════════════════════════════════════════════

🔑 SCHRITT 2: Mailcow API Key Konfigurieren
   
   Status: ⏳ TODO
   
   Schritte:
   ├─ 1. Öffne Mailcow Admin Panel
   │  └─ https://mailcow.rest-rampe.tech
   │
   ├─ 2. Navigiere zu: System → API
   │
   ├─ 3. Kopiere deinen API Key
   │
   ├─ 4. SSH zum Server
   │  └─ ssh reste-rampe
   │
   ├─ 5. Bearbeite .env
   │  └─ cd /home/newuser/Reste-Rampe
   │  └─ nano .env
   │  └─ Finde: MAILCOW_API_KEY=your_api_key_here
   │  └─ Ersetze mit deinem Key
   │  └─ Speichern: Ctrl+O → Enter → Ctrl+X
   │
   ├─ 6. Container neustarten
   │  └─ docker-compose restart backend
   │  └─ sleep 5
   │
   └─ 7. Testen
      └─ curl https://rest-rampe.tech/api/mailbox
      └─ Sollte funktionieren!

   📖 Detaillierte Anleitung:
   └─ Lies: MAILCOW_API_KEY_SETUP.md

═════════════════════════════════════════════════════════════════════════════

🧪 SCHRITT 3: End-to-End Testing
   
   Status: ⏳ TODO
   
   Test-Flows:
   
   ├─ Test 1: User Registration
   │  ├─ Browser: https://rest-rampe.tech
   │  ├─ Klicke: "Register"
   │  ├─ Fülle aus: Username, Email, Password
   │  ├─ Warte auf Email
   │  └─ Klicke Verification Link
   │
   ├─ Test 2: Login
   │  ├─ Gebe Credentials ein
   │  └─ Sollte zum Dashboard gehen
   │
   ├─ Test 3: Mailbox erstellen
   │  ├─ Gehe zu: Mailbox Management
   │  ├─ Klicke: "Create Mailbox"
   │  ├─ Warte auf Success Message
   │  └─ Mailbox sollte aktiv sein
   │
   ├─ Test 4: Email Forwarding
   │  ├─ Klicke: "Add Forwarding"
   │  ├─ Gebe ein: forward@example.com
   │  └─ Sollte hinzugefügt werden
   │
   └─ Test 5: Mailbox löschen
      ├─ Klicke: "Delete Mailbox"
      ├─ Bestätige
      └─ Sollte gelöscht sein

═════════════════════════════════════════════════════════════════════════════

📊 SCHRITT 4: Health Check & Monitoring
   
   Status: ✅ READY
   
   Befehle:
   
   ssh reste-rampe
   cd /home/newuser/Reste-Rampe
   
   # Automatischer Health Check
   bash health_check.sh
   
   # Sollte zeigen:
   ├─ ✅ API Health: HTTP 200
   ├─ ✅ Database: Accepting connections
   ├─ ✅ Disk Space: < 80%
   ├─ ✅ Resource Usage: Normal
   └─ ✅ All Services: Up

═════════════════════════════════════════════════════════════════════════════

✅ SCHRITT 5: Production Readiness Check
   
   Status: 🔄 IN PROGRESS
   
   Durchlaufe diese Checkliste:
   └─ Öffne: PRODUCTION_READINESS_CHECKLIST.md
   └─ Markiere jedes Item als DONE
   └─ Wenn alles ✅: Launch Ready!

═════════════════════════════════════════════════════════════════════════════

🚀 LAUNCH! 🎉
   
   Wenn alles oben DONE:
   
   ├─ 🔐 SSL aktiv & Auto-Renewal läuft
   ├─ 🔑 Mailcow API konfiguriert
   ├─ 🧪 Tests erfolgreich
   ├─ 📊 Health Checks alle grün
   ├─ ✅ Readiness Checklist komplett
   └─ 🎉 LIVE gehen!

═════════════════════════════════════════════════════════════════════════════

📚 DOKUMENTATION

Wichtige Dateien auf dem Server:

├─ SSL_DOMAIN_COMPLETE_GUIDE.md      (📘 DNS + SSL Step-by-Step)
├─ SSL_SETUP.md                       (🔧 Detaillierte SSL Info)
├─ ssl_setup.sh                       (⚙️  Automatisierung)
├─ dns_helper.sh                      (🔍 DNS Verifikation)
├─ health_check.sh                    (🏥 System Monitoring)
├─ MAILCOW_API_KEY_SETUP.md          (🔑 Mailcow Config)
├─ README_PRODUCTION.md               (📖 Übersicht)
├─ PRODUCTION_READINESS_CHECKLIST.md (✅ Readiness Check)
├─ DEPLOYMENT_COMPLETE.md             (📊 Deployment Report)
└─ SERVER_CHEATSHEET.sh              (⚡ Quick Commands)

═════════════════════════════════════════════════════════════════════════════

⚡ QUICK COMMANDS

# SSH ohne Passwort
ssh reste-rampe

# Container Status
docker-compose ps

# Logs anschauen
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f db

# Health Check
bash health_check.sh

# SSL Status
sudo certbot certificates

# Database Backup
docker-compose exec db pg_dump -U reste reste-rampe-db > backup.sql

# Container Restart
docker-compose restart backend

═════════════════════════════════════════════════════════════════════════════

🎯 TIMELINE ESTIMATE

Wenn alles smooth läuft:

├─ DNS Setup:           5-10 Minuten
├─ DNS Propagation:     5 Minuten - 48 Stunden (meist 5 Min)
├─ SSL Setup:           5-10 Minuten
├─ Mailcow API Key:     5 Minuten
├─ End-to-End Testing:  10-15 Minuten
└─ LIVE:               🟢 Ready!

**Gesamtzeit:** ~30 Minuten (+ DNS Propagation)

═════════════════════════════════════════════════════════════════════════════

🆘 PROBLEME?

1. DNS nicht propagiert?
   → Warte 5-48 Stunden
   → Test: dig rest-rampe.tech @8.8.8.8

2. SSL Fehler?
   → Lese: SSL_DOMAIN_COMPLETE_GUIDE.md → Troubleshooting
   → Run: bash dns_helper.sh

3. Mailcow API nicht funktioniert?
   → Lies: MAILCOW_API_KEY_SETUP.md
   → Check: docker-compose logs backend

4. Sonst Problem?
   → Run: bash health_check.sh
   → Check: Server logs

═════════════════════════════════════════════════════════════════════════════

📞 SUPPORT

SSH zum Server und frag Fragen:

ssh reste-rampe
cd /home/newuser/Reste-Rampe
cat SSL_DOMAIN_COMPLETE_GUIDE.md  # Lese die Guides
bash dns_helper.sh                 # Interaktive Hilfe
bash health_check.sh               # System Status

═════════════════════════════════════════════════════════════════════════════

🎉 VIEL SPASS MIT DEINEM LAUNCH! 🎉

Status: 🟡 IN PROGRESS (SSL/DNS Setup)
Next: 🔑 Mailcow API Key
Then: 🧪 Testing
Finally: 🚀 LIVE

═════════════════════════════════════════════════════════════════════════════

EOF

echo ""
echo "💡 Tip: Diese Datei nochmal lesen nach jedem Step!"
echo ""
