# Content Automation Platform - Frontend

This is the Next.js 15 frontend for the Content Automation Platform, providing a dynamic, multi-site content management interface with admin controls and AI-powered content generation.

## Features

- **Multi-Site Support**: Dynamic routing for multiple branded sites
- **Admin Interface**: Protected admin dashboard with article management
- **AI Content Generation**: Interface for creating AI-generated content
- **Authentication**: Secure login/logout with session management
- **Responsive Design**: Mobile-friendly interface with Tailwind CSS
- **TypeScript**: Full type safety and better development experience

## Tech Stack

- **Next.js 15.3.4** with App Router
- **React 19.0.0**
- **TypeScript 5.x**
- **Tailwind CSS 4.x**
- **Client-side components** for admin functionality

## Getting Started

1. **Install dependencies**
   npm install

2. **Start the development server**
   npm run dev

3. **Access the application**
   - Frontend: http://localhost:3000
   - Admin interface: http://localhost:3000/admin
   - Login page: http://localhost:3000/admin/login

## Project Structure

```
src/
├── app/                    # Next.js app router pages
│   ├── admin/             # Admin interface pages
│   │   ├── articles/      # Article management
│   │   ├── ai-content/    # AI content generation
│   │   └── login/         # Authentication
│   ├── [site]/            # Dynamic site pages
│   │   └── [slug]/        # Individual article pages
│   └── layout.tsx         # Root layout
├── lib/                   # Utility functions
│   ├── auth.tsx           # Authentication utilities
│   └── getSiteConfig.ts   # Site configuration
└── types/                 # TypeScript type definitions
```

## Key Components

### Admin Interface
- **Dashboard**: Overview with article statistics
- **Article Management**: Filter, approve, reject, and manage articles
- **AI Content Generation**: Create AI-generated content for sites
- **Authentication**: Secure login with CSRF protection

### Public Sites
- **Dynamic Routing**: Site-specific pages with custom branding
- **Article Display**: Individual article pages with proper formatting
- **Search & Filter**: Find articles by category and status
- **Responsive Design**: Mobile-friendly layouts

## Development

### Available Scripts
- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint

### Environment Variables
The frontend connects to the Django backend API. Ensure the backend is running on `http://localhost:8000` or update the API endpoints accordingly.

## Deployment

This frontend can be deployed to any platform that supports Next.js:

- **Vercel** (recommended)
- **Netlify**
- **AWS Amplify**
- **Self-hosted**
