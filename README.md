# Content Automation Platform

An AI-powered, multi-site publishing engine that auto-generates, humanizes, approves, and distributes articles across multiple niche websites.

## Project Structure

content-automation-platform/
├── backend/        # Django + DRF API (core logic, approvals, metadata)
├── frontend/       # Next.js 15 frontend (multi-site, themed per brand)
├── cms/            # WordPress (headless, ACF, structured fields)
├── infra/          # Docker, CI/CD, shared environment config

## MVP Features

- Daily Article Generation via GPT-4
- Tone Customization per site using site-specific prompts
- Human Review Interface via Django Admin
- StealthGPT to humanize and de-plagiarize AI content
- Publishing to WordPress using REST API
- Multi-Site Frontend via dynamic routes in Next.js
- Auto-Social Posting via n8n workflows

## Tech Stack

| Layer       | Tech                                      |
|-------------|-------------------------------------------|
| Frontend    | Next.js 15, Tailwind CSS v4, Framer Motion |
| Backend     | Django 5.1.6, DRF, PostgreSQL              |
| CMS         | WordPress (Headless, ACF, JWT/Auth)        |
| Automation  | n8n, GPT-4, StealthGPT                     |
| DevOps      | Docker, GitHub Actions                     |
| Hosting     | Vercel (frontend), Render (API), WP Host   |

## Local Dev Setup (coming soon)

- Docker Compose for all services
- .env templates for backend, frontend, CMS
- asdf for tool version management
- One-line bootstrapping script

## Post-MVP Plans

- Stripe subscriptions for premium content
- Reader accounts with personalization
- Admin dashboard for workflow control
- Feedback loops to fine-tune prompts
- Vendor/sponsor accounts
- Scalable to 10, 50, or 100+ verticals

## Contributing

This is a solo project but structured for future contributors. Please follow:

- Semantic commits (type(scope): message)
- Consistent code formatting
- Feature-specific commits per service layer
