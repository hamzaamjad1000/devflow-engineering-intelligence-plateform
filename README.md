# DevFlow - Enginnering Intelligence Plateform

### Engineering Intelligence & Delivery Management Platform

DevFlow Nexus is a modern engineering operations platform for managing projects, tasks, teams, delivery progress, analytics, and workspace administration from one focused console.

It combines a Kanban workflow with engineering intelligence views so teams can understand not only what is being built, but also how work is progressing.

![DevFlow Nexus](https://img.shields.io/badge/DevFlow-Nexus-8B7FFF?style=for-the-badge)
![Next.js](https://img.shields.io/badge/Next.js-16-black?style=flat-square&logo=next.js)
![React](https://img.shields.io/badge/React-19-61DAFB?style=flat-square&logo=react)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=flat-square&logo=fastapi)

## Product Overview

DevFlow Nexus gives engineering teams a single workspace to:

- Organize projects and delivery tasks
- Track work through a drag-and-drop Kanban board
- Monitor completion, velocity, health, and task distribution
- Review team members and individual progress
- Search projects, tasks, and members globally
- Manage workspace users, projects, tasks, and roles through an admin console

## Core Features

### Engineering Dashboard

- Project health score and engineering quality indicators
- Sprint velocity visualization
- Task completion and sprint progress metrics
- Bug-rate and developer-velocity indicators
- Workspace activity timeline

### Kanban Delivery Board

- To Do, In Progress, and Done workflow columns
- Drag-and-drop task movement
- Project-aware task creation
- Task ownership and member assignment
- Status updates synchronized with the backend

### Analytics

- Project and task totals
- Task distribution by status
- Completion-rate tracking
- Bugs reported versus resolved visualization
- Engineering activity insights

### Team & Member Profiles

- Directory of registered workspace members
- Member IDs and email identities
- Individual task progress
- Completed and in-progress task metrics
- Clickable profile drill-down views

### Admin Control Center

Administrators can manage the complete workspace from `/admin`:

- Create, edit, and delete users
- Reset member passwords
- Grant or remove admin access
- Create, edit, and delete projects
- Create, edit, assign, update, and delete tasks
- Monitor members, projects, tasks, and completion totals

### Authentication & Access Control

- JWT-based authentication
- Separate member and admin sign-in flows
- Admin-only management endpoints
- Password hashing with Passlib/Bcrypt
- Protected project, task, user, and search APIs

## Technology Stack

### Frontend

- Next.js 16
- React 19
- TypeScript
- Tailwind CSS
- Custom dark engineering-console design system

### Backend

- Python
- FastAPI
- SQLAlchemy
- SQLite
- JWT authentication
- Passlib and Bcrypt password hashing

## Project Structure

```text
DevFlow/
├── backend/
│   ├── auth.py              # JWT and password authentication
│   ├── database.py          # SQLAlchemy database configuration
│   ├── main.py              # FastAPI routes and admin APIs
│   ├── models.py            # Database models
│   ├── schemas.py           # Request validation schemas
│   └── devflow.db           # Local SQLite database
│
├── frontend/
│   ├── app/
│   │   ├── admin/           # Admin login and control center
│   │   ├── analytics/        # Analytics dashboard
│   │   ├── dashboard/        # Engineering dashboard
│   │   ├── insights/         # Engineering insights
│   │   ├── kanban/           # Task board
│   │   ├── members/          # Member profile pages
│   │   ├── settings/         # Workspace settings
│   │   ├── team/             # Team directory
│   │   └── components/       # Shared application shell
│   └── package.json
│
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- npm

### 1. Start the Backend

```powershell
cd backend
.\venv\Scripts\Activate.ps1
pip install fastapi uvicorn sqlalchemy passlib bcrypt python-jose email-validator
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

### 2. Start the Frontend

Open a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

Open the application at:

```text
http://localhost:3000
```

## Authentication

Create a normal account from the application registration screen, then sign in through the member login page.

The admin console is available at:

```text
http://localhost:3000/admin/login
```

Admin credentials should be configured for your local environment. Do not commit real passwords, secrets, or production credentials to GitHub.

## API Highlights

| Method | Endpoint | Purpose |
|---|---|---|
| `POST` | `/register` | Register a member |
| `POST` | `/login` | Member authentication |
| `POST` | `/admin/login` | Admin authentication |
| `GET` | `/me` | Current authenticated user |
| `GET` | `/users` | Workspace members |
| `GET` | `/projects` | Workspace projects |
| `POST` | `/projects` | Create a project |
| `GET` | `/tasks` | Workspace tasks |
| `POST` | `/tasks` | Create a task |
| `PUT` | `/tasks/{task_id}` | Update task status/details |
| `GET` | `/search?q=` | Search workspace records |
| `GET` | `/admin/users` | Admin member management |
| `PUT` | `/admin/users/{member_id}` | Admin update member |
| `DELETE` | `/admin/users/{member_id}` | Admin delete member |
| `PUT` | `/admin/projects/{project_id}` | Admin update project |
| `DELETE` | `/admin/projects/{project_id}` | Admin delete project |
| `POST` | `/admin/tasks` | Admin create and assign task |
| `DELETE` | `/admin/tasks/{task_id}` | Admin delete task |

## Design Direction

DevFlow Nexus uses a dark, data-dense engineering console interface designed for long working sessions:

- Deep navy workspace surfaces
- Violet, teal, amber, red, and blue status accents
- Clear monospace metric labels
- Compact operational navigation
- Responsive layouts for desktop and smaller screens

## Development Commands

Frontend:

```powershell
npm run dev       # Start development server
npm run build     # Create production build
npm run start     # Start production server
npx tsc --noEmit  # Type-check frontend
```

Backend:

```powershell
uvicorn main:app --reload
```

## Security Notes

Before deploying to production:

- Move the JWT secret into environment variables
- Use a production database instead of local SQLite
- Configure production CORS origins
- Add rate limiting and audit logging
- Use secure password and admin-account provisioning
- Never commit `.env` files, database backups, or real credentials

## Roadmap

- GitHub and GitLab repository integrations
- Pull request and deployment activity sync
- Role-based workspace permissions
- Notifications and activity subscriptions
- Advanced sprint reporting
- PostgreSQL production support
- Docker Compose deployment

## Author

Built as a focused engineering operations platform for teams that want clearer delivery visibility, stronger collaboration, and actionable project intelligence.
