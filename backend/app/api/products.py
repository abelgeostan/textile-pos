from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.db.session import get_db
from app.models.models import Product
from app.schemas.schemas import ProductIn,ProductOut
from app.api.deps import admin_required,billing_required
router=APIRouter(prefix='/api/products',tags=['products'])
@router.get('',response_model=list[ProductOut])
def list_products(q:str='',db:Session=Depends(get_db),user=Depends(billing_required)):
    x=db.query(Product).filter(Product.active==True)
    if q: x=x.filter(or_(Product.name.ilike(f'%{q}%'),Product.sku.ilike(f'%{q}%'),Product.category.ilike(f'%{q}%')))
    return x.order_by(Product.name).all()
@router.post('',response_model=ProductOut)
def create(data:ProductIn,db:Session=Depends(get_db),user=Depends(admin_required)):
    if db.query(Product).filter(Product.sku==data.sku).first(): raise HTTPException(409,'SKU already exists')
    p=Product(**data.model_dump()); db.add(p); db.commit(); db.refresh(p); return p
@router.put('/{pid}',response_model=ProductOut)
def update(pid:int,data:ProductIn,db:Session=Depends(get_db),user=Depends(admin_required)):
    p=db.get(Product,pid)
    if not p: raise HTTPException(404,'Product not found')
    for k,v in data.model_dump().items(): setattr(p,k,v)
    db.commit(); db.refresh(p); return p
@router.delete('/{pid}')
def delete(pid:int,db:Session=Depends(get_db),user=Depends(admin_required)):
    p=db.get(Product,pid)
    if not p: raise HTTPException(404,'Product not found')
    p.active=False; db.commit(); return {'message':'Product deactivated'}
