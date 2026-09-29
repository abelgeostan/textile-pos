from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.models import User
from app.schemas.schemas import UserIn,UserOut
from app.core.security import hash_password
from app.api.deps import admin_required
router=APIRouter(prefix='/api/staff',tags=['staff'])
@router.get('',response_model=list[UserOut])
def list_staff(db:Session=Depends(get_db),user=Depends(admin_required)): return db.query(User).order_by(User.name).all()
@router.post('',response_model=UserOut)
def create(data:UserIn,db:Session=Depends(get_db),user=Depends(admin_required)):
    if db.query(User).filter(User.email==data.email).first(): raise HTTPException(409,'Email already exists')
    if not data.password: raise HTTPException(422,'Password is required')
    u=User(name=data.name,email=data.email,password_hash=hash_password(data.password),role=data.role,active=data.active); db.add(u); db.commit(); db.refresh(u); return u
@router.put('/{uid}',response_model=UserOut)
def update(uid:int,data:UserIn,db:Session=Depends(get_db),user=Depends(admin_required)):
    u=db.get(User,uid)
    if not u: raise HTTPException(404,'Staff member not found')
    u.name=data.name; u.email=data.email; u.role=data.role; u.active=data.active
    if data.password: u.password_hash=hash_password(data.password)
    db.commit(); db.refresh(u); return u
