from datetime import datetime,timedelta
from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi import APIRouter,Depends
from app.db.session import get_db
from app.models.models import Product,Invoice,Return,LedgerEntry
from app.api.deps import admin_required
router=APIRouter(prefix='/api/reports',tags=['reports'])
@router.get('/dashboard')
def dashboard(db:Session=Depends(get_db),user=Depends(admin_required)):
    today=datetime.utcnow().date(); start=datetime.combine(today,datetime.min.time())
    sales=db.query(func.coalesce(func.sum(Invoice.total),0)).filter(Invoice.created_at>=start).scalar() or 0
    gross=db.query(func.coalesce(func.sum(Invoice.total),0)).scalar() or 0
    bills=db.query(func.count(Invoice.id)).filter(Invoice.created_at>=start).scalar() or 0
    returns=db.query(func.coalesce(func.sum(Return.refund_amount),0)).filter(Return.created_at>=start).scalar() or 0
    low=db.query(func.count(Product.id)).filter(Product.active==True,Product.stock<10).scalar() or 0
    return {'gross_sales':float(gross),'today_sales':float(sales),'today_bills':bills,'today_returns':float(returns),'low_stock':low}
@router.get('/ledger')
def ledger(db:Session=Depends(get_db),user=Depends(admin_required)):
    return [{'id':x.id,'entry_type':x.entry_type,'reference':x.reference,'description':x.description,'amount':float(x.amount),'created_at':x.created_at.isoformat()} for x in db.query(LedgerEntry).order_by(LedgerEntry.created_at.desc()).limit(200).all()]
