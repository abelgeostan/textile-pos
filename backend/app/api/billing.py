from decimal import Decimal
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session,joinedload
from sqlalchemy import func
from app.db.session import get_db
from app.models.models import Product,Invoice,InvoiceItem,LedgerEntry
from app.schemas.schemas import BillIn
from app.api.deps import billing_required,admin_required
router=APIRouter(prefix='/api/billing',tags=['billing'])
@router.post('/invoices')
def create_bill(data:BillIn,db:Session=Depends(get_db),user=Depends(billing_required)):
    if not data.items: raise HTTPException(422,'Bill must contain at least one item')
    subtotal=Decimal('0'); prepared=[]
    for it in data.items:
        p=db.get(Product,it.product_id)
        if not p or not p.active: raise HTTPException(404,f'Product {it.product_id} not found')
        if p.stock<it.quantity: raise HTTPException(400,f'Insufficient stock for {p.name}. Available: {p.stock}')
        line=p.selling_price*it.quantity; subtotal+=line; prepared.append((p,it.quantity,line))
    total=subtotal-data.discount+data.tax
    if total<0: raise HTTPException(400,'Discount cannot exceed subtotal plus tax')
    if data.paid_amount<total: raise HTTPException(400,'Paid amount is less than total')
    no=f'INV-{db.query(Invoice).count()+1:06d}'
    while db.query(Invoice).filter(Invoice.invoice_no==no).first(): no=f'INV-{db.query(Invoice).count()+1:06d}'
    inv=Invoice(invoice_no=no,staff_id=user.id,subtotal=subtotal,discount=data.discount,tax=data.tax,total=total,payment_method=data.payment_method,paid_amount=data.paid_amount,change_amount=data.paid_amount-total)
    db.add(inv); db.flush()
    for p,q,line in prepared:
        p.stock-=q; db.add(InvoiceItem(invoice_id=inv.id,product_id=p.id,product_name=p.name,quantity=q,unit_price=p.selling_price,line_total=line))
    db.add(LedgerEntry(entry_type='sale',reference=no,description=f'Sale {no}',amount=total)); db.commit(); db.refresh(inv)
    return invoice_detail(inv,db)
@router.get('/invoices')
def invoices(db:Session=Depends(get_db),user=Depends(billing_required)):
    rows=db.query(Invoice).options(joinedload(Invoice.items)).order_by(Invoice.created_at.desc()).limit(100).all(); return [invoice_dict(x) for x in rows]
@router.get('/invoices/{iid}')
def invoice(iid:int,db:Session=Depends(get_db),user=Depends(billing_required)):
    inv=db.query(Invoice).options(joinedload(Invoice.items)).filter(Invoice.id==iid).first()
    if not inv: raise HTTPException(404,'Invoice not found')
    return invoice_dict(inv)
def invoice_dict(x): return {'id':x.id,'invoice_no':x.invoice_no,'staff_id':x.staff_id,'subtotal':float(x.subtotal),'discount':float(x.discount),'tax':float(x.tax),'total':float(x.total),'payment_method':x.payment_method,'paid_amount':float(x.paid_amount),'change_amount':float(x.change_amount),'created_at':x.created_at.isoformat(),'items':[{'product_id':i.product_id,'product_name':i.product_name,'quantity':i.quantity,'unit_price':float(i.unit_price),'line_total':float(i.line_total)} for i in x.items]}
def invoice_detail(inv,db): return invoice_dict(inv)
