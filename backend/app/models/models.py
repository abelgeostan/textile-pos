from datetime import datetime
from decimal import Decimal
from sqlalchemy import Boolean,DateTime,ForeignKey,Integer,Numeric,String,Text
from sqlalchemy.orm import Mapped,mapped_column,relationship
from app.db.session import Base

class User(Base):
    __tablename__='users'
    id:Mapped[int]=mapped_column(primary_key=True); name:Mapped[str]=mapped_column(String(120)); email:Mapped[str]=mapped_column(String(180),unique=True,index=True); password_hash:Mapped[str]=mapped_column(String(255)); role:Mapped[str]=mapped_column(String(30),default='billing_staff'); active:Mapped[bool]=mapped_column(Boolean,default=True); created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)
class Supplier(Base):
    __tablename__='suppliers'
    id:Mapped[int]=mapped_column(primary_key=True); name:Mapped[str]=mapped_column(String(180)); phone:Mapped[str|None]=mapped_column(String(40)); email:Mapped[str|None]=mapped_column(String(180)); address:Mapped[str|None]=mapped_column(Text); active:Mapped[bool]=mapped_column(Boolean,default=True)
    products:Mapped[list['Product']]=relationship(back_populates='supplier')
class Product(Base):
    __tablename__='products'
    id:Mapped[int]=mapped_column(primary_key=True); sku:Mapped[str]=mapped_column(String(60),unique=True,index=True); name:Mapped[str]=mapped_column(String(180),index=True); category:Mapped[str]=mapped_column(String(100)); size:Mapped[str|None]=mapped_column(String(30)); color:Mapped[str|None]=mapped_column(String(50)); purchase_price:Mapped[Decimal]=mapped_column(Numeric(12,2),default=0); selling_price:Mapped[Decimal]=mapped_column(Numeric(12,2)); stock:Mapped[int]=mapped_column(Integer,default=0); reorder_level:Mapped[int]=mapped_column(Integer,default=5); supplier_id:Mapped[int|None]=mapped_column(ForeignKey('suppliers.id',ondelete='SET NULL')); active:Mapped[bool]=mapped_column(Boolean,default=True); created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)
    supplier:Mapped[Supplier|None]=relationship(back_populates='products')
class Purchase(Base):
    __tablename__='purchases'
    id:Mapped[int]=mapped_column(primary_key=True); supplier_id:Mapped[int]=mapped_column(ForeignKey('suppliers.id')); product_id:Mapped[int]=mapped_column(ForeignKey('products.id')); quantity:Mapped[int]=mapped_column(Integer); unit_cost:Mapped[Decimal]=mapped_column(Numeric(12,2)); total:Mapped[Decimal]=mapped_column(Numeric(12,2)); purchased_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)
class Invoice(Base):
    __tablename__='invoices'
    id:Mapped[int]=mapped_column(primary_key=True); invoice_no:Mapped[str]=mapped_column(String(40),unique=True,index=True); staff_id:Mapped[int]=mapped_column(ForeignKey('users.id')); subtotal:Mapped[Decimal]=mapped_column(Numeric(12,2)); discount:Mapped[Decimal]=mapped_column(Numeric(12,2),default=0); tax:Mapped[Decimal]=mapped_column(Numeric(12,2),default=0); total:Mapped[Decimal]=mapped_column(Numeric(12,2)); payment_method:Mapped[str]=mapped_column(String(30)); paid_amount:Mapped[Decimal]=mapped_column(Numeric(12,2)); change_amount:Mapped[Decimal]=mapped_column(Numeric(12,2),default=0); created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)
    items:Mapped[list['InvoiceItem']]=relationship(back_populates='invoice',cascade='all, delete-orphan')
class InvoiceItem(Base):
    __tablename__='invoice_items'
    id:Mapped[int]=mapped_column(primary_key=True); invoice_id:Mapped[int]=mapped_column(ForeignKey('invoices.id',ondelete='CASCADE')); product_id:Mapped[int]=mapped_column(ForeignKey('products.id')); product_name:Mapped[str]=mapped_column(String(180)); quantity:Mapped[int]=mapped_column(Integer); unit_price:Mapped[Decimal]=mapped_column(Numeric(12,2)); line_total:Mapped[Decimal]=mapped_column(Numeric(12,2))
    invoice:Mapped[Invoice]=relationship(back_populates='items')
class Return(Base):
    __tablename__='returns'
    id:Mapped[int]=mapped_column(primary_key=True); invoice_id:Mapped[int]=mapped_column(ForeignKey('invoices.id')); product_id:Mapped[int]=mapped_column(ForeignKey('products.id')); quantity:Mapped[int]=mapped_column(Integer); refund_amount:Mapped[Decimal]=mapped_column(Numeric(12,2)); reason:Mapped[str]=mapped_column(String(255)); processed_by:Mapped[int]=mapped_column(ForeignKey('users.id')); created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)
class LedgerEntry(Base):
    __tablename__='ledger_entries'
    id:Mapped[int]=mapped_column(primary_key=True); entry_type:Mapped[str]=mapped_column(String(30)); reference:Mapped[str]=mapped_column(String(80)); description:Mapped[str]=mapped_column(String(255)); amount:Mapped[Decimal]=mapped_column(Numeric(12,2)); created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)
