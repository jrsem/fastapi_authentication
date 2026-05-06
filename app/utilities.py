from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, InvalidHashError
from dotenv import load_dotenv
from datetime import timedelta, datetime, timezone
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
import os
from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.dependencies import get_session
from app.db.models import User
from app.exceptions import raise_unauthorized_exception, raise_not_found_exception
from fastapi.security import OAuth2PasswordBearer
import uuid

load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

password_hasher = PasswordHasher()

SALT = os.getenv("SALT", "")


def get_pwd_hash(plain_password: str) -> str:
    password_with_salt = SALT + plain_password
    return password_hasher.hash(password_with_salt)


def verify_password(hashed_pwd: str, plain_pwd: str) -> bool:
    password_with_salt = SALT + plain_pwd
    try:
        return password_hasher.verify(hashed_pwd, password_with_salt)
    except VerifyMismatchError:
        print("Incorrect username or password")
        return False
    except InvalidHashError:
        print("CRITICAL: Invalid hash format detected.")
        return False
    except Exception:
        print("CRITICAL: Authentication failed due to system error.")
        return False


def create_access_token(user_id: uuid.UUID, user_username: str) -> str:
    payload = {
        "sub": str(user_id),
        "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        "iat": datetime.now(timezone.utc),
        "username": user_username
    }

    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM", "HS256")
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str) -> dict | None:
    ALGORITHM = os.getenv("ALGORITHM", "HS256")

    try:
        payload = jwt.decode(
            token,
            key=os.getenv("SECRET_KEY"),
            algorithms=[ALGORITHM]
        )
        user_id = payload.get("sub")
        if user_id is None:
            return None
        return payload

    except ExpiredSignatureError:
        print("Verification Failed: Token has expired.")
        return None

    except InvalidTokenError:
        print("Verification Failed: Invalid signature, algorithm, or token format.")
        return None

    except Exception as e:
        print(f"Verification Failed due to an unexpected error: {e}")
        return None


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_session)):
    if token is None:
        raise_unauthorized_exception(detail="token expired")

    user_payload = verify_access_token(token)

    if user_payload is None:
        raise_unauthorized_exception(detail="token expired")

    current_user = db.query(User).filter(User.username == user_payload.get("username")).first()
    current_user_id = user_payload.get("sub")

    if current_user is None or current_user_id is None:
        raise_unauthorized_exception(detail="Could not validate user")

    return current_user


