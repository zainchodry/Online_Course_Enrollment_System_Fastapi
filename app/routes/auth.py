from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from app.database import get_db
import app.models.user as user_models
import app.schemas.user as user_schemas
from app.utils import security, helpers
from app.utils.deps import get_current_user, get_current_active_user

router = APIRouter(prefix="/auth", tags=["Authentication & Profile"])

@router.post("/register", response_model=user_schemas.UserResponse)
def register(user: user_schemas.UserCreate, db: Session = Depends(get_db)):
    if db.query(user_models.User).filter(user_models.User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
        
    new_user = user_models.User(
        email=user.email, 
        hashed_password=security.get_password_hash(user.password),
        first_name=user.first_name,
        last_name=user.last_name,
        role=user.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Auto-create profile
    db.add(user_models.UserProfile(user_id=new_user.id))
    db.commit()
    
    return new_user

@router.post("/login", response_model=user_schemas.LoginResponse)
def login(user: user_schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(user_models.User).filter(user_models.User.email == user.email).first()
    if not user or not security.verify_password(user.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
        
    return {
        "access_token": security.create_access_token(data={"sub": user.email}), 
        "refresh_token": security.create_refresh_token(data={"sub": user.email}),
        "token_type": "bearer"
    }

@router.put("/change-password")
def change_password(
    data: user_schemas.ChangePassword, 
    db: Session = Depends(get_db), 
    current_user: user_models.User = Depends(get_current_user)
):
    if not security.verify_password(data.old_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid old password")
    if data.new_password != data.confirm_new_password:
        raise HTTPException(status_code=400, detail="New passwords do not match")
        
    current_user.hashed_password = security.get_password_hash(data.new_password)
    db.commit()
    return {"message": "Password updated successfully"}

@router.post("/request-reset-email")
def request_reset_email(data: user_schemas.ResetPasswordRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    user = db.query(user_models.User).filter(user_models.User.email == data.email).first()
    if user:
        token = security.create_reset_token(user.email)
        reset_link = f"http://localhost:3000/password-reset-confirm?token={token}"
        email_body = f"Hello {user.first_name},\n\nReset your password here:\n{reset_link}"
        background_tasks.add_task(helpers.send_email_background, user.email, "Password Reset", email_body)
    return {"message": "If the email exists, a reset link has been sent."}

@router.post("/reset-password-complete")
def reset_password(data: user_schemas.ResetPasswordConfirm, db: Session = Depends(get_db)):
    if data.new_password != data.confirm_new_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")
        
    try:
        payload = jwt.decode(data.token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
        email, token_type = payload.get("sub"), payload.get("type")
        if token_type != "reset": raise HTTPException(status_code=400, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
        
    user = db.query(user_models.User).filter(user_models.User.email == email).first()
    if not user: raise HTTPException(status_code=404, detail="User not found")
        
    user.hashed_password = security.get_password_hash(data.new_password)
    db.commit()
    return {"message": "Password reset successful"}

@router.get("/profile", response_model=user_schemas.UserProfileResponse)
def get_profile(current_user: user_models.User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    profile = db.query(user_models.UserProfile).filter(user_models.UserProfile.user_id == current_user.id).first()
    profile_data = profile.__dict__.copy()
    profile_data.update({"first_name": current_user.first_name, "last_name": current_user.last_name, "email": current_user.email, "role": current_user.role})
    return profile_data

@router.patch("/profile", response_model=user_schemas.UserProfileResponse)
def update_profile(
    update_data: user_schemas.UserProfileUpdate, 
    current_user: user_models.User = Depends(get_current_active_user), 
    db: Session = Depends(get_db)
):
    profile = db.query(user_models.UserProfile).filter(user_models.UserProfile.user_id == current_user.id).first()
    data_dict = update_data.model_dump(exclude_unset=True)
    
    if "first_name" in data_dict: current_user.first_name = data_dict.pop("first_name")
    if "last_name" in data_dict: current_user.last_name = data_dict.pop("last_name")
        
    for key, value in data_dict.items():
        setattr(profile, key, value)
        
    db.commit()
    db.refresh(profile)
    return get_profile(current_user, db)