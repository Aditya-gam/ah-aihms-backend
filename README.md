# 🧠 AH-AIHMS Backend

**AI-Driven Healthcare Management System (AH-AIHMS)** backend built using **Flask**, containerized with **Docker**, managed via **venv**, tested rigorously, and seamlessly deployed using **GitHub Actions CI/CD** on **Render**. It provides secure REST APIs for user authentication, patient records, appointment scheduling, blockchain integrations, and AI-powered analytics, all backed by **MongoDB Atlas**.

[![CI/CD](https://github.com/Aditya-gam/ah-aihms-backend/actions/workflows/backend.yml/badge.svg)](https://github.com/Aditya-gam/ah-aihms-backend/actions/workflows/backend.yml)
[![Codecov](https://codecov.io/gh/Aditya-gam/ah-aihms-backend/branch/master/graph/badge.svg?token=CODECOV_TOKEN)](https://codecov.io/gh/Aditya-gam/ah-aihms-backend)

---

## 🚀 Tech Stack

| Layer                | Technology                                 |
|----------------------|--------------------------------------------|
| **Framework**        | Flask 3.0.2                                |
| **Language**         | Python 3.11                                |
| **Environment**      | venv + requirements.txt                    |
| **Database**         | MongoDB Atlas                              |
| **ODM**              | Flask-MongoEngine                          |
| **Linting**          | Flake8, Ruff                               |
| **Formatting**       | Black, isort                               |
| **Testing**          | pytest, pytest-cov                         |
| **CI/CD**            | GitHub Actions                             |
| **Deployment**       | Render                                     |
| **Containerization** | Docker, Docker Compose                     |
| **Monitoring**       | Sentry                                     |

---

## 📂 Project Structure

```bash
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
├── requirements.txt
├── dev-requirements.txt
├── pyproject.toml
├── .pre-commit-config.yaml
├── README.md
└── run.py
```

---

## 🔧 Local Setup Instructions

### 🛑 Prerequisites

Install Python 3.11:

```bash
brew install python@3.11
```

### ⚙️ Project Setup

Clone the repository and navigate inside:

```bash
git clone https://github.com/Aditya-gam/ah-aihms-backend.git
cd ah-aihms-backend
```

### 📦 Create Virtual Environment and Install Dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install -r dev-requirements.txt
```

### 🚀 Run the Application Locally

```bash
flask run
```

Open browser at:  
📍 `http://localhost:5000/api/auth/status`

Expected Response:
```json
{ "status": "auth route working" }
```

---

## 🐳 Docker & Docker Compose

### Build Docker Container

```bash
docker-compose build
```

### Run Docker Container

```bash
docker-compose up
```

The app will be accessible at:  
📍 `http://localhost:5001/api/auth/status`

---

## ✅ Linting & Formatting

### Run Lint Checks

```bash
black --check app
isort --check-only app
ruff check app
```

### Auto-format Code

```bash
black app
isort app
ruff check --fix app
```

### Pre-commit Hooks Setup

Install pre-commit hooks to auto-format before commits:

```bash
pre-commit install
```

---

## 🧪 Testing & Coverage

Run tests with coverage reports:

```bash
pytest tests/ --cov=app --cov-report=term-missing
```

---

## 🔁 CI/CD Pipeline (GitHub Actions)

Configured for:

- Installing dependencies
- Linting and formatting checks
- Running unit tests with coverage
- Auto-deployment on Render via webhook

📄 **`.github/workflows/backend.yml`**

[View backend.yml](https://github.com/Aditya-gam/ah-aihms-backend/blob/master/.github/workflows/backend.yml)

---

## 🌐 Frontend Integration

Frontend URLs (managed in `.env`):

```env
REACT_APP_API_BASE_URL=your-api-url # Production
REACT_APP_API_BASE_URL=http://localhost:5001/api                  # Development
```

---

## 📈 Logging & Monitoring (Sentry)

Sentry integrated for automatic error tracking and performance monitoring.

To configure Sentry:

- Sign up at [Sentry.io](https://sentry.io/)
- Create a Flask project.
- Replace `dsn` in `app/__init__.py`:

```python
sentry_sdk.init(
    dsn="your_sentry_dsn_here",
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0,
)
```

---

## 📋 Environment Variables

Managed through `.env`:

```env
SECRET_KEY=your_secure_key
FLASK_ENV=production
MONGODB_URI=your_mongodb_atlas_uri
```

---

## 🧾 Contribution Guidelines

1. Fork the repository.
2. Create your feature branch:
    ```bash
    git checkout -b feature/your-feature-name
    ```
3. Commit your changes:
    ```bash
    git commit -m "feat: add your feature"
    ```
4. Push changes:
    ```bash
    git push origin feature/your-feature-name
    ```
5. Open a Pull Request.

---

## 📄 License

Distributed under the **MIT License**. [See LICENSE file](LICENSE).

---

## 📧 Contact

- **Aditya Gambhir** - [agamb031@ucr.edu](mailto:agamb031@ucr.edu)  
- **Ajit Singh** - [asing349@ucr.edu](mailto:asing349@ucr.edu)

📦 [Project Repository](https://github.com/Aditya-gam/ah-aihms-backend)

---

## 📚 References & Acknowledgements

- [Flask Documentation](https://flask.palletsprojects.com/)
- [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
- [Docker Documentation](https://docs.docker.com/)
- [GitHub Actions](https://docs.github.com/actions)
- [Black Formatter](https://black.readthedocs.io/)
- [Flake8](https://flake8.pycqa.org/)
- [Ruff](https://docs.astral.sh/ruff/)
- [pytest](https://docs.pytest.org/)
- [Sentry](https://docs.sentry.io/)
- [Render](https://render.com/docs)
- [Codecov](https://about.codecov.io/)

---

### 🎯 Next Steps & Future Improvements

- Extend API functionality for blockchain integrations.
- Enhance monitoring with Prometheus & Grafana.
- Implement further security measures (rate-limiting, secure headers, etc.).