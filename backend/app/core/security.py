from datetime import datetime,timedelta,timezone
from jose import jwt,JWTError
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError, InvalidHash
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.config import settings
from app.db.session import get_db
from app.models.models import User

password_hasher=PasswordHasher()
oauth2_scheme=OAuth2PasswordBearer(tokenUrl='/api/auth/login')

def hash_password(password: str) -> str:
    return password_hasher.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    try:
        return password_hasher.verify(hashed, password)
    except (VerifyMismatchError, VerificationError, InvalidHash):
        return False
def create_token(user:User)->str:
    exp=datetime.now(timezone.utc)+timedelta(minutes=settings.access_token_expire_minutes)
    return jwt.encode({'sub':str(user.id),'role':user.role,'name':user.name,'exp':exp},settings.jwt_secret,algorithm='HS256')

def get_current_user(token:str=Depends(oauth2_scheme),db:Session=Depends(get_db)):
    exc=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Invalid or expired authentication token',headers={'WWW-Authenticate':'Bearer'})
    try: uid=int(jwt.decode(token,settings.jwt_secret,algorithms=['HS256']).get('sub'))
    except (JWTError,TypeError,ValueError): raise exc
    user=db.get(User,uid)
    if not user or not user.active: raise exc
    return user

def require_roles(*roles):
    def dep(user=Depends(get_current_user)):
        if user.role not in roles: raise HTTPException(status_code=403,detail='Insufficient permissions')
        return user
    return dep
