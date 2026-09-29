# Textile POS & Billing System

A complete Point of Sale (POS) and billing application for a textile/retail business.

The system provides:
- Admin Portal
- Billing Staff Portal
- Mobile-specific Admin Portal
- Product and inventory management
- Staff and role management
- Supplier and purchase management
- Billing and payment processing
- Product returns
- Ledger and reports
- PostgreSQL persistence
- Docker-based deployment

---

## 1. Short Project Description

This project is a production-style textile/retail POS application built with a React + TypeScript frontend and a FastAPI backend backed by PostgreSQL.

The Admin Portal provides product/inventory management, staff management, suppliers and purchases, returns, transactions, ledger/reporting, and dashboard information.

The Billing Portal is optimized for fast counter billing. Staff can search products, build bills, change quantities, accept cash/UPI/card payments, calculate cash balance/change, complete transactions, and print invoices.

A dedicated mobile Admin Portal is available at `/admin/mobile`. It uses a mobile-app-style layout with bottom navigation and is displayed in a phone-sized frame even when opened on a desktop browser.

---

## 2. Technology Stack

### Frontend
- React
- TypeScript
- Vite
- Axios
- React Router
- Lucide React
- Responsive CSS

### Backend
- Python
- FastAPI
- SQLAlchemy
- Pydantic
- JWT authentication
- Argon2 password hashing
- Alembic migrations
- Uvicorn

### Database
- PostgreSQL 16
- PostgreSQL runs in Docker

### Deployment
- Docker
- Docker Compose
- Nginx for production frontend serving
- Cloudflare Tunnel / reverse proxy can be used for public access

---

## 3. Application URLs

### Production / Demo

Frontend:

https://textpos.brethren.in

Backend API:

https://textposback.brethren.in

Swagger API documentation:

https://textposback.brethren.in/docs

### Mobile Admin UI

Direct mobile Admin Portal:

https://textpos.brethren.in/admin/mobile

Sign in with the Admin account before opening this route.

The `/admin/mobile` route is specifically designed for the mobile Admin experience. On a desktop/laptop it remains inside a phone-sized application frame rather than switching back to the desktop sidebar layout.

---

## 4. Main Application Routes

| Route | Purpose | Access |
|---|---|---|
| `/login` | Authentication | Public |
| `/admin` | Desktop Admin Portal | Admin |
| `/admin/mobile` | Mobile Admin Portal | Admin |
| `/billing` | Counter Billing Portal | Billing Staff |

### Admin Portal

The Admin Portal includes:

- Dashboard
- Product CRUD
- Inventory information
- Staff management
- Staff activation/deactivation
- Supplier management
- Supplier purchases
- Product returns
- Billing/transaction records
- Ledger
- Sales/return reports

### Billing Portal

Billing staff can:

- Search products
- Add products to a bill
- Change quantities
- View totals
- Select payment method
- Enter cash received
- See change/balance to return
- Complete transactions
- Generate/print the final bill

### Mobile Admin Portal

The mobile Admin interface includes:

- Dashboard
- Products
- Bills
- Staff
- Reports
- More menu

The More menu contains administrative sections such as:

- Returns
- Suppliers/Purchases
- Billing Transactions
- Sign out

---

## 5. Test Credentials

### Admin

```text
Email:    admin@textilepos.com
Password: Admin@123
Role:     Admin
```

### Billing Staff

```text
Email:    cashier@textilepos.com
Password: Cashier@123
Role:     Billing Staff
```

The seed data also contains additional cashier/staff accounts for testing.

> These credentials are demo credentials only. Change them before using the application for real business data.

---

## 6. Public GitHub Repository

Repository:

```text
<ADD-YOUR-PUBLIC-GITHUB-REPOSITORY-URL-HERE>
```

The repository should contain the complete source code, including:

```text
backend/
frontend/
docker-compose.yml
.env.example
README.md
```

Do NOT commit a real `.env` file containing production secrets.

---

## 7. Production Deployment

The production Docker Compose configuration runs:

1. PostgreSQL
2. FastAPI backend
3. React frontend served by Nginx

### Ports

The stack uses these host ports:

| Service | Host Port | Public Hostname |
|---|---:|---|
| Frontend | `18731` | `textpos.brethren.in` |
| Backend | `18732` | `textposback.brethren.in` |
| PostgreSQL | `18733` | Not public |

PostgreSQL is bound locally and should NOT be exposed through a public tunnel.

### Cloudflare Tunnel

Configure the tunnel as:

```text
textpos.brethren.in
        ↓
http://localhost:18731
```

and:

```text
textposback.brethren.in
        ↓
http://localhost:18732
```

Do NOT expose:

```text
18733
```

publicly.

Cloudflare provides HTTPS externally while the local Docker services can remain HTTP.

---

## 8. Server Setup

Clone the GitHub repository:

```bash
git clone [https://github.com/abelgeostan/textile-pos.git](https://github.com/abelgeostan/textile-pos.git)
cd textile-pos
```

Create the production environment file:

```bash
cp .env.example .env
```

Edit `.env` and set a strong secret:

```env
JWT_SECRET=replace-this-with-a-long-random-secret
```

Then build and start the application:

```bash
docker compose up -d --build
```

Check the containers:

```bash
docker compose ps
```

View backend logs:

```bash
docker compose logs -f backend
```

View all logs:

```bash
docker compose logs -f
```

---

## 9. Verify the Deployment

Frontend:

```bash
curl -I http://localhost:18731
```

Backend health:

```bash
curl http://localhost:18732/api/health
```

Swagger:

```text
http://SERVER_IP:18732/docs
```

Frontend before the tunnel is configured:

```text
http://SERVER_IP:18731
```

After Cloudflare Tunnel configuration:

```text
https://textpos.brethren.in
```

---

## 10. Local Development

### Backend + PostgreSQL

Start PostgreSQL and backend:

```bash
docker compose up --build
```

Backend:

```text
http://localhost:8000
```

Swagger:

```text
http://localhost:8000/docs
```

### Frontend

From the frontend directory:

```bash
cd frontend
npm install
npm run dev
```

Frontend:

```text
http://localhost:5173
```

For local development, make sure the frontend API base URL points to the local backend if required.

---

## 11. Database

PostgreSQL data is persisted in the Docker volume:

```text
postgres_data
```

Backend migrations are stored under:

```text
backend/alembic/
```

On startup, the backend applies migrations and seeds demo data.

### Important

Do not use:

```bash
docker compose down -v
```

unless you intentionally want to delete the PostgreSQL Docker volume and all stored database data.

For a normal restart:

```bash
docker compose down
docker compose up -d
```

---

## 12. Seed / Demo Data

The application includes realistic demo data for testing:

- Multiple products
- Products with different stock levels
- Low-stock products
- Multiple staff/cashiers
- Suppliers
- Supplier purchases
- Billing transactions
- Different payment methods
- Returns
- Ledger entries

Low-stock products are identified when:

```text
stock < 10
```

---

## 13. Returns Workflow

Returns are linked to existing billing transactions.

The Admin can:

1. Select an invoice.
2. Select a product from that invoice.
3. See the quantity originally sold.
4. See previously returned quantity.
5. Enter the quantity being returned.
6. Select/enter the return reason.
7. Process the return.

The system prevents returning more than the remaining returnable quantity.

A successful return updates the relevant stock and financial records.

---

## 14. Billing Workflow

Billing Staff:

1. Log in.
2. Search/select products.
3. Add products to the current bill.
4. Adjust quantities.
5. Review subtotal/total.
6. Select payment method.
7. Complete payment.
8. For cash payments, enter the amount received.
9. If the received amount is higher than the bill total, the system calculates the change to return.
10. Complete the order.
11. Print the invoice.

---

## 15. Mobile Admin UI

Open:

```text
https://textpos.brethren.in/admin/mobile
```

The mobile Admin route is intentionally separate from the desktop Admin layout.

It provides:

- Phone-sized application frame on desktop
- Mobile header
- Bottom navigation
- Staff in the main bottom navigation
- Returns inside More
- Mobile-specific dashboard
- Responsive cards and tables
- Mobile-friendly administrative workflows

On a real mobile device, the application expands naturally to the device viewport.

---

## 16. Authentication and Roles

The application uses JWT authentication.

### Admin

Admin users can access administrative functionality including:

- Products
- Inventory
- Staff
- Suppliers
- Purchases
- Returns
- Transactions
- Ledger
- Reports
- Mobile Admin Portal

### Billing Staff

Billing Staff users are restricted to the Billing Portal and the functionality required for counter billing.

---

## 17. CORS / API Configuration

The production frontend uses:

```text
https://textposback.brethren.in/api
```

The backend allows the production frontend origin:

```text
https://textpos.brethren.in
```

The local Vite development origin is also supported.

---

## 18. Environment Variables

Example:

```env
DATABASE_URL=postgresql+psycopg://pos:pos@postgres:5432/posdb
JWT_SECRET=replace-with-a-long-random-secret
ACCESS_TOKEN_EXPIRE_MINUTES=480
CORS_ORIGINS=https://textpos.brethren.in,http://localhost:5173
```

Never publish production secrets in GitHub.

---

## 19. Important Notes / Limitations

- This is a POS/billing application intended for demonstration and evaluation.
- Production deployment should use a strong unique JWT secret.
- Demo passwords should be changed for real business use.
- PostgreSQL should remain private and should not be publicly tunneled.
- The public domain URLs require the corresponding DNS and Cloudflare Tunnel configuration.
- The application intentionally focuses only on the requested POS functionality and does not include unrelated CRM, HR, e-commerce, or full accounting modules.

---

## 20. GitHub Upload

After creating a public GitHub repository:

```bash
git init
git add .
git commit -m "Initial textile POS application"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
git push -u origin main
```

Before running `git add .`, make sure `.env` is excluded.

Recommended `.gitignore` entries:

```gitignore
.env
.env.*
!.env.example

node_modules/
dist/
__pycache__/
*.pyc
.venv/
venv/

.idea/
.vscode/

.DS_Store
Thumbs.db
```

If the repository already has a Git history, use:

```bash
git add .
git commit -m "Update Textile POS"
git push
```

---

## Project Structure

```text
textile-pos/
├── backend/
│   ├── alembic/
│   ├── app/
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── Dockerfile
│   ├── nginx.conf
│   └── package.json
│
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## Submission Summary

### 1. Short Project Description

Complete textile/retail POS and billing system with Admin and Billing Staff portals, inventory management, suppliers, purchases, returns, transactions, ledger/reporting, and a dedicated mobile Admin UI.

### 2. Technology Stack

React + TypeScript + Vite, FastAPI + Python, PostgreSQL, SQLAlchemy, Alembic, JWT, Argon2, Docker, Docker Compose, and Nginx.

### 3. Live/Demo URL

https://textpos.brethren.in

### 4. Mobile UI URL

https://textpos.brethren.in/admin/mobile

### 5. Public GitHub Repository

```text
<ADD-YOUR-PUBLIC-GITHUB-REPOSITORY-URL-HERE>
```

### 6. Test Credentials

```text
Admin
admin@textilepos.com
Admin@123

Billing Staff
cashier@textilepos.com
Cashier@123
```

### 7. Additional Notes

The application is Dockerized and can run as a three-service stack consisting of PostgreSQL, FastAPI, and the production React/Nginx frontend. The frontend uses `https://textposback.brethren.in/api` for the production API. Cloudflare Tunnel can expose the frontend on port `18731` and backend on port `18732`; PostgreSQL uses port `18733` locally and should remain private.
