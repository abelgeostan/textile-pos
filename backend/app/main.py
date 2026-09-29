from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import auth,products,users,suppliers,billing,returns,reports
app=FastAPI(title='Textile POS API',version='1.0.0')
app.add_middleware(CORSMiddleware,allow_origins=[x.strip() for x in settings.cors_origins.split(',')],allow_credentials=True,allow_methods=['*'],allow_headers=['*'])
for r in [auth.router,products.router,users.router,suppliers.router,billing.router,returns.router,reports.router]: app.include_router(r)
@app.get('/api/health')
def health(): return {'status':'ok'}
