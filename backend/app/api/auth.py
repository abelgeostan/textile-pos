from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.schemas import Login,Token
from app.models.models import User
from app.core.security import verify_password,create_token,get_current_user
router=APIRouter(prefix='/api/auth',tags=['auth'])
@router.post('/login',response_model=Token)
def login(data:Login,db:Session=Depends(get_db)):
    u=db.query(User).filter(User.email==data.email).first()
    if not u or not u.active or not verify_password(data.password,u.password_hash): raise HTTPException(401,'Invalid email or password')
    return {'access_token':create_token(u),'user':{'id':u.id,'name':u.name,'email':u.email,'role':u.role}}
@router.get('/me')
def me(user=Depends(get_current_user)): return {'id':user.id,'name':user.name,'email':user.email,'role':user.role}
