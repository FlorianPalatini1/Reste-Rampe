# Mailcow REST API Integration - Setup & Configuration

## 📋 Überblick

Die Mailcow REST API Integration ermöglicht es eurem Reste-Rampe Backend, Mailboxen zu erstellen, zu löschen und zu verwalten.

**Was wurde integriert:**
- ✅ Mailcow REST API Client (`backend/app/mailcow_api.py`)
- ✅ User Mailbox Management Endpoints (`backend/app/routers/mailbox.py`)
- ✅ Admin Mailbox Management Endpoints (`backend/app/routers/admin_mailbox.py`)
- ✅ Database Schema Extensions
- ✅ Test Script (`test_mailcow_api.py`)

---

## 🔧 Schritt 1: Mailcow API Key erhalten

1. **Öffne Mailcow Admin Panel:**
   - Gehe zu `https://mailcow.example.com/admin`

2. **Navigiere zu System > API:**
   - Klicke auf "Manage API" oder "API"
   - Erstelle einen neuen API Key oder kopiere den bestehenden
   - Der Key sieht so aus: `abcd1234efgh5678ijkl9012mnop3456`

3. **Notiere dir:**
   - API URL: `https://mailcow.example.com/api/v1`
   - API Key: `your_api_key_here`
   - Domain: `reste-rampe.tech`

---

## 📝 Schritt 2: Environment Variablen setzen

### In `backend/.env` (oder docker-compose.yml):

```bash
# ============ MAILCOW REST API CONFIGURATION ============
# Mailcow API URL (mit /api/v1 suffix)
MAILCOW_API_URL=https://mailcow.example.com/api/v1
# Mailcow Admin API Key
MAILCOW_API_KEY=your_api_key_here
# Domain für Mailboxen
MAILCOW_DOMAIN=reste-rampe.tech
# SSL Zertifikate verifizieren (false für self-signed in dev)
MAILCOW_VERIFY_SSL=false
```

### In `docker-compose.yml` Backend Service:

```yaml
backend:
  environment:
    - MAILCOW_API_URL=https://mailcow:443/api/v1
    - MAILCOW_API_KEY=your_api_key_here
    - MAILCOW_DOMAIN=reste-rampe.tech
    - MAILCOW_VERIFY_SSL=false
```

**Wichtig:** 
- Nutze den internen Mailcow Container-Namen wenn beide im selben Docker Network sind
- In Production: `MAILCOW_VERIFY_SSL=true` setzen

---

## 🧪 Schritt 3: Testen der Integration

### Test Script ausführen:

```bash
# Im Projekt-Root:
cd /home/newuser/Reste-Rampe

# Stelle sicher, dass Environment Variablen gesetzt sind
export MAILCOW_API_URL=https://mailcow.example.com/api/v1
export MAILCOW_API_KEY=your_api_key_here
export MAILCOW_DOMAIN=reste-rampe.tech
export MAILCOW_VERIFY_SSL=false

# Führe Test aus
python3 test_mailcow_api.py
```

**Erwartete Ausgabe:**
```
============================================================
  1. Testing Mailcow API Connection
============================================================
API URL: https://mailcow.example.com/api/v1
Domain: reste-rampe.tech
API Key: ****...3456
✅ Connection successful!

============================================================
  2. Testing Mailbox Operations
============================================================
Creating test mailbox: testuser123@reste-rampe.tech
✅ Mailbox created successfully
...
🎉 All tests passed! Mailcow API integration is working correctly.
```

---

## 🚀 API Endpoints Übersicht

### User Endpoints (Authentifiziert)

```
GET    /api/mailbox                    - Mailbox Status abrufen
POST   /api/mailbox                    - Mailbox erstellen
DELETE /api/mailbox                    - Mailbox löschen
GET    /api/mailbox/quota              - Quota & Speicher
POST   /api/mailbox/password           - Passwort ändern
GET    /api/mailbox/forwarding         - Weiterleitungen auflisten
POST   /api/mailbox/forwarding         - Weiterleitung hinzufügen
DELETE /api/mailbox/forwarding/{dest}  - Weiterleitung entfernen
```

### Admin Endpoints (Admin-Only)

```
GET    /api/admin/mailboxes            - Alle Mailboxen auflisten
GET    /api/admin/mailboxes/stats      - Statistiken
GET    /api/admin/mailboxes/{user}     - Mailbox Details
POST   /api/admin/mailboxes/{user}/disable  - Deaktivieren
POST   /api/admin/mailboxes/{user}/enable   - Aktivieren
POST   /api/admin/mailboxes/{user}/quota    - Quota setzen
DELETE /api/admin/mailboxes/{user}          - Löschen
```

---

## 📚 Beispiele

### 1. Mailbox erstellen (User)

```bash
curl -X POST http://localhost:8000/api/mailbox \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "password": "SecurePassword123!"
  }'
```

**Response:**
```json
{
  "message": "Mailbox created successfully",
  "email": "username@reste-rampe.tech"
}
```

### 2. Mailbox Status (User)

```bash
curl -X GET http://localhost:8000/api/mailbox \
  -H "Authorization: Bearer <token>"
```

**Response:**
```json
{
  "enabled": true,
  "username": "username",
  "email": "username@reste-rampe.tech",
  "quota_mb": 5120,
  "quota_percent": 45,
  "active": true,
  "created_at": "2025-11-05T10:30:00"
}
```

### 3. Quota abrufen (User)

```bash
curl -X GET http://localhost:8000/api/mailbox/quota \
  -H "Authorization: Bearer <token>"
```

**Response:**
```json
{
  "quota_total_mb": 5120,
  "quota_used_mb": 2304,
  "quota_percent": 45
}
```

### 4. Weiterleitung hinzufügen (User)

```bash
curl -X POST http://localhost:8000/api/mailbox/forwarding \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "destination": "personal@gmail.com",
    "keep_local_copy": true
  }'
```

### 5. Alle Mailboxen (Admin)

```bash
curl -X GET http://localhost:8000/api/admin/mailboxes \
  -H "Authorization: Bearer <admin_token>"
```

### 6. Mailbox deaktivieren (Admin)

```bash
curl -X POST http://localhost:8000/api/admin/mailboxes/username/disable \
  -H "Authorization: Bearer <admin_token>"
```

---

## 🔐 Sicherheitshinweise

1. **API Key schützen:**
   - Niemals in Git committen
   - In Production in Environment Variable halten
   - Regelmäßig rotieren

2. **CORS & SSL:**
   - Nur über HTTPS in Production
   - CORS ist im Backend konfiguriert

3. **Rate Limiting:**
   - Mailcow API hat möglicherweise Rate Limits
   - Implementiert Retry Logic wenn nötig

4. **Fehlerbehandlung:**
   - Alle Endpoints haben Try-Catch
   - Errormessages werden ins Log geschrieben

---

## 🐛 Troubleshooting

### ❌ "Mailcow API: Invalid API key"
- API Key in Environment Variablen überprüfen
- Key in Mailcow Admin Panel bestätigen
- Backend Container neu starten

### ❌ "Mailcow API connection error: Connection refused"
- Mailcow URL überprüfen
- DNS/Connectivity zum Mailcow Server testen
- Firewall Rules checken
- SSL Certificate validieren (wenn MAILCOW_VERIFY_SSL=true)

### ❌ "Failed to create mailbox"
- Mailbox-Username prüfen (muss eindeutig sein)
- Passwort-Anforderungen überprüfen
- Mailcow API Logs ansehen

### ✅ "Failed to retrieve quota information"
- Mailbox existiert möglicherweise nicht
- Status endpoint aufrufen um zu checken ob Mailbox enabled ist

---

## 📦 Nächste Schritte

1. **Frontend Component:**
   - Erstelle `frontend/src/views/MailboxManagement.vue`
   - Zeige Mailbox Status, Quota, Weiterleitungen
   - Ermögliche Mailbox Erstellung/Löschung

2. **Integration mit Registration:**
   - Nach Email-Verifikation: Mailbox automatisch erstellen?
   - Oder Optional bei User-Entscheidung?

3. **Admin Dashboard:**
   - Mailbox Management Interface
   - User Quota Limits setzen
   - Monitoring von Mailbox-Nutzung

---

## 📖 Struktur der Code-Dateien

```
backend/
├── app/
│   ├── mailcow_api.py          ← Mailcow REST API Client
│   ├── models.py               ← User Model mit Mailbox Fields
│   ├── routers/
│   │   ├── mailbox.py          ← User Mailbox Endpoints
│   │   ├── admin_mailbox.py    ← Admin Mailbox Endpoints
│   │   └── __init__.py
│   ├── main.py                 ← Router Registration
│   └── ...
├── alembic/versions/
│   └── add_mailbox_fields.py   ← Database Migration
└── ...
```

---

**Fragen?** 🤔 Lass mich wissen wenn etwas nicht funktioniert!
