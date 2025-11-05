# 🔧 Mailcow REST API Setup Anleitung

## Schritt 1: Mailcow Admin Panel öffnen

Öffne in deinem Browser:
```
https://mailcow.reste-rampe.tech/admin
```

Oder deine Mailcow Installation URL.

## Schritt 2: API Key finden/generieren

1. Melde dich im Admin Panel an
2. Gehe zu: **System > API**
3. Du siehst einen bestehenden API Key oder kannst einen neuen generieren
4. Der Key sieht etwa so aus: `abcd1234efgh5678ijkl9012mnop3456`

## Schritt 3: API Key in .env eintragen

Öffne die `.env` Datei auf dem Server:

```bash
ssh reste-rampe
nano /home/newuser/Reste-Rampe/.env
```

Finde diese Zeilen und trage deinen Key ein:

```bash
MAILCOW_API_URL=https://mailcow.reste-rampe.tech/api/v1
MAILCOW_API_KEY=DEIN_API_KEY_HIER
MAILCOW_DOMAIN=reste-rampe.tech
MAILCOW_VERIFY_SSL=true
```

## Schritt 4: Backend neu starten

```bash
cd /home/newuser/Reste-Rampe
docker-compose restart backend
```

## Schritt 5: Testen

Versuche im Frontend: Mailbox erstellen

Die Mailbox sollte dann automatisch in Mailcow erstellt werden! ✅

---

## 🔑 Dein API Key:

Kopiere hier deinen Key rein:

```
MAILCOW_API_KEY = ______________________________________
```

Dann speichern und Backend neu starten!
