# Lynkeer API

> A secure and scalable FastAPI-based REST API for business management with JWT authentication.

## 🚀 Features

- JWT Authentication
- Role-based Access Control
- Owner Management
- PostgreSQL Database Integration
- Docker Containerization
- API Documentation with Swagger/OpenAPI

## 🛠️ Tech Stack

- **FastAPI** - Modern web framework
- **SQLModel** - SQL toolkit and ORM
- **PostgreSQL** - Primary database
- **JWT** - Authentication using JSON Web Tokens
- **Docker** - Containerization
- **Pydantic** - Data validation
- **Uvicorn** - ASGI web server

## 🏗️ Project Structure

```
lynkeer-api/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   ├── auth.py
│   │       │   └── owner.py
│   │       └── routers/
│   ├── core/
│   │   ├── config.py
│   │   ├── db.py
│   │   └── security.py
│   ├── models/
│   │   └── owner.py
│   └── main.py
├── tests/
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Docker & Docker Compose
- PostgreSQL

### Development Setup

1. Clone the repository:
````markdown
```bash
git clone git@github.com:lynkeer-org/lynkeer-api.git
cd lynkeer-api
```
````markdown

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configurations
```

### Running with Docker

```bash
docker-compose up --build
```

The API will be available at `http://localhost:80`

## 📚 API Documentation

Once the server is running, access:
- Swagger UI: `http://localhost:80/docs`
- ReDoc: `http://localhost:80/redoc`

### Authentication

The API uses JWT tokens for authentication:

```bash
POST /api/v1/auth/signin
{
    "email": "owner@example.com",
    "password": "your_password"
}
```

Use the returned token in the Authorization header:
```bash
Authorization: Bearer <your_token>
```

## 🧪 Testing

Run the test suite:

```bash
pytest
```

## 📦 Deployment

1. Build the Docker image:
```bash
docker build -t lynkeer-api .
```

2. Deploy using Docker Compose:
```bash
docker-compose -f docker-compose.prod.yml up -d
```

## 🛡️ Security

- JWT authentication
- Password hashing with bcrypt
- Environment variable configuration
- CORS protection
- Input validation with Pydantic

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This repository is **not licensed for public or commercial use**.
It is shared for development and collaboration purposes only, with explicit permission from the Lynkeer team.

All rights reserved © 2025 Lynkeer.
See [`LICENSE.txt`](./LICENSE.txt) for full terms.

## 📫 Contact

Want to collaborate or have questions?
Reach us at [contact@lynkeer.com](mailto:contact@lynkeer.com)

---

Made with ❤️ by the Lynkeer Team
