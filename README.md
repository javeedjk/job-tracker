\# Job Application Tracker



A full-stack web application to track job applications through every stage of the hiring process — from applied to offer.



\*\*Live Demo:\*\* https://job-tracker-ten-beige.vercel.app

\*\*Backend API Docs:\*\* https://job-tracker-api-qavg.onrender.com/docs



\---



\## Features



\- \*\*User authentication\*\* — secure signup and login with JWT tokens and bcrypt password hashing

\- \*\*Full CRUD\*\* — add, view, edit, and delete job applications

\- \*\*Status tracking\*\* — track each application through Applied, Interviewing, Offer, Rejected, or Withdrawn

\- \*\*Protected routes\*\* — all application data is user-scoped; no user can access another's data

\- \*\*Automated tests\*\* — 13 pytest integration tests covering auth, CRUD, and data isolation



\---



\## Tech Stack



\*\*Backend\*\*

\- FastAPI (Python) — REST API framework

\- PostgreSQL — relational database

\- SQLAlchemy — ORM for database interaction

\- JWT (python-jose) — token-based authentication

\- bcrypt (passlib) — password hashing

\- pytest + httpx — integration testing



\*\*Frontend\*\*

\- React — UI framework

\- React Router — client-side routing

\- Tailwind CSS — utility-first styling

\- Axios — HTTP client

\- Vite — build tool



\*\*Deployment\*\*

\- Render — backend + PostgreSQL hosting

\- Vercel — frontend hosting



\---



\## Project Structure

job-tracker/

├── backend/

│   ├── app/

│   │   ├── main.py        # FastAPI app and route definitions

│   │   ├── models.py      # SQLAlchemy database models

│   │   ├── schemas.py     # Pydantic request/response schemas

│   │   ├── crud.py        # Database operations

│   │   ├── auth.py        # JWT token creation and verification

│   │   ├── security.py    # Password hashing utilities

│   │   └── database.py    # Database connection setup

│   ├── tests/

│   │   ├── conftest.py    # Test fixtures and SQLite test database setup

│   │   └── test\_api.py    # 13 integration tests

│   └── requirements.txt

└── frontend/

└── src/

├── api/           # Axios client and API helper functions

├── pages/         # Login, Signup, Dashboard, ApplicationForm

└── App.jsx        # React Router setup



\---



\## Running Locally



\### Backend



```bash

cd backend

python -m venv venv

venv\\Scripts\\activate        # Windows

pip install -r requirements.txt



\# Create a .env file with:

\# DATABASE\_URL=postgresql://user:password@localhost:5432/job\_tracker

\# SECRET\_KEY=your-secret-key



uvicorn app.main:app --reload

```



API runs at `http://127.0.0.1:8000`  

Interactive docs at `http://127.0.0.1:8000/docs`



\### Frontend



```bash

cd frontend

npm install



\# Create a .env file with:

\# VITE\_API\_URL=http://127.0.0.1:8000



npm run dev

```



Frontend runs at `http://localhost:5173`



\### Running Tests



```bash

cd backend

pytest tests/ -v

```



\---



\## API Endpoints



| Method | Endpoint | Auth Required | Description |

|--------|----------|---------------|-------------|

| POST | `/users` | No | Create a new user account |

| POST | `/login` | No | Log in, receive JWT token |

| GET | `/applications` | Yes | List all applications for current user |

| POST | `/applications` | Yes | Create a new application |

| GET | `/applications/{id}` | Yes | Get a specific application |

| PUT | `/applications/{id}` | Yes | Update an application |

| DELETE | `/applications/{id}` | Yes | Delete an application |



\---



\## Author



Javeed Kamal  

\[GitHub](https://github.com/javeedjk) | \[LinkedIn](https://www.linkedin.com/in/javeed-shaik-12b377194)



