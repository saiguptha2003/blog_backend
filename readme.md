# Blog Backend API
A FastAPI-based RESTful API for managing blog posts and user authentication.

## Features
    - User authentication (signup/login)
    - JWT token-based authorization
    - CRUD operations for blog posts
    - PostgreSQL database integration
    - Docker containerization
    - Logging system
    - API documentation with Swagger UI

## Technology Stack
    - Python 3.11
    - FastAPI
    - SQLAlchemy
    - PostgreSQL
    - Docker
    - Pydantic
    - JWT Authentication

## Setup Instructions
### Local Development
#### Clone the repository:

```bash
git clone https://github.com/saiguptha2003/blog_backend.git
cd blog_backend
```

#### Create and activate virtual environment:

```bash
python -m venv env
.\env\Scripts\activate
```

#### Install dependencies:
```bash
pip install -r requirements.txt
```

#### Run the application:
```bash
uvicorn main:app --reload
```
### Docker Setup

#### Build and run with Docker Compose:
```bash
docker-compose up --build
```

#### Stop containers:
```bash
docker-compose down
```

## API Endpoints
### Authentication
- POST /auth/signup - Register new user
- POST /auth/login - Login user

### Blogs
- POST /blogs/ - Create new blog
- GET /blogs/ - List all blogs
- GET /blogs/{id} - Get specific blog
- PUT /blogs/{id} - Update blog
- DELETE /blogs/{id} - Delete blog

## Testing
Use the provided api.http file with VS Code's REST Client extension to test endpoints:

- Sign up a new user
- Login to get JWT token
- Use token for authenticated endpoints

## Documentation
Access API documentation at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Logging
- Logs are stored in app.log with daily rotation.


## Cloud Deployments 

    - https://api-blogify.onrender.com  -- backend API can go through https://api-blogify.onrender.com/docs

    - https://blogify-x.netlify.app -- Frontend URL can go through ui