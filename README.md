Student Data Warehouse — Full Project README

Overview
The Student Data Warehouse is a full‑stack platform to manage student profiles, placements, research projects, clubs, skills, and achievements. It includes a React + TypeScript frontend and a Node.js + Express + MySQL backend with JWT authentication and role‑based access control.

Tech Stack
- Frontend: React (Vite), TypeScript, Tailwind CSS, React Router, React Query, Zustand
- Backend: Node.js, Express.js, MySQL (mysql2/promise), Joi validation, Multer uploads
- Auth: JWT with role‑based authorization

Repository Structure
./
├── backend/   API server, services, models, controllers, routes, migrations
└── frontend/  Web client, pages, components, stores, API layer

Roles & Access
- Admin: Full control across modules
- CIR: Company and placements management
- Faculty: Research projects and participants
- Student: Profile, invitations, and placements visibility

Quick Start
Prerequisites
- Node.js 16+
- MySQL 8+
- npm (or yarn)

Backend (API)
1) cd backend
2) npm install
3) Copy env.example to .env and configure MySQL and JWT
   Example:
   MYSQL_HOST=localhost
   MYSQL_PORT=3306
   MYSQL_USER=root
   MYSQL_PASSWORD=your-password
   MYSQL_DATABASE=student_dw
   JWT_SECRET=your-jwt-secret
   PORT=4000
4) Run database migrations: npm run migrate
5) Optional seed data: npm run seed
6) Start development server: npm run dev
   API available at http://localhost:4000 (base path /api)

Frontend (Web App)
1) cd frontend
2) npm install
3) Copy env.example to .env
4) Set API base URL: VITE_API_BASE_URL=http://localhost:4000/api
5) Start development server: npm run dev
   App available at http://localhost:5173 (Vite will use the next port if 5173 is busy)

Configuration
- Backend: See backend/env.example for DB and auth settings
- Frontend: Set VITE_API_BASE_URL to your API (defaults to http://localhost:4000/api)

Core Features
- Authentication: Login, JWT management, role‑based navigation
- Students: List, search, filter, profile details, skills/interests
- Companies & Job Roles: Manage companies, create/update/delete job roles
- Placements & Invitations: Offer tracking, suggest students via invitations, status updates
- Research Projects: View projects and participants, faculty management
- Skills & Interests: Catalog management and student association
- Clubs: Club creation and invitations (with role checks)

API Basics
- Base URL: http://localhost:4000/api
- Format: JSON with standardized success/error shape
- Auth: Bearer JWT required for protected routes

Scripts
Backend:
- npm run dev     Start dev server
- npm start       Start production server
- npm run migrate Apply database migrations
- npm run seed    Seed baseline data
- npm test        Run tests

Frontend:
- npm run dev     Start dev server
- npm run build   Build for production
- npm run preview Preview production build
- npm run lint    Run ESLint

Build & Deploy
Frontend:
- npm run build creates a production bundle in frontend/dist/
- Serve static files via Nginx/Apache or the backend if integrated

Backend:
- npm start runs the API
- Use a process manager (PM2/system service)
- Configure environment variables and secure JWT secrets

Troubleshooting
- If the frontend doesn’t load, confirm VITE_API_BASE_URL matches your backend port and path (/api)
- If port 5173 is busy, Vite will use the next available port (e.g., 5174)
- Check backend logs for validation/authorization errors; ensure roles are correct

Contributing
- Keep changes scoped and consistent with existing patterns
- Add loading/error states for async features
- Follow TypeScript and linting guidelines

