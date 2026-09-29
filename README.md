# Textile POS & Billing System

A complete textile/retail POS application with Admin, Billing Staff, and mobile Admin interfaces. Built with React/TypeScript, FastAPI, PostgreSQL, and Docker.

## Demo

**Live:** https://textpos.brethren.in  
**Mobile Admin:** https://textpos.brethren.in/admin/mobile  
**API / Swagger:** https://textposback.brethren.in/docs  
**GitHub:** https://github.com/abelgeostan/textile-pos

If you experience any issues with the live demo, please run the project locally using the setup instructions provided in this README.

### Test Accounts

**Admin**
```text
admin@textilepos.com
Admin@123
```

**Billing Staff**
```text
cashier@textilepos.com
Cashier@123
```

## What to Test

### Admin
Open `/admin` after logging in as Admin.

You can test:
- Dashboard and reports
- Products and inventory
- Staff management
- Suppliers and purchases
- Billing transactions
- Product returns
- Ledger

### Mobile Admin
Open:

```text
https://textpos.brethren.in/admin/mobile
```

This is a dedicated mobile-style Admin UI. On desktop it appears inside a phone-sized layout; on mobile it uses the available screen.

### Billing
Log in with the Billing Staff account and open `/billing`.

Test:
1. Search/add products
2. Change quantities
3. Select payment method
4. For cash, enter the amount received and verify the change/balance
5. Complete the order
6. Print the invoice

Returns are linked to existing invoices and automatically update stock.

## Technology

- **Frontend:** React, TypeScript, Vite, Axios, React Router
- **Backend:** Python, FastAPI, SQLAlchemy, Pydantic
- **Authentication:** JWT + Argon2
- **Database:** PostgreSQL 16
- **Migrations:** Alembic
- **Deployment:** Docker, Docker Compose, Nginx
- **Public access:** Cloudflare Tunnel

## Production Deployment

The Docker Compose stack runs:

| Service | Host Port |
|---|---:|
| Frontend | `18731` |
| Backend | `18732` |
| PostgreSQL | `18733` (local only) |

Cloudflare Tunnel:

```text
textpos.brethren.in     -> http://localhost:18731
textposback.brethren.in -> http://localhost:18732
```

Do **not** expose PostgreSQL port `18733` publicly.

### Start

```bash
git clone https://github.com/abelgeostan/textile-pos.git
cd textile-pos

cp .env.example .env
```

Set a strong `JWT_SECRET` in `.env`, then:

```bash
docker compose up -d --build
```

Check:

```bash
docker compose ps
docker compose logs -f backend
```

### Useful URLs

```text
Frontend: http://SERVER_IP:18731
Backend:  http://SERVER_IP:18732
Swagger:  http://SERVER_IP:18732/docs
```

## Local Development

```bash
docker compose up --build
```

Frontend development server:

```bash
cd frontend
npm install
npm run dev
```

Then open:

```text
http://localhost:5173
```

## Database

PostgreSQL data is stored in the Docker volume `postgres_data`.

Migrations are in:

```text
backend/alembic/
```

The backend applies migrations and seeds demo data on startup.

To restart without deleting data:

```bash
docker compose down
docker compose up -d
```

Do **not** use `docker compose down -v` unless you want to delete the database volume.

## Demo Data

Seed data includes:
- Multiple products and stock levels
- Low-stock products (`stock < 10`)
- Multiple cashiers
- Suppliers and purchases
- Sales/orders
- Cash, UPI, and card transactions
- Returns
- Ledger entries

## Security Notes

- Demo credentials are for evaluation only.
- Change passwords before real-world use.
- Set a strong production `JWT_SECRET`.
- Never commit `.env` or production secrets.
- PostgreSQL should remain private.

## Project Structure

```text
textile-pos/
├── backend/
│   ├── alembic/
│   ├── app/
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   ├── Dockerfile
│   ├── nginx.conf
│   └── package.json
├── docker-compose.yml
├── .env.example
└── README.md
```

## If the Live Demo Has an Issue

Please use the GitHub repository and run the project locally using the setup instructions above.

## Submission Details

**Project:** Textile POS & Billing System  
**Live Demo:** https://textpos.brethren.in  
**Mobile Admin:** https://textpos.brethren.in/admin/mobile  
**GitHub:** https://github.com/abelgeostan/textile-pos
