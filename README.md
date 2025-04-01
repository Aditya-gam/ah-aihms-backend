# 🧠 AH-AIHMS Backend

The official backend for the **AI-Driven Healthcare Management System (AH-AIHMS)** — built with **Flask**, containerized using **Docker**, managed via **Pipenv**, and deployed through **GitHub Actions CI/CD**. This backend serves secure REST APIs for authentication, patient records, appointments, blockchain integrations, and AI-powered health analytics.

![CI/CD](https://github.com/Aditya-gam/ah-aihms-backend/actions/workflows/backend.yml/badge.svg)
[![codecov](https://codecov.io/gh/Aditya-gam/ah-aihms-backend/branch/master/graph/badge.svg?token=CODECOV_TOKEN)](https://codecov.io/gh/Aditya-gam/ah-aihms-backend)


---

## 📦 Tech Stack

| Layer              | Technology                            |
|-------------------|----------------------------------------|
| Backend Framework  | Flask 3.0.x                            |
| Language           | Python 3.11.x                          |
| Virtual Env Tool   | Pipenv 2024.x                          |
| Linting            | Flake8                                |
| Formatting         | Black, isort                          |
| Containerization   | Docker, Docker Compose                |
| CI/CD              | GitHub Actions                        |
| Deployment Target  | Compatible with Vercel frontend setup |

---

## 🗂️ Project Structure

```
ah-aihms-backend/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── routes/
│   │   └── auth.py
│   ├── models/
│   ├── services/
│   └── utils/
├── tests/
│   └── test_auth.py
├── .github/workflows/backend.yml
├── .env
├── .flaskenv
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── Pipfile
├── Pipfile.lock
├── README.md
└── run.py
```

---

## 🔧 Local Setup Instructions

### 🛑 Prerequisites (Install Globally)

> You only need to do this once per system:

#### 1. Install Python 3.11
```bash
brew install python@3.11
```

#### 2. Install Pipenv
```bash
brew install pipenv
```

---

### ⚙️ Project Setup

Clone the repo and navigate into it:

```bash
git clone https://github.com/Aditya-gam/ah-aihms-backend.git
cd ah-aihms-backend
```

---

### 1. Create Virtual Environment & Install Flask

```bash
pipenv --python 3.11
pipenv install flask==3.0.2
```

---

### 2. Install Development Tools

```bash
pipenv install --dev black flake8 isort
```

---

### 3. Lock Dependencies

```bash
pipenv lock
```

---

### 4. Run App (Locally)

```bash
pipenv run python run.py
```

Open browser at:  
📍 `http://localhost:5000/api/auth/status`  
Expected Output:
```json
{ "status": "auth route working" }
```

---

## 🐳 Docker Setup (Optional)

### 1. Build and Run

```bash
docker-compose up --build
```

App will be live at: `http://localhost:5000/api/auth/status`

---

## ✅ Linting & Formatting

Run linting:

```bash
pipenv run lint
```

Auto-format code:

```bash
pipenv run format
```

---

## 🔁 CI/CD Pipeline (GitHub Actions)

GitHub Actions is configured to:

- Run Flake8 linter
- Run (placeholder) tests
- Trigger on every push to `main`

📄 File: `.github/workflows/backend.yml`

```yaml
name: Backend CI/CD

on:
  push:
    branches: [main]

jobs:
  backend:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: 3.11

      - name: Install Pipenv + Dependencies
        run: |
          python -m pip install pipenv
          pipenv install --dev

      - name: Lint Code
        run: pipenv run lint

      - name: Run Tests
        run: echo "✅ Add pytest later"
```

---

## 🌐 Frontend Integration

Set in your frontend `.env.development`:

```env
REACT_APP_API_BASE_URL=http://localhost:5000/api
```

### Example Axios Instance (Frontend)

```js
import axios from 'axios';

const API = axios.create({
  baseURL: process.env.REACT_APP_API_BASE_URL,
});

export default API;
```

---

## 📋 API Example (for Testing)

- **Route:** `GET /api/auth/status`
- **Description:** Health check for `auth` blueprint
- **Response:**

```json
{
  "status": "auth route working"
}
```

---

## 🧪 Testing

> Add `pytest` setup in a later story

```bash
mkdir tests/
touch tests/test_auth.py
```

---

## 🧾 Contribution Guidelines

1. Fork the repository
2. Create a new branch: `git checkout -b feature/feature-name`
3. Commit your changes: `git commit -m "feat: Add feature"`
4. Push to the branch: `git push origin feature/feature-name`
5. Create a Pull Request

---

## 📄 License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for full details.

---

## 📧 Contact

**Aditya Gambhir**  
📬 [agamb031@ucr.edu](mailto:agamb031@ucr.edu)

**Ajit Singh**  
📬 [asing349@ucr.edu](mailto:asing349@ucr.edu)

📦 Project Repo: [ah-aihms-backend](https://github.com/Aditya-gam/ah-aihms-backend)

---

## 📚 References

- [Flask Docs](https://flask.palletsprojects.com/)
- [Pipenv Docs](https://pipenv.pypa.io/en/latest/)
- [Docker Docs](https://docs.docker.com/)
- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Black Formatter](https://black.readthedocs.io/en/stable/)
- [Flake8](https://flake8.pycqa.org/en/latest/)