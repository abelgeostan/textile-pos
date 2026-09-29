from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.models import Return,Invoice,InvoiceItem,Product,LedgerEntry
from app.schemas.schemas import ReturnIn
from app.api.deps import admin_required
router=APIRouter(prefix='/api/returns',tags=['returns'])
@router.get('')
def list_returns(db:Session=Depends(get_db),user=Depends(admin_required)):
    return [{'id':r.id,'invoice_id':r.invoice_id,'product_id':r.product_id,'quantity':r.quantity,'refund_amount':float(r.refund_amount),'reason':r.reason,'created_at':r.created_at.isoformat()} for r in db.query(Return).order_by(Return.created_at.desc()).limit(100).all()]
@router.post('')
def process(data:ReturnIn,db:Session=Depends(get_db),user=Depends(admin_required)):
    inv=db.get(Invoice,data.invoice_id); p=db.get(Product,data.product_id)
    if not inv or not p: raise HTTPException(404,'Invoice or product not found')
    item=db.query(InvoiceItem).filter(InvoiceItem.invoice_id==inv.id,InvoiceItem.product_id==p.id).first()
    if not item or data.quantity>item.quantity: raise HTTPException(400,'Return quantity exceeds sold quantity')
    already=db.query(Return).filter(Return.invoice_id==inv.id,Return.product_id==p.id).all(); returned=sum(r.quantity for r in already)
    if returned+data.quantity>item.quantity: raise HTTPException(400,'Return quantity exceeds remaining returnable quantity')
    refund=item.unit_price*data.quantity; r=Return(invoice_id=inv.id,product_id=p.id,quantity=data.quantity,refund_amount=refund,reason=data.reason,processed_by=user.id); p.stock+=data.quantity
    db.add(r); db.add(LedgerEntry(entry_type='return',reference=inv.invoice_no,description=f'Return for {inv.invoice_no}',amount=-refund)); db.commit()
    return {'message':'Return processed','refund_amount':float(refund),'new_stock':p.stock}
