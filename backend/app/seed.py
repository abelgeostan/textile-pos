from datetime import datetime, timedelta
from decimal import Decimal
from app.db.session import SessionLocal
from app.models.models import User,Supplier,Product,Invoice,InvoiceItem,LedgerEntry,Purchase
from app.core.security import hash_password

ADMIN_EMAIL='admin@textilepos.com'
CASHIER_EMAIL='cashier@textilepos.com'

STAFF_SEED=[
 ('Counter Cashier','cashier@textilepos.com','Cashier@123'),
 ('Anjali Menon','anjali@textilepos.com','Cashier@123'),
 ('Rahul Nair','rahul@textilepos.com','Cashier@123'),
 ('Meera Joseph','meera@textilepos.com','Cashier@123'),
 ('Vishnu Kumar','vishnu@textilepos.com','Cashier@123'),
]
SUPPLIERS=[
 ('Demo Textiles Supplier','9876543210','supplier@example.com','Broadway, Kochi'),
 ('Malabar Fabrics','9847012345','sales@malabarfabrics.com','Kaloor, Kochi'),
 ('Cochin Garments Wholesale','9895012345','orders@cochingarments.com','Palarivattom, Kochi'),
 ('Kerala Cotton House','9037012345','hello@keralacotton.com','Edappally, Kochi'),
]
PRODUCTS=[
 ('TSH-001','Premium Cotton T-Shirt','T-Shirts','L','Navy',350,699,40),
 ('SRT-001','Linen Casual Shirt','Shirts','M','White',650,1299,25),
 ('JNS-001','Regular Fit Jeans','Jeans','32','Blue',900,1799,18),
 ('KUR-001','Cotton Kurta','Ethnic','XL','Maroon',500,999,8),
 ('TSH-002','Classic Crew T-Shirt','T-Shirts','M','Black',300,599,32),
 ('TSH-003','Oversized Graphic Tee','T-Shirts','XL','Olive',420,899,14),
 ('SRT-002','Formal Oxford Shirt','Shirts','L','Sky Blue',720,1499,22),
 ('SRT-003','Checked Casual Shirt','Shirts','M','Green',580,1199,7),
 ('JNS-002','Slim Fit Jeans','Jeans','34','Dark Blue',950,1899,16),
 ('JNS-003','Straight Fit Jeans','Jeans','30','Black',880,1699,6),
 ('KUR-002','Printed Cotton Kurta','Ethnic','L','Mustard',540,1099,11),
 ('SAR-001','Cotton Saree','Sarees','Free','Teal',850,1699,19),
 ('SAR-002','Printed Daily Saree','Sarees','Free','Pink',620,1299,5),
 ('DRE-001','Women Casual Dress','Dresses','M','Wine',700,1499,13),
 ('KID-001','Kids Cotton Set','Kids','6Y','Yellow',380,799,24),
 ('TRS-001','Cotton Trousers','Trousers','32','Beige',560,1099,9),
 ('SHO-001','Men Casual Chinos','Trousers','34','Khaki',610,1199,17),
 ('DUP-001','Cotton Dupatta','Accessories','Free','Peach',220,449,28),
]

def get_or_create_user(db,name,email,password,role):
    user=db.query(User).filter(User.email==email).first()
    if not user:
        user=User(name=name,email=email,password_hash=hash_password(password),role=role,active=True)
        db.add(user); db.flush()
    return user

def seed():
    db=SessionLocal()
    try:
        # Repair the old local demo emails if this database came from an earlier build.
        legacy_admin=db.query(User).filter(User.email=='admin@textilepos.local').first()
        admin=db.query(User).filter(User.email==ADMIN_EMAIL).first()
        if legacy_admin and not admin:
            legacy_admin.email=ADMIN_EMAIL; admin=legacy_admin
        if not admin:
            admin=get_or_create_user(db,'System Admin',ADMIN_EMAIL,'Admin@123','admin')

        legacy_cashier=db.query(User).filter(User.email=='cashier@textilepos.local').first()
        cashier=db.query(User).filter(User.email==CASHIER_EMAIL).first()
        if legacy_cashier and not cashier:
            legacy_cashier.email=CASHIER_EMAIL; cashier=legacy_cashier
        if not cashier:
            cashier=get_or_create_user(db,'Counter Cashier',CASHIER_EMAIL,'Cashier@123','billing_staff')

        for name,email,password in STAFF_SEED[1:]:
            get_or_create_user(db,name,email,password,'billing_staff')

        suppliers=[]
        for name,phone,email,address in SUPPLIERS:
            s=db.query(Supplier).filter(Supplier.name==name).first()
            if not s:
                s=Supplier(name=name,phone=phone,email=email,address=address,active=True); db.add(s); db.flush()
            suppliers.append(s)

        product_by_sku={p.sku:p for p in db.query(Product).all()}
        for idx,row in enumerate(PRODUCTS):
            sku,name,category,size,color,purchase_price,selling_price,stock=row
            if sku not in product_by_sku:
                p=Product(sku=sku,name=name,category=category,size=size,color=color,purchase_price=purchase_price,selling_price=selling_price,stock=stock,reorder_level=10,supplier_id=suppliers[idx%len(suppliers)].id)
                db.add(p); db.flush(); product_by_sku[sku]=p

        # Seed supplier purchases once, so supplier/purchase screens look realistic.
        if db.query(Purchase).count()==0:
            for idx,p in enumerate(list(product_by_sku.values())[:8]):
                supplier=suppliers[idx%len(suppliers)]
                qty=12+idx*3; cost=Decimal(str(p.purchase_price))
                db.add(Purchase(supplier_id=supplier.id,product_id=p.id,quantity=qty,unit_cost=cost,total=cost*qty,purchased_at=datetime.utcnow()-timedelta(days=idx+1)))
                db.add(LedgerEntry(entry_type='purchase',reference=f'PUR-{idx+1:04d}',description=f'Purchase from {supplier.name} · {p.name}',amount=-(cost*qty),created_at=datetime.utcnow()-timedelta(days=idx+1)))

        db.flush()
        staff=db.query(User).filter(User.role=='billing_staff',User.active==True).order_by(User.id).all()
        products=list(product_by_sku.values())
        invoice_count=db.query(Invoice).count()
        if invoice_count<25 and products and staff:
            # Add enough deterministic historical/current counter bills to make the demo feel like a live shop.
            next_no=1
            for inv in db.query(Invoice).all():
                try: next_no=max(next_no,int(inv.invoice_no.split('-')[-1])+1)
                except Exception: pass
            for n in range(invoice_count+1,26):
                p1=products[(n*3)%len(products)]
                p2=products[(n*5+2)%len(products)]
                q1=1+(n%2); q2=1 if n%3 else 2
                subtotal=Decimal(p1.selling_price)*q1 + Decimal(p2.selling_price)*q2
                payment=['cash','upi','card'][n%3]
                paid=subtotal
                if payment=='cash' and n%4==0: paid=subtotal+Decimal('100')
                created=datetime.utcnow()-timedelta(days=n%12,hours=n%9,minutes=n*3)
                inv=Invoice(invoice_no=f'INV-{next_no:06d}',staff_id=staff[n%len(staff)].id,subtotal=subtotal,discount=0,tax=0,total=subtotal,payment_method=payment,paid_amount=paid,change_amount=paid-subtotal,created_at=created)
                db.add(inv); db.flush()
                db.add_all([
                    InvoiceItem(invoice_id=inv.id,product_id=p1.id,product_name=p1.name,quantity=q1,unit_price=p1.selling_price,line_total=Decimal(p1.selling_price)*q1),
                    InvoiceItem(invoice_id=inv.id,product_id=p2.id,product_name=p2.name,quantity=q2,unit_price=p2.selling_price,line_total=Decimal(p2.selling_price)*q2),
                ])
                db.add(LedgerEntry(entry_type='sale',reference=inv.invoice_no,description=f'Sale {inv.invoice_no}',amount=subtotal,created_at=created))
                next_no+=1
        db.commit()
        print('Seed complete: demo accounts, staff, suppliers, products, purchases and counter bills are ready.')
    finally:
        db.close()

if __name__=='__main__': seed()
