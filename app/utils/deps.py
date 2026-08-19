from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from database import get_db
from models.user import User
from models.base import RoleEnum
from utils import security

# This URL must match your login route for Swagger UI integration
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
        email: str = payload.get("sub")
        token_type: str = payload.get("type")
        
        if email is None or token_type != "access":
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user

def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user account")
    return current_user

def require_instructor_or_admin(current_user: User = Depends(get_current_active_user)) -> User:
    """Enforces that the user can create or manage courses."""
    if current_user.role not in [RoleEnum.INSTRUCTOR, RoleEnum.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="You must be an instructor or admin to perform this action."
        )
    return current_user

def require_student(current_user: User = Depends(get_current_active_user)) -> User:
    """Enforces that the user is a student (e.g., for enrollments or reviews)."""
    if current_user.role != RoleEnum.STUDENT:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Only students can perform this action."
        )
    return current_user