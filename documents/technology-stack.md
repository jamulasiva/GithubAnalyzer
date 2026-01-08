# Technology Stack Summary - GitHub Audit Platform

**Updated:** January 2, 2026  
**Technology Choices:** Supabase + FastAPI + React/Vite + Tailwind CSS

## Core Technology Stack

### Backend
- **Framework**: FastAPI 0.108+ (Python 3.11+)
- **Database**: Supabase (Managed PostgreSQL 15+)
- **ORM**: SQLAlchemy 2.0+ with asyncpg driver
- **Authentication**: Supabase Auth + JWT
- **Task Queue**: Celery + Redis (or Supabase Edge Functions)
- **API Client**: HTTPX (async)
- **Validation**: Pydantic 2.5+

### Frontend
- **Framework**: React 18+
- **Build Tool**: Vite 5+
- **Styling**: Tailwind CSS 3+
- **UI Components**: HeadlessUI + Heroicons
- **State Management**: Redux Toolkit + RTK Query
- **Forms**: React Hook Form + Zod validation
- **Charts**: Chart.js + React-Chartjs-2
- **HTTP Client**: Axios + Supabase JS Client

### Database & Storage
- **Primary DB**: Supabase PostgreSQL with real-time subscriptions
- **File Storage**: Supabase Storage (S3-compatible)
- **Search**: PostgreSQL Full-Text Search
- **Caching**: Redis or Supabase Edge Functions
- **Backups**: Supabase automated backups + PITR

### Infrastructure
- **Containerization**: Docker + Docker Compose
- **Deployment**: Vercel/Netlify (Frontend) + Railway/Render (Backend)
- **CI/CD**: GitHub Actions
- **Monitoring**: Supabase Dashboard + custom metrics

## Key Benefits of This Stack

### Supabase Advantages
- **Managed PostgreSQL** with automatic scaling and backups
- **Real-time subscriptions** for live dashboard updates
- **Built-in authentication** with social providers and RLS
- **Edge Functions** for serverless background processing
- **Auto-generated APIs** and real-time capabilities
- **Storage solution** with CDN and image transformations

### React + Vite + Tailwind Advantages
- **Fast development** with hot module replacement
- **Modern build tool** with optimized bundling
- **Utility-first CSS** for rapid UI development
- **Excellent TypeScript support** out of the box
- **Small bundle sizes** and great performance

### FastAPI + SQLAlchemy Advantages
- **High performance** async web framework
- **Automatic API documentation** with OpenAPI/Swagger
- **Type safety** with Pydantic models
- **Async database operations** with asyncpg
- **Easy testing** and great developer experience

## Development Environment Setup

### Prerequisites
```bash
# Install required tools
npm install -g @supabase/cli
pip install poetry  # Python dependency management
```

### Supabase Setup
```bash
# Initialize Supabase project
supabase init
supabase start  # Start local development stack
supabase db reset  # Reset database with migrations
```

### Backend Setup
```bash
cd backend
poetry install  # Install Python dependencies
poetry run uvicorn app.main:app --reload  # Start FastAPI server
```

### Frontend Setup
```bash
cd frontend
npm install  # Install Node.js dependencies
npm run dev  # Start Vite development server
```

## Configuration Files

### Backend Dependencies (pyproject.toml)
```toml
[tool.poetry.dependencies]
python = "^3.11"
fastapi = "^0.108.0"
uvicorn = {extras = ["standard"], version = "^0.25.0"}
sqlalchemy = {extras = ["asyncio"], version = "^2.0.23"}
alembic = "^1.13.1"
asyncpg = "^0.29.0"
supabase = "^2.3.0"
pydantic = "^2.5.2"
httpx = "^0.25.2"
celery = "^5.3.4"
redis = "^5.0.1"
python-dotenv = "^1.0.0"
```

### Frontend Config (package.json)
```json
{
  "name": "github-audit-frontend",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.8.0",
    "@supabase/supabase-js": "^2.38.0",
    "@reduxjs/toolkit": "^2.0.1",
    "react-redux": "^9.0.4",
    "tailwindcss": "^3.4.0",
    "@headlessui/react": "^1.7.17",
    "@heroicons/react": "^2.0.18",
    "chart.js": "^4.4.0",
    "react-chartjs-2": "^5.2.0"
  }
}
```

### Vite Config (vite.config.ts)
```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      }
    }
  }
})
```

### Tailwind Config (tailwind.config.js)
```javascript
module.exports = {
  content: ['./src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
        }
      }
    }
  },
  plugins: [
    require('@headlessui/tailwindcss'),
  ]
}
```

This technology stack provides an excellent foundation for building a modern, scalable, and maintainable GitHub audit platform!