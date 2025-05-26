# FastAPI Auth Service - Run with Docker

1. Clone the repository:

git clone https://github.com/vratan1401/auth_service.git
cd auth_service

2. Create the .env file (based on example below):

cat > .env <<EOF
# JWT config
JWT_SECRET_KEY=supersecretkey123
JWT_REFRESH_SECRET_KEY=refresh-secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_MINUTES=10080

# PostgreSQL config
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
DB_NAME=auth_db

# Redis config
REDIS_HOST=redis
REDIS_PORT=6379
EOF

3. Run the app with Docker:

docker-compose up --build

# FastAPI runs at http://localhost:8000
# API docs: http://localhost:8000/docs

4. To stop it:

docker-compose down
