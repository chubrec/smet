Backend for Construction Estimate App

Run locally with Docker:

1. docker compose up -d --build
2. Run DB migrations: docker compose exec backend bash -lc "alembic upgrade head"
3. Open API docs: http://localhost:8000/docs

Sample requests:

- Create project:

  POST /projects {"name":"Apartment 60m2","client_name":"Client","currency":"EUR"}

- Create work:

  POST /works {"name":"Painting walls","unit":"m2","base_rate":20}

- Create estimate:

  POST /estimates {"project_id":1,"name":"Base","items":[{"work_id":1,"quantity":200,"unit":"m2","unit_price":20}]}

