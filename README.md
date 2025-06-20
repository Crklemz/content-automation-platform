# Content Automation Platform

A Django + Next.js platform that uses AI to generate and publish weekly articles across multiple branded sites. Each site has its own topic, branding, and dynamic content pipeline.

---

## 🧠 What It Does

- Scrapes trending news about a topic
- Summarizes articles using OpenAI
- Stores drafts in Django backend
- Lets admin approve/reject content
- Displays approved articles per site in a branded frontend

---

## 🛠 Tech Stack

**Backend:**
- Django + DRF
- PostgreSQL
- Celery + Redis (for scheduled tasks)
- Python-dotenv

**Frontend:**
- Next.js
- Tailwind CSS
- SWR or Axios

**AI & Automation:**
- OpenAI (GPT-4)
- SerpAPI / NewsAPI / Custom scraper

**Dev & Infra:**
- Docker (optional)
- Git + GitHub
- Trello (project management)

---

## 📁 Repo Structure

### `/backend/`
Django backend code, models, API logic, Celery tasks, and `.env` config.

### `/frontend/`
Next.js frontend app with Tailwind styling, API fetching, and site branding.

### `/assets/`
Logos, images, or other static site visuals.

### `/data/`
Configuration files like `site_config.json` and AI prompt templates.

### Root Files
- `.gitignore`
- `README.md`

---

## ✅ Getting Started (Local Dev)

1. Clone the repo
2. Add `.env` files to `/backend` and `/frontend`
3. Install backend dependencies:
    cd backend
    pip install -r requirements.txt
4. Install frontend dependencies:
    cd ../frontend
    npm install
5. Start both apps:
    # In backend
    python manage.py runserver
    # In frontend
    npm run dev
