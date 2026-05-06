from fastapi import APIRouter, Depends, Form
from app.db.models import User
from app.db.dependencies import get_session
from app.utilities import get_pwd_hash, verify_password, create_access_token, get_current_active_user
from app.schemas import tokenSchema, UserRole
from sqlalchemy.orm import Session
from app.schemas import userResponse
from fastapi.security import OAuth2PasswordRequestForm
from app.exceptions import raise_not_found_exception
from app.utilities import verify_access_token

auth_routes=APIRouter(prefix="/api/v1/auth",tags=["Auth"])


@auth_routes.get("/verify-token/{token}")
def verify_token(token:str)->dict | None:   
    """
     This endpoint to register a user.
    """
   
    return verify_access_token(token)


@auth_routes.post("/register", response_model=userResponse)
def register(
    name: str = Form(""),
    username: str = Form(""),
    password: str = Form(""),
    phone: str = Form(""),
    role: UserRole = Form(""),
    admin: bool = Form(False),
    active: bool = Form(True),
    db: Session = Depends(get_session)
):
    db_user = db.query(User).filter(User.username == username).first()
    if db_user:
        raise_not_found_exception(detail="user already exists!")

    hashed_password = get_pwd_hash(password)
    new_user = User(
        name=name,
        username=username,
        password=hashed_password,
        admin=admin,
        phone=phone,
        active=active,
        role=role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@auth_routes.post("/token",response_model=tokenSchema)
def login_for_access_token(form_data:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_session)):
    """autheticate a user by checking its password and email"""

    
    db_user=db.query(User).filter(User.username==form_data.username).first()


    if not db_user or not verify_password(db_user.password,form_data.password):
       
        raise_not_found_exception(detail="Wrong credentials")
    
    if not db_user.active:  
        raise_not_found_exception(detail="Inactive user")
        
   
    access_token = create_access_token(db_user.id, db_user.username)
    return {
        "access_token": access_token,
        "current_user": db_user
    }


@auth_routes.get("/me", response_model=userResponse)
def get_current_user_info(current_user: User = Depends(get_current_active_user)):
    """Get current authenticated user info - requires Authorization header"""
    return current_user