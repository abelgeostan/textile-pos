from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.models import Supplier,Purchase,Product,LedgerEntry
from app.schemas.schemas import SupplierIn,SupplierOut,PurchaseIn
from app.api.deps import admin_required
router=APIRouter(prefix='/api/suppliers',tags=['suppliers'])
@router.get('',response_model=list[SupplierOut])
def list_suppliers(db:Session=Depends(get_db),user=Depends(admin_required)): return db.query(Supplier).order_by(Supplier.name).all()
@router.post('',response_model=SupplierOut)
def create(data:SupplierIn,db:Session=Depends(get_db),user=Depends(admin_required)):
    s=Supplier(**data.model_dump()); db.add(s); db.commit(); db.refresh(s); return s
@router.put('/{sid}',response_model=SupplierOut)
def update(sid:int,data:SupplierIn,db:Session=Depends(get_db),user=Depends(admin_required)):
    s=db.get(Supplier,sid)
    if not s: raise HTTPException(404,'Supplier not found')
    for k,v in data.model_dump().items(): setattr(s,k,v)
    db.commit(); db.refresh(s); return s
@router.delete('/{sid}')
def delete(sid:int,db:Session=Depends(get_db),user=Depends(admin_required)):
    s=db.get(Supplier,sid)
    if not s: raise HTTPException(404,'Supplier not found')
    s.active=False; db.commit(); return {'message':'Supplier deactivated'}
@router.post('/purchases')
def purchase(data:PurchaseIn,db:Session=Depends(get_db),user=Depends(admin_required)):
    if not db.get(Supplier,data.supplier_id) or not db.get(Product,data.product_id): raise HTTPException(404,'Supplier or product not found')
    total=data.quantity*data.unit_cost; p=Purchase(**data.model_dump(),total=total); prod=db.get(Product,data.product_id); prod.stock+=data.quantity; prod.purchase_price=data.unit_cost
    db.add(p); db.add(LedgerEntry(entry_type='purchase',reference=f'PUR-{p.id}',description=f'Purchase from {db.get(Supplier,data.supplier_id).name}',amount=-total)); db.commit(); return {'message':'Purchase recorded','total':total,'stock':prod.stock}
