# ESMS Frontend (React + Vite)

Quickstart:

Install dependencies and run dev server:

```bash
cd frontend
npm install
npm run dev
```

Set backend URL in `.env` (copy from `.env.example`) as `VITE_API_URL` (e.g. `http://localhost:8000`).

Pages scaffolded: Login, Register, Dashboard, Employees, Teams, Skills, Skill Ratings.

Testing / Run steps:

1. Start the backend (from repo root):

```bash
# ensure your .env contains DB URL and JWT settings
uvicorn ESMS.main:app --reload
```

2. Start the frontend:

```bash
cd frontend
npm install
npm run dev
```

3. Quick manual test flow:
- Open the frontend URL printed by Vite (usually http://localhost:5173).
- Register a new user via `/register`.
- Login via `/login` (login stores token and protects routes).
- Visit `Employees`, `Teams`, `Skills`, and `Skill Ratings` pages to load lists/details.

Notes:
- The login form sends URL-encoded credentials to the backend OAuth2 endpoint.
- Protected routes require a valid JWT; the header is set automatically after login.
- If the backend is on a different host/port, set `VITE_API_URL` in `.env` accordingly.

Tailwind setup:

1. Install the new dev dependencies added to `package.json`:

```bash
cd frontend
npm install
```

2. If already running, restart the dev server so Vite picks up PostCSS/Tailwind.

UI notes:
- Employee detail pages now include a rating editor. Managers can edit `manager_rating`; employees can edit `self_rating` for themselves.
- Assigning skills remains available to managers on the employee detail page.
