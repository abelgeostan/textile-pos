from decimal import Decimal
from pydantic import BaseModel,ConfigDict,EmailStr,Field
class Token(BaseModel): access_token:str; token_type:str='bearer'; user:dict
class Login(BaseModel): email:EmailStr; password:str
class ProductIn(BaseModel): sku:str; name:str; category:str; size:str|None=None; color:str|None=None; purchase_price:Decimal=0; selling_price:Decimal; stock:int=0; reorder_level:int=5; supplier_id:int|None=None; active:bool=True
class ProductOut(ProductIn): id:int; model_config=ConfigDict(from_attributes=True)
class UserIn(BaseModel): name:str; email:EmailStr; password:str|None=None; role:str='billing_staff'; active:bool=True
class UserOut(BaseModel): id:int; name:str; email:EmailStr; role:str; active:bool; model_config=ConfigDict(from_attributes=True)
class SupplierIn(BaseModel): name:str; phone:str|None=None; email:EmailStr|None=None; address:str|None=None; active:bool=True
class SupplierOut(SupplierIn): id:int; model_config=ConfigDict(from_attributes=True)
class PurchaseIn(BaseModel): supplier_id:int; product_id:int; quantity:int=Field(gt=0); unit_cost:Decimal=Field(ge=0)
class BillItem(BaseModel): product_id:int; quantity:int=Field(gt=0)
class BillIn(BaseModel): items:list[BillItem]; discount:Decimal=Field(default=0,ge=0); tax:Decimal=Field(default=0,ge=0); payment_method:str='cash'; paid_amount:Decimal=Field(gt=0)
class ReturnIn(BaseModel): invoice_id:int=Field(gt=0); product_id:int=Field(gt=0); quantity:int=Field(gt=0); reason:str='Customer return'
