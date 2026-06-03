# MarsLink Backend

Backend simples em Python com FastAPI, seguindo o mesmo molde do projeto de referência:

```txt
database.py
main.py
models.py
schemas.py
seed.py
requirements.txt
.env
```

## Como rodar

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python -m uvicorn main:app --reload
```

Swagger:

```txt
http://localhost:8000/docs
```

## PostgreSQL

Crie o banco:

```sql
CREATE DATABASE marslink;
```

Depois configure o `.env`:

```env
DATABASE_URL=postgresql://postgres:SUA_SENHA@localhost:5432/marslink
AUTO_CREATE_TABLES=true
AUTO_SEED=true
```

## Tabelas

- missions
- messages
- tasks
- crew
- notifications
- emergency_alerts
- mission_logs
- map_points

## Endpoints

```txt
GET    /mission
PUT    /mission

GET    /messages
POST   /messages
PATCH  /messages/{id}/status
DELETE /messages/{id}

GET    /tasks
POST   /tasks
PUT    /tasks/{id}
DELETE /tasks/{id}

GET    /crew
POST   /crew
PUT    /crew/{id}
DELETE /crew/{id}

GET    /notifications
POST   /notifications
PATCH  /notifications/{id}/read
PATCH  /notifications/read-all
DELETE /notifications/{id}

GET    /emergency-alerts
POST   /emergency-alerts
POST   /emergency-alerts/trigger
DELETE /emergency-alerts/{id}

GET    /mission-logs
POST   /mission-logs
DELETE /mission-logs/{id}

GET    /map-points
POST   /map-points
PUT    /map-points/{id}
DELETE /map-points/{id}
```
