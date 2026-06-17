from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Auth API")

origins=[
    "http://localhost:5173",
    "https://yourfrentendDomain.com",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    )

from app.api.v1.auth_routes import auth_routes
from app.api.v1.user_routes import user_routes

app.include_router(auth_routes)

app.include_router(user_routes)
