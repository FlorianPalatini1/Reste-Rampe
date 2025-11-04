# 🏗️ Reste-Rampe Architecture & Network Structure

## System-Übersicht

```
┌─────────────────────────────────────────────────────────────────────┐
│                         EXTERNE INTERNET (HTTP/HTTPS)              │
└────────────────────────────────┬──────────────────────────────────┘
                                 │
                    Port 5173 (HTTP localhost)
                                 │
         ┌───────────────────────┴───────────────────────┐
         │                                               │
    ┌────▼─────────────────────────────────────────────┐
    │     DOCKER NETWORK: reste_net                    │
    │   ┌──────────────────────────────────────────┐   │
    │   │                                          │   │
    │   │  ┌─────────────────┐  ┌──────────────┐  │   │
    │   │  │   FRONTEND      │  │   BACKEND    │  │   │
    │   │  │  Container      │  │  Container   │  │   │
    │   │  │ (Nginx + Vue3)  │  │  (FastAPI)   │  │   │
    │   │  │  Port: 5173     │  │ Port: 8000   │  │   │
    │   │  └────────┬────────┘  └──────┬───────┘  │   │
    │   │           │                  │           │   │
    │   │      /api/ proxy     SQLAlchemy ORM     │   │
    │   │      /:/ files              │           │   │
    │   │           │                  │           │   │
    │   │           │          ┌───────▼───────┐  │   │
    │   │           │          │  DATABASE     │  │   │
    │   │           │          │ (PostgreSQL)  │  │   │
    │   │           │          │  Port: 5432   │  │   │
    │   │           │          └───────────────┘  │   │
    │   │           │                  │           │   │
    │   └───────────┼──────────────────┼───────────┘   │
    │               │                  │               │
    └───────────────┼──────────────────┼───────────────┘
                    │                  │
              External              External
              Services              Services
              (Gemini AI)           (optional)
```

---

## 📦 Container-Details

### **Frontend Container (Nginx + Vue3)**
```
Technologien:
├── Vue 3 + Vite (Build Tool)
├── Tailwind CSS (Styling)
├── vue-i18n (7 Sprachen)
├── vue-router (Routing)
├── Axios (HTTP Client)
└── DOMPurify + Marked (Content Rendering)

Port: 5173
Nginx Config:
├── Static Files: /usr/share/nginx/html/
├── API Proxy: /api/ → http://backend:8000/api/
└── SPA Fallback: /* → /index.html
```

### **Backend Container (FastAPI)**
```
Technologien:
├── FastAPI 0.95.2 (Web Framework)
├── SQLAlchemy 1.4.49 (ORM)
├── PostgreSQL psycopg2-binary (DB Driver)
├── Passlib + Argon2 (Password Hashing)
├── python-jose + cryptography (JWT)
├── google-generativeai (Gemini AI)
└── python-dotenv (Config)

Port: 8000
Routers:
├── /api/auth/ (Authentication)
├── /api/users/ (User Management - Admin)
├── /api/recipes/ (Recipe CRUD + AI Gen)
├── /api/ingredients/ (Ingredient Management)
├── /api/shopping-lists/ (Shopping Lists)
├── /api/news/ (News Feed)
└── /api/pages/ (Static Pages: Privacy, Terms)

Features:
├── JWT Authentication (30 min tokens)
├── Argon2 Password Hashing
├── Admin Role System
├── CORS Enabled
└── Gemini AI Recipe Generation
```

### **Database Container (PostgreSQL 15)**
```
Port: 5432
Database: reste-rampe-db
User: reste

Tables:
├── users (id, username, email, hashed_password, is_admin, created_at, last_login)
├── recipes (name, ingredients, instructions, is_healthy, language, created_at)
├── ingredients (name, category, location, quantity, expiry_date)
├── shopping_lists (name, created_at)
├── shopping_items (list_id, item_name, quantity, is_purchased)
├── news (title, content, category, language, published_at)
├── pages (slug, title, content, language, updated_at)
└── ai_suggestions (text, dietary, created_at)

Alembic Migrations:
├── 3de95423ff05_initial.py
├── 7a2b1b8f7f7a_add_ingredient_fields.py
├── 9c8f2a1b2a3b_add_ai_suggestions_table.py
└── add_user_timestamps.py (created_at, last_login)
```

---

## 🌐 Netzwerk-Kommunikation

### **Request Flow: Frontend → Backend**

```
1. Browser Request
   GET http://localhost:5173/admin
   
2. Nginx (Frontend)
   ├── Static: /index.html → Vue App lädt
   └── API: /api/users/ → Proxy zu Backend
   
3. Backend (FastAPI)
   ├── Route Handler: GET /api/users/
   ├── Auth Check: JWT Token validieren
   ├── Database: Query User Table
   └── Response: [user1, user2, user3] (JSON)
   
4. Browser (Vue)
   ├── Parse JSON Response
   ├── Update Component State
   └── Render Users Table
```

### **Data Flow: Login Example**

```
Frontend:                          Backend:                Database:
  │                                  │                        │
  ├─ POST /api/auth/login ────────→ │                        │
  │  (username, password)            │                        │
  │                                  ├─ Query users table ───→│
  │                                  │                    ←─(User Found)
  │                                  │                        │
  │                                  ├─ verify_password()     │
  │                                  │  (Argon2)              │
  │                                  │                        │
  │                                  ├─ create_access_token() │
  │                                  │  (JWT)                 │
  │                                  │                        │
  │ ←─────────────────────────────────┤                        │
  │    {access_token, token_type}     │                        │
  │                                  │                        │
  ├─ Store token in localStorage     │                        │
  │                                  │                        │
  ├─ GET /api/auth/me ───────────────→│                        │
  │  (Authorization: Bearer <token>)  │                        │
  │                                  ├─ JWT Decode & Verify   │
  │                                  ├─ Query users table ───→│
  │                                  │                    ←─(Current User)
  │ ←────────────────────────────────┤                        │
  │        {id, username, is_admin}   │                        │
  │                                  │                        │
  └─ Redirect to Dashboard           │                        │
```

---

## 🔐 Security Architecture

```
┌────────────────────────────────────────────┐
│         CLIENT (Browser)                   │
│  Stores JWT Token in localStorage          │
└─────────────────┬──────────────────────────┘
                  │ Authorization Header
                  │ Bearer <JWT_TOKEN>
                  │
┌─────────────────▼──────────────────────────┐
│      NGINX (Frontend Proxy)                │
│  ├─ CORS Headers                           │
│  ├─ Rate Limiting (optional)               │
│  └─ SSL/TLS (Production)                   │
└─────────────────┬──────────────────────────┘
                  │
┌─────────────────▼──────────────────────────┐
│      FastAPI Backend                       │
│  ├─ JWT Token Validation                   │
│  │  └─ decode(token, SECRET_KEY)           │
│  ├─ Extract Username from JWT              │
│  ├─ Database Lookup                        │
│  ├─ Check Permissions (is_admin)           │
│  └─ Execute Protected Endpoint             │
└─────────────────┬──────────────────────────┘
                  │
┌─────────────────▼──────────────────────────┐
│      PostgreSQL Database                   │
│  └─ Secure Password Storage (Argon2)       │
└────────────────────────────────────────────┘
```

---

## 🌍 Internationalization (i18n)

```
Frontend i18n Structure:
frontend/src/i18n/
├── index.js (i18n Configuration)
└── locales/
    ├── de.json (Deutsch) ✅
    ├── en.json (English) ✅
    ├── fr.json (Français) ✅
    ├── ja.json (日本語) ✅
    ├── tr.json (Türkçe) ✅
    ├── fa.json (فارسی) ✅
    └── nds.json (Low German) ✅

Key Translations:
├── Navigation (nav.*)
├── Authentication (login.*, register.*)
├── Recipes (recipes.*)
├── Admin (admin.users.*, admin.news.*, admin.pages.*)
└── Common UI (common.*)

Language Auto-Detection:
1. Check localStorage for saved language
2. Get browser language (navigator.language)
3. Fall back to German (de)
```

---

## 📡 API Routes & Authentication

```
PUBLIC ROUTES (No Auth Required):
├── POST   /api/auth/register
├── POST   /api/auth/login
├── GET    /api/pages/public/{slug}
├── GET    /api/news/public
└── GET    /api/recipes/public

AUTHENTICATED ROUTES (Bearer Token):
├── GET    /api/auth/me
├── GET    /api/users/              (Admin Only)
├── PUT    /api/users/{id}/admin    (Admin Only)
├── DELETE /api/users/{id}/         (Admin Only)
├── GET    /api/recipes/
├── POST   /api/recipes/
├── GET    /api/ingredients/
├── POST   /api/ingredients/
├── GET    /api/shopping-lists/
├── POST   /api/news/admin          (Admin)
├── DELETE /api/news/{id}           (Admin)
└── PUT    /api/pages/              (Admin)

Auth Header Format:
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## 🚀 Development Stack

```
Frontend Stack:
├── Node.js 18+
├── npm/yarn
├── Vite (Build)
├── Vue 3 (Composition API)
├── Tailwind CSS 3
├── Axios
└── draw.io (Diagrams)

Backend Stack:
├── Python 3.11+
├── FastAPI
├── SQLAlchemy
├── PostgreSQL 15
├── Alembic (Migrations)
└── Gemini AI API

DevOps:
├── Docker & Docker Compose
├── Nginx 1.25
├── PostgreSQL 15
└── Environment Variables (.env files)

Monitoring:
├── Docker Logs
├── Browser Console (Frontend)
└── Backend Uvicorn Logs
```

---

## 📊 Database Schema Relations

```
┌──────────────┐
│ users        │
├──────────────┤
│ id (PK)      │
│ username     │
│ email        │
│ hashed_pwd   │
│ is_admin     │
│ created_at   │
│ last_login   │
└──────────────┘
       │
       │ (Owner)
       │
       ├──────────────────────┬────────────────────────┐
       │                      │                        │
       ▼                      ▼                        ▼
┌─────────────┐         ┌──────────┐          ┌─────────────┐
│ recipes     │         │ news     │          │ shopping_   │
│             │         │          │          │ lists       │
├─────────────┤         ├──────────┤          ├─────────────┤
│ id (PK)     │         │ id (PK)  │          │ id (PK)     │
│ name        │         │ title    │          │ name        │
│ ingredients │         │ content  │          │ created_at  │
│ language    │         │ language │          └─────────────┘
│ is_healthy  │         │ pub date │                  │
└─────────────┘         └──────────┘                  │
                                              ┌───────▼────────┐
┌─────────────┐                               │shopping_items  │
│ ingredients │                               ├────────────────┤
├─────────────┤                               │ id (PK)        │
│ id (PK)     │                               │ list_id (FK)   │
│ name        │                               │ item_name      │
│ category    │                               │ quantity       │
│ expiry_date │                               │ is_purchased   │
└─────────────┘                               └────────────────┘

┌──────────────┐
│ pages        │
├──────────────┤
│ id (PK)      │
│ slug (UQ)    │
│ title        │
│ content      │
│ language     │
│ updated_at   │
└──────────────┘

┌──────────────────────┐
│ ai_suggestions       │
├──────────────────────┤
│ id (PK)              │
│ text                 │
│ dietary              │
│ created_at           │
└──────────────────────┘
```

---

## 🎯 Feature Overview

| Feature | Status | Technology |
|---------|--------|-----------|
| User Authentication | ✅ | JWT + Argon2 |
| User Management | ✅ | Admin Roles |
| Recipe Management | ✅ | CRUD + Gemini AI |
| Ingredient Tracking | ✅ | CRUD + Expiry Dates |
| Shopping Lists | ✅ | CRUD |
| News Feed | ✅ | Backend Admin |
| Privacy Page | ✅ | Markdown + DOMPurify |
| Multilingual (7 lang) | ✅ | vue-i18n |
| Admin Panel | ✅ | User/News/Pages Mgmt |
| AI Recipe Generation | ✅ | Google Gemini API |

---

## 📝 How to View the Draw.io Diagram

1. **In VS Code:**
   - Install "Draw.io" Extension
   - Open `/home/florian/reste-rampe/ARCHITECTURE.drawio`
   - Extension auto-opens in draw.io viewer

2. **Online:**
   - Go to https://app.diagrams.net/
   - File → Open → Select `ARCHITECTURE.drawio`

3. **Export:**
   - Open in draw.io
   - File → Export as PNG/SVG/PDF
   - Save for presentations

---

Viel Erfolg mit Reste-Rampe! 🚀
